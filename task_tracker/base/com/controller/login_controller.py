from flask import render_template, redirect, request, url_for, make_response, session, flash, jsonify
from base import app
from base.com.dao.login_dao import LoginDAO
from base.com.dao.user_dao import UserDAO
from base.com.vo.login_vo import LoginVO
from base.com.vo.user_vo import UserVO
from base.com.vo.task_vo import TaskVO
from base.com.dao.task_dao import TaskDAO
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

@app.route('/', methods=['GET','POST'])
def home():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        login_vo = LoginVO()
        login_dao = LoginDAO()
        login_vo.login_username = request.form.get('email')
        login_vo.login_password = request.form.get('password')
        test = login_dao.authenticate_user(login_vo)
        final = [i.as_dict() for i in test]
        print(final)
        if final:
            response = make_response(redirect(url_for('dashboard')))
            response.set_cookie('user_unique', value=str(final[0]['login_id']))
            return response
        else:
            flash('username or password is wrong!')
            return redirect('/')

@app.route('/register_page', methods=['GET','POST'])
def register_page():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        user_vo = UserVO()
        user_dao = UserDAO()
        login_vo = LoginVO()
        login_dao = LoginDAO()
        user_vo.user_firstname = request.form.get('first_name')
        user_vo.user_lastname = request.form.get('last_name')
        user_vo.user_contact = request.form.get('contact')
        login_vo.login_username = request.form.get('email')
        login_vo.login_password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        test = login_dao.search_user_exist(login_vo)
        final = [i.as_dict() for i in test]
        if final:
            flash('already exist')
            return redirect('/register_page')
        if login_vo.login_password != confirm_password:
            flash('password does not match')
            return redirect('/register_page')
        else:
            login_dao.save_user(login_vo)
            user_dao.add_user(user_vo)
            flash('successfully registered')
            return redirect('/')

@app.route('/create_task_load', methods=['GET','POST'])
def create_task_load():
    if str(request.cookies.get('user_unique'))!= 'None':
        return render_template('create_task.html')
    else:
        return redirect('/')


@app.route('/create_task', methods=['POST'])
def create_task():
    task_vo = TaskVO()
    task_dao = TaskDAO()
    task_vo_list = task_dao.view_task(task_vo)
    if request.method == 'POST':
        task_vo.task_title = request.form.get('task_title')
        task_vo.task_description = request.form.get('task_description')
        task_vo.task_user_id =  str(request.cookies.get('user_unique'))
        task_vo.task_due_date = request.form.get('task_due_date')
        flash('Task created successfully')
        task_dao.insert_task(task_vo)
        login_vo = LoginVO()
        login_dao = LoginDAO()
        login_vo.login_id = int(request.cookies.get('user_unique'))
        user_name = login_dao.find_login_username(login_vo)
        send_mail(user_name,task_vo)
        return redirect("/modify_task")

@app.route('/dashboard', methods=['GET','POST'])
def dashboard():
    if str(request.cookies.get('user_unique'))=='None':
        return redirect('/')
    task_vo = TaskVO()
    task_dao = TaskDAO()
    task_vo.task_user_id = str(request.cookies.get('user_unique'))
    task_vo_list = task_dao.view_task(task_vo)
    return render_template('index.html',task_vo_list=task_vo_list)

@app.route('/modify_task', methods=['GET','POST'])
def modify_task():
    if str(request.cookies.get('user_unique'))=='None':
        return redirect('/')
    else:
        task_vo = TaskVO()
        task_dao = TaskDAO()
        task_vo.task_user_id = str(request.cookies.get('user_unique'))
        task_vo_list = task_dao.view_task(task_vo)
        return render_template('modify_task.html',task_vo_list=task_vo_list)

@app.route('/task_edit', methods=['GET'])
def edit_task():
    if str(request.cookies.get('user_unique'))!='None':
        task_vo = TaskVO()
        task_dao = TaskDAO()
        task_vo.task_id = int(request.args.get("task_id"))
        task_list = task_dao.search_task(task_vo)
        return render_template('edit_task.html',task=task_list)
    else:
        return redirect('/')

@app.route('/save_edit_task', methods=['POST'])
def save_edit_task():
    task_vo = TaskVO()
    task_dao = TaskDAO()
    task_vo_list = task_dao.view_task(task_vo)
    if request.method == 'POST':
        task_vo.task_id = request.form.get('task_id')
        task_vo.task_title = request.form.get('task_title')
        task_vo.task_description = request.form.get('task_description')
        task_vo.task_due_date = request.form.get('task_due_date')
        flash('Task edited successfully')
        task_dao.update_task(task_vo)
        return redirect("/modify_task")

@app.route('/task_delete', methods=['GET'])
def task_delete():
    task_vo = TaskVO()
    task_dao = TaskDAO()
    task_vo.task_id = int(request.args.get("task_id"))
    task_list = task_dao.delete_task(task_vo)
    flash('Task deleted successfully')
    return redirect("/modify_task")

@app.route('/logout', methods=['GET'])
def logout():
    response = make_response(redirect(url_for('home')))
    response.set_cookie('user_unique', value='None')
    return response

@app.route('/forget_password', methods=['GET'])
def forget_password():
    return render_template('forget_password.html')

@app.route('/change_password', methods=['POST'])
def change_password():
    login_vo = LoginVO()
    login_dao = LoginDAO()
    login_vo.login_username = request.form.get('email')
    login_vo.login_password = request.form.get('old_password')
    users = login_dao.authenticate_user(login_vo)
    final = [i.as_dict() for i in users]
    if not final:
        flash('username or password does not match')
        return redirect('/forget_password')
    else:
        login_vo.login_id = final[0]['login_id']
        login_vo.login_password = request.form.get('new_password')
        login_dao.change_password(login_vo)
        return redirect('/')

def send_mail(receiver,task_vo):
    sender = "2018ecbab003@ldce.ac.in"
    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = receiver
    msg['Subject'] = "Task Tracker"
    body = "Dear User, 'Title: "+task_vo.task_title+"' task has been created.\n Due date: "+str(task_vo.task_due_date)
    msg.attach(MIMEText(body, 'plain'))

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender, "Babariya@80584")
    text = msg.as_string()
    server.sendmail(sender, receiver, text)
    server.quit()

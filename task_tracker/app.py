from base import app

port = 5555

app.run(host='0.0.0.0',threaded=True, debug=True, port=port)

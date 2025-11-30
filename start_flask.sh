FLASK_APP=app/api.py python -m flask run --port 5000 &
echo $! > flask.pid
echo "Flask started with PID $(cat flask.pid)"
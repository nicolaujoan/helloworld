FLASK_APP=app/api.py python -m flask run --port 5000 > flask.log 2>&1 &
echo $! > flask.pid
echo "Flask started with PID $(cat flask.pid)"
echo "Output redirected to flask.log"
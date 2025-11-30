if [ -f flask.pid ]; then
    kill $(cat flask.pid)
    rm flask.pid
    echo "Flask server stopped"
else
    echo "No flask.pid file found. Flask may not be running."
fi

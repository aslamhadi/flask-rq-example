import requests
import time

from flask import Flask, jsonify, request, url_for
from tasks import count_words_at_url, add
from worker import conn

from rq import Queue
from redis import Redis

app = Flask(__name__)

@app.errorhandler(404)
def route_not_found(e):
    response = jsonify(message='Route not found', status=404)
    response.status_code = 404
    return response

@app.errorhandler(Exception)
def internal_error(exception):
    return jsonify(error_message = str(exception)), 500
    
@app.route('/')
def hello_world():
	return 'Don\'t panic! Server is running at.'

@app.route('/cassandra/export')
def test_cassandra():
    return transport_data.cassandra_to_hadoop("test_export", "test_data", "test_export", "test_export_data", 1000)

@app.route('/rq', methods=['POST'])
def cassandra_hive_tracking():
    
    q = Queue(connection=conn)

    job = q.enqueue(count_words_at_url, 'http://heroku.com')
    time.sleep(10)

    return jsonify(results = job.result)


from flask import got_request_exception

def setup_app(app):
    #setup syslog
    app.logger.addFilter(app_logging.ContextFilter())
    syslog_handler = app_logging.get_syslog_handler()
    if syslog_handler:
        app.logger.addHandler(syslog_handler)

        #send application error exception message to log
        def log_exception(sender, exception, **extra):
            sender.logger.error(exception)
        got_request_exception.connect(log_exception, app)

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=9010)

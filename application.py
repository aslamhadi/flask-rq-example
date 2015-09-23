import requests
import time

from flask import Flask, jsonify, request, url_for
from tasks import count_words_at_url, add

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
	return 'Don\'t panic! Server is running at : ' + CASSANDRA_SERVER

@app.route('/cassandra/export')
def test_cassandra():
    return transport_data.cassandra_to_hadoop("test_export", "test_data", "test_export", "test_export_data", 1000)

@app.route('/rq', methods=['POST'])
def cassandra_hive_tracking():
    
    # redis_conn = Redis(host='192.168.59.103')
    # q = Queue(connection=redis_conn)  # no args implies the default queue

    # job = q.enqueue(count_words_at_url, 'http://nvie.com')
    job = add.delay(3, 4)
    time.sleep(10)

    # job = q.enqueue_call(transport_data.cassandra_to_hadoop, 
    #     args=(cassandra_tracking_cluster, "tracking_events", hadoop_database, "tracking_events_temp", int(settings.FETCH_SIZE)),
    #     timeout=21600)

    # return jsonify(results = "resultsss")
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

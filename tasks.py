import requests
import sys

from rq.decorators import job
from redis import Redis

redis_conn = Redis(host='192.168.59.103')


def count_words_at_url(url):
    resp = requests.get(url)
    result = len(resp.text.split())
    sys.stdout.write("result : {}\n".format(result))
    return result

def add(x, y):
    return x + y
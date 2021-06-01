import os
from flask import Flask, request, jsonify
from rq import Queue
from worker import conn
from utils import scrapeMap
from datetime import datetime
import base64
import requests

app = Flask(__name__)
q = Queue(connection=conn)

def get_status(job):
    status = {
        'id': job.id,
        'result': job.result,
        'status': 'failed' if job.is_failed else 'pending' if job.result == None else 'completed'
    }
    status.update(job.meta)
    return status

@app.route("/")
def handle_job():
    query_id = request.args.get('job')
    query_name = request.args.get('name')
    query_key = request.args.get('key')
    if query_id:
        found_job = q.fetch_job(query_id)
        if found_job:
            output = get_status(found_job)
        else:
            output = { 'id': None, 'error_message': 'No job exists with the id number ' + query_id }
    elif query_name and query_key:
        if (str(base64.b64decode(query_key))[2:-1] == str(datetime.today()).split()[0]):
            res = requests.get('https://api.krunker.io/search?type=map&val=' + map_name)
            response = json.loads(res.text)
            try:
                map_id = response["data"][0]["map_id"]
                new_job = q.enqueue(scrapeMap, query_name)
                output = get_status(new_job)
            except:
                print("no map found")
                output = {'error_message': 'No map found with that name'}
        else:
            output = {'error_message': 'Failed to start due to an invalid API key'}
    elif query_name is None and query_key:
        output = {'error_message': 'No job can start without a map name'}
    elif query_key is None and query_name:
        output = {'error_message': 'No job can start without a valid API key'}
    else:
        output = {'error_message': 'No job can start without a map name and a valid API key'}
    return jsonify(output)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
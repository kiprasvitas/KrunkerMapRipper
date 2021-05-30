import os
from flask import Flask, request, jsonify
from rq import Queue
from worker import conn
from utils import scrapeMap

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
    if query_id:
        found_job = q.fetch_job(query_id)
        if found_job:
            output = get_status(found_job)
        else:
            output = { 'id': None, 'error_message': 'No job exists with the id number ' + query_id }
    elif query_name:
        new_job = q.enqueue(scrapeMap, query_name)
        output = get_status(new_job)
    else:
        output = {'error_message': 'No job can start without a map name'}
    return jsonify(output)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
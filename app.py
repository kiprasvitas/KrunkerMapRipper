import os
from flask import Flask, request, jsonify, render_template
from rq import Queue
from worker import conn
from utils import scrapeMap
from datetime import datetime
import base64
import requests
import json
from time import sleep

app = Flask(__name__)
q = Queue(connection=conn)

@app.route("/")
def handle_job():
    query_name = request.args.get('name')
    query_id = request.args.get('job')
    if query_id:
        found_job = q.fetch_job(query_id)
        if found_job:
            return 'failed' if job.is_failed else "pending" if job.result == None else found_job.result
    elif query_name:
        job = q.enqueue(scrapeMap, query_name)
        return job.id
    else:
        return "include name"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
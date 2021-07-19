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
            return 'This job has failed, please contact my support link at krunkermaps.com' if found_job.is_failed else "This job is pending. Please wait 10 seconds and refresh." if found_job.result == None else found_job.result
    elif query_name:
        job = q.enqueue(scrapeMap, query_name)
        return job.id
    else:
        return "Here's how to download any Krunker Map using this API:<br/>1. First, at the end of this url, add a '?name=' and then the name of the map you want<br/>2. You will get a job id. Make sure you copy this.<br/>3. At the end of this url, replace '?name=' with '?job=' and then the job id you were given.<br/>4. Keep on refreshing once every 10 seconds until it doesn't say 'pending' anymore<br/>5. Not all maps can be downloaded and sometimes the API can be unreliable. Both of these could cause other errors. You can always try again if it fails."

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
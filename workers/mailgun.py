#!/home/envs/fun/bin/python

import gearman
import base64
import json
import logging
import requests
import configparser

CONFIG_FILE = '/home/django/projects/fun/fun/mailgun.conf'

config = configparser.ConfigParser()
config.read(CONFIG_FILE)

worker = gearman.Worker()
worker.add_servers('127.0.0.1:4730')
logging.basicConfig(format='%(asctime)s %(message)s', filename=config.get('Global', 'log_file'), level=logging.DEBUG)


def task_emailer(job):
    logging.debug("TEST: %s" % base64.b64decode(job.workload).decode('utf-8'))
    data = json.loads(base64.b64decode(job.workload).decode('utf-8'))
    recipient_string = ",".join(data['to_address'])

    logging.info("Received mail for [" + recipient_string + "]")

    try:
        logging.info("Sending message from " + data['from_address'] + " to [" + recipient_string + "] via mailgun.com")
        requests.post(
            "https://api.mailgun.net/v3/samples.mailgun.org/messages",
            auth=("api", config.get('Global', 'api_key')),
            data={"from": data['from_address'],
                  "to": [recipient_string],
                  "subject": data['subject'],
                  "text": data['message']})
        logging.info("Done.")
    except:
        logging.error("EXCEPTION OCCURED")

    job.complete(job.workload.decode('utf-8'))

worker.add_func('emailer', task_emailer)
while True:
    worker.work()

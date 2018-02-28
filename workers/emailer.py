#!/home/envs/fun/bin/python

import gearman
import base64
import json
import smtplib
import logging
import configparser

CONFIG_FILE = '/home/django/projects/fun/fun/emailer.conf'

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
        logging.debug("Connecting to " + data['host'])
        server = smtplib.SMTP(host=data['host'])
        if data['auth_user'] is not None and data['auth_password'] is not None:
            logging.debug("Authenticating ...")
            server.login(data['auth_user'], data['auth_password'])
        logging.info("Sending message from " + data['from_address'] + " to [" + recipient_string + "] via " + data['host'])
        server.sendmail(data['from_address'], recipient_string, data['message'])
        server.quit()
        logging.info("Done.")
    except:
        logging.error("EXCEPTION OCCURED")

    job.complete(job.workload.decode('utf-8'))

worker.add_func('emailer', task_emailer)
while True:
    worker.work()

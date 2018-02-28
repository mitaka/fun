#!/usr/bin/env python

import sleekxmpp
import sys
import gearman
import base64
import json
import logging
import configparser

CONFIG_FILE = '/home/django/projects/fun/fun/jabber.conf'

config = configparser.ConfigParser()
config.read(CONFIG_FILE)

logging.basicConfig(format='%(asctime)s [JABBER] %(message)s', filename=config.get('Global', 'log_file'), level=logging.DEBUG)

if sys.version_info < (3, 0):
    from sleekxmpp.util.misc_ops import setdefaultencoding
    setdefaultencoding('utf8')
else:
    raw_input = input


class SendMsgBot(sleekxmpp.ClientXMPP):
    def __init__(self, jid, password, recipient, message):
        sleekxmpp.ClientXMPP.__init__(self, jid, password)
        self.recipient = recipient
        self.message = message

        self.add_event_handler("session_start", self.start, threaded=True)

    def start(self, event):
        self.send_presence()
        self.get_roster()
        self.send_message(mto=self.recipient, mbody=self.message, mtype='chat')
        self.disconnect(wait=True)


def task_jabber(job):
    logging.debug("TEST: %s" % base64.b64decode(job.workload).decode('utf-8'))
    data = json.loads(base64.b64decode(job.workload).decode('utf-8'))
    username = config.get('Global', 'jabber_user')
    password = config.get('Global', 'jabber_pass')

    logging.info("Received message for " + data['recipient'])

    xmpp = SendMsgBot(username, password, data['recipient'].strip(), data['message'])

    xmpp.register_plugin('xep_0030')  # Service Discovery
    xmpp.register_plugin('xep_0045')  # Multi-User Chat
    xmpp.register_plugin('xep_0071')  # HTML-IM
    xmpp.register_plugin('xep_0199')  # XMPP Ping

    if xmpp.connect():
        xmpp.process(block=True)
        message = "Message sent."
        logging.info(message)
    else:
        message = "Cannot connect to jabber server."
        logging.error(message)

    return base64.b64encode(bytes(json.dumps(message), 'utf-8'))

worker = gearman.Worker()
worker.add_servers('127.0.0.1:4730')
worker.add_func('jabber', task_jabber)

logging.info("Starting jabber worker...")

while True:
        worker.work()

#!/usr/bin/env python

import sleekxmpp
import sys
import gearman
import base64
import json
import logging
import ConfigParser

CONFIG_FILE = '/home/django/projects/fun/fun/jabber.conf'

config = ConfigParser.ConfigParser()
config.read(CONFIG_FILE)

logging.basicConfig(format='%(asctime)s %(message)s', filename=config.get('Global', 'log_file'), level=logging.DEBUG)

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


class JabberWorker(gearman.GearmanWorker):
    pass


def task_jabber(gearman_worker, job):
    data = json.loads(base64.b64decode(job.data).decode('utf-8'))
    logging.info("Data: " + base64.b64decode(job.data).decode('utf-8'))
    username = config.get('Global', 'jabber_user')
    password = config.get('Global', 'jabber_pass')

    logging.info("Received message for " + data['recipient'])

    xmpp = SendMsgBot(username, password, data['recipient'], data['message'])

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

worker = JabberWorker(['localhost:4730'])
worker.set_client_id('jabber')
worker.register_task('jabber', task_jabber)
worker.work()

from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags
from django.db.models import Q
import re
import gearman
import json
import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from django.core.exceptions import ValidationError

def send_html_mail(subject, message, from_email, recipient_list, fail_silently=False, auth_user=None, auth_password=None, connection=None):
    text_part = strip_tags(message)
    msg = EmailMultiAlternatives(subject, text_part, from_email, recipient_list)
    msg.attach_alternative(message, "text/html")
    return msg.send()

def send_gearman_mail(subject, message, from_email, recipient_list, fail_silently=False, auth_user=None, auth_password=None, host='127.0.0.1'):
    data = {}
    text = strip_tags(message)
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = from_email
    msg['To'] = ",".join(recipient_list)
    text_part = MIMEText(text, 'plain')
    html_part = MIMEText(message, 'html')
    msg.attach(text_part)
    msg.attach(html_part)

    data['host'] = host
    data['message'] = msg.as_string()
    data['subject'] = subject
    data['auth_user'] = auth_user
    data['auth_password'] = auth_password
    data['to_address'] = recipient_list
    data['from_address'] = from_email


    try:
        client = gearman.Client()
        client.add_servers('127.0.0.1:4730')
        client.do('emailer', base64.b64encode(bytes(json.dumps(data), 'utf-8')), background=True)
    except:
        raise ValidationError

def normalize_query(query_string, findterms=re.compile(r'"([^"]+)"|(\S+)').findall, normspace=re.compile(r'\s{2,}').sub):
    ''' Splits the query string in invidual keywords, getting rid of unecessary spaces
        and grouping quoted words together.
        Example:

        >>> normalize_query('  some random  words "with   quotes  " and   spaces')
        ['some', 'random', 'words', 'with quotes', 'and', 'spaces']

    '''
    return [normspace(' ', (t[0] or t[1]).strip()) for t in findterms(query_string)]

def get_query(query_string, search_fields):
    ''' Returns a query, that is a combination of Q objects. That combination
        aims to search keywords within a model by testing the given search fields.

    '''
    query = None # Query to search for every search term
    terms = normalize_query(query_string)
    for term in terms:
        or_query = None # Query to search for a given term in each field
        for field_name in search_fields:
            q = Q(**{"%s__icontains" % field_name: term})
            if or_query is None:
                or_query = q
            else:
                or_query = or_query | q
        if query is None:
            query = or_query
        else:
            query = query & or_query
    return query

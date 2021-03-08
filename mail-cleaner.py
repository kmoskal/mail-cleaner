#!/usr/bin/python3
''' Clear yours mailbox from unwanted messages '''
import imaplib
import smtplib
from email.message import EmailMessage
import os
import json
from datetime import datetime, timedelta

basedir = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(basedir, ('config.json')), 'r') as cnf:
    config = json.load(cnf)

#login to email and select default mailbox='inbox'
M = imaplib.IMAP4_SSL(config['host'])
M.login(config['login'], config['password'])
M.select()

def create_query_strings():
    ''' Create IMAP query strings from json file'''
    now = datetime.now()
    strings = []
    with open(os.path.join(basedir, ('filter.json')), 'r') as filter_json:
        filters = json.load(filter_json)
        for item in filters['to_string']:
            string = []
            for key, value in item.items():
                if key == 'BEFORE':
                    date = now - timedelta(days=int(value))
                    string.append(f'BEFORE "{date.strftime("%d-%b-%Y")}" ')
                else:
                    if isinstance(value, list): # if list create string for all elements
                        string.append(''.join(list(map(lambda value, key=key: f'{key} "{value}" ',
                            value)
                        )))
                    else:
                        string.append(f'{key} "{value}" ')
            strings.append(''.join(string))
    return strings



def delete_messages(strings):
    ''' Deletes matching messages '''
    deleted_count = 0
    report = []
    now = datetime.now()
    for string in strings:
        _, msg_uids = M.uid('search', None, string)
        count = 0
        for uid in msg_uids[0].split():
            count += 1
            M.uid('store', uid, '+FLAGS', '\\Deleted')
        if count:
            report.append(f'{now.strftime("%d-%b-%Y")} {count} messages have been deleted '
                f'from matching query: {string}.')
        deleted_count += count
    return deleted_count, report


def create_report(deleted_number, deleted_report_log):
    ''' send report to email '''
    S = smtplib.SMTP_SSL(config['host'])
    S.login(config['login'], config['password'])

    # body message must be a string for set_content
    body = ''
    for report in report_log:
        body += f'{report} \n'

    msg = EmailMessage()
    msg.set_content(body)
    msg['Subject'] = f'{deleted_number} messages have been deleted.'
    msg['From'] = config['login']
    msg['To'] = config['email']

    S.send_message(msg)
    S.quit()

    # write report to log
    with open(os.path.join(basedir, 'mc.log'), 'a') as writer:
        for report in deleted_report_log:
            writer.write('\n'+report)

deleted, report_log = delete_messages(create_query_strings())
create_report(deleted, report_log)
M.expunge()
M.close()
M.logout()

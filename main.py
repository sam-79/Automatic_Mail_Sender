import base64
import json
import os
from flask.json import jsonify
from flask.wrappers import Request
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from decouple import config
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import (
    Mail, Attachment, FileContent, FileName,
    FileType, Disposition, ContentId)
from sendgrid import SendGridAPIClient

"""
scope = ['https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('keys.json',scope)
client = gspread.authorize(creds)

sheet = client.open('sampleData').sheet1

data = sheet.get_all_records()
print(data)
values_list = sheet.col_values(2)
print(values_list)

"""

from flask import Flask, render_template, request, Response, render_template_string

app = Flask(__name__)
app.debug = True
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024
app.config['UPLOAD_EXTENSIONS'] = ['jpg', 'png', 'webp', 'jpeg', "pdf"]


# Home Page
@app.route('/')
def home():
    return render_template('index.html')


@app.route('/confirm-recipants', methods=['POST'])
def confirm_recipants():

    html = request.data.decode()

    gmail_user = 'ghostpy001@gmail.com'

    scope = ['https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name(
        'keys.json', scope)

    client = gspread.authorize(creds)

    # accessing first sheet of spreadsheet
    sheet = client.open('Employee_Data').sheet1

    data_as_list_of_dict = sheet.get_all_records()
    print(data_as_list_of_dict)

    # col_names_as_list = sheet.get_all_values()[0]
    # print(col_names_as_list)

    emails = sheet.col_values(3)[1:]
    print(emails)

    for (i, j) in zip(data_as_list_of_dict, emails):

        message = Mail(
            from_email=gmail_user,
            to_emails=j,
            subject='Notification',
            html_content=render_template_string(html, **i)
        )

        # with open('temp.txt','rb') as f:
        #     data = f.read()
        #     f.close()
        
        # encoded = base64.b64encode(data).decode()
        # attachment = Attachment()
        # attachment.file_content = FileContent(encoded)
        # attachment.file_type = FileType('text/plain')
        # attachment.file_name = FileName('temp.txt')
        # attachment.disposition = Disposition('attachment')

        # message.add_attachent = attachment


        try:
            sg = SendGridAPIClient(os.getenv('sendmail_key', config('sendmail_key')))
            response = sg.send(message)

        except Exception as exp:
            print(exp.message)


    return jsonify({'res':'DOne','res':str('Doba')})


if(__name__ == '__main__'):
    app.run()

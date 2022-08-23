import os.path
import smtplib
import pandas as pd
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from IP_Reputation.Scripts.init import *



class SendMail():
    def __init__(self, htmldata: str, email_ids: list, filepaths: list):
        user = mail_user
        password = mail_password
        default = mail_default
        subject = "IP-Reputation Automated Mail"
        if htmldata != "None":
            self.htmldata = htmldata
            self.htmldata = self.htmldata.replace('<table border="1" class="dataframe">', '<table>')
            self.htmldata = """
            <!DOCTYPE html>
            <html>
               <head>
                  <style>
                     table{
                     	border-collapse: collapse;
                        width :5rem;
                        border-radius : 10px;
                        margin : 50px auto; 
                        text-align : center;
                        box-shadow : 5px 3px 20px 1px rgba(39, 42, 107,0.3);
                        background-color : #9ED2C6
                     }

                     th{
                     font-size : 16px;
                     letter-spacing : 0.5px;
                     color : white;
                     padding: 10px;
                     background-color : #54BAB9;
                     text-align : center;
                     }


                     td{
                     padding : 8px;
                     font-size : 16px;
                     color : white;
                     border-bottom: 1px solid #54BAB9;
                     }

                  </style>
               </head>
               <body>
               %s
               <br>
               <p  style="color:#e3e2de;font-size : 6 px">
                    <hr><br>
                    This Mail Is Auto Generated
                    <br> Also To View Whole Reputation Data kindly Download The Csv File Available In Attachment.
                </p>
            </body>
            </html>
            """ % self.htmldata

        self.filepaths = filepaths
        self.email_ids = [default]
        self.email_ids.extend(email_ids)
        self.email_ids = list(set(self.email_ids))
        self.email_ids = ",".join(self.email_ids)

        MESSAGE = MIMEMultipart('alternative')
        MESSAGE['Subject'] = subject
        MESSAGE['From'] = user
        MESSAGE['To'] = self.email_ids

        for file in self.filepaths:
            if os.path.isfile(file):
                with open(file, 'rb') as f:
                    file_data = f.read()
                    filename = file.split("\\")[-1]
                attachment = MIMEApplication(file_data)
                attachment['content-Disposition'] = 'attachment; filename = {}'.format(filename)
                MESSAGE.attach(attachment)
        if htmldata != 'None':
            MESSAGE.attach(MIMEText(self.htmldata, 'html'))

        server = smtplib.SMTP_SSL(mail_smtp, 465)
        server.login(user=user, password=password)
        server.send_message(MESSAGE)
        server.quit()
        print("Mail Has Been Sent")



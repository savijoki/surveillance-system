#!/usr/bin/env python
# -*- coding: utf-8 -*-

import smtplib
import getpass
import re
import os
import datetime
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart

class MailHandler:

    def __init__(self, recipient):
        
        self.username, self.password = self.login_info(True)
        self.recipient = recipient
        self.server_type = self.smtp_server_type()
        self.server = None

    # Gather user's login info
    def login_info(self, notifications=None):

        email_user = None
        email_pwd = None

        while True:
            if notifications == None:
                use_email = raw_input(
                    "Do you wish to use email notifications? [Y/n]").strip()
            if notifications or use_email == '' or use_email.lower() == 'y':
                print(
                    "[INFO] Using email notifications. Supported servers are outlook and gmail.")
                email_user = raw_input("Enter username: ").strip()
                email_pwd = getpass.getpass(prompt='Enter password: ')
                break
            elif not notifications or use_email.lower() == 'n':
                break
            else:
                print("Please respond with 'y' or 'n'.")

        return email_user, email_pwd


    # Define what smtp-server to use (outlook or gmail)
    def smtp_server_type(self):

        user = self.username
        hotmail = "(.*?@hotmail.com)"

        # Doesn't want emails
        if not user:
            return None
        # Hotmail users match this pattern
        elif re.match(hotmail, user):
            print("[INFO] User is sending through hotmail smtp-server!")
            return "hotmail"
        # Gmail users
        else:
            print("[INFO] User is sending through gmail smtp-server!")
            return "gmail"

    def validate_login(self):

        server_type = self.server_type

        while server_type:

            valid_smtp_server = self.check_server()

            # If not None, server is good to go
            if valid_smtp_server:
                print("[INFO] Login success! We have a valid smtp server!")
                break
            print("Please re-enter the login credentials for email.")
            self.username, self.password = self.login_info(True)
            server_type = self.smtp_server_type()
        self.server = valid_smtp_server

    # Validate login info
    def check_server(self):

        username = self.username
        password = self.password
        server_type = self.server_type

        if server_type == "hotmail":
            server = smtplib.SMTP('smtp.live.com', 587)
        else:
            server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.ehlo()
        try:
            server.login(username, password)
        except smtplib.SMTPException:
            print("[ERROR] Login failed, username or password isn't correct!")
            return None

        return server

    # # Shutdown smtp server
    # def shutdown(self):

    #     self.server.quit()
    #     self.server = None

    # Construct email message
    def construct_message(self, path):

        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        img_data = open(path, 'rb')
        file_type = 'Video' if re.match(".*?.avi$", path) else 'Image'
        file_size = os.path.getsize(path)
        msg = MIMEMultipart()
        textMessage = "Hello!\n\nPicture was taken with security camera. " \
            "See the details of the picture below.\n\n\nTime: %s\nType: %s\n" \
            "Size: %s Bytes\n\n\nImage is in the attachments!\n\n\n" \
            "This message was sent automatically through sec-cam application." % (
                now, file_type, file_size)
        text = MIMEText(textMessage)
        msg.attach(text)
        image = MIMEImage(img_data.read())
        msg.attach(image)
        msg['Subject'] = 'Activity in security camera!'
        return msg


    # Send email to user, path gives the path to attachment (photo)
    def send_mail(self, path):

        server = self.server
        msg = self.construct_message(path)
        server.sendmail(self.username, self.recipient, msg.as_string())
        print("[INFO] Email sent successfully!")

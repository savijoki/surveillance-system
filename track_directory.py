#!/usr/bin/env python
# -*- coding: utf-8 -*-

from watchdog.events import PatternMatchingEventHandler


# Class to track newly created files in path
class DirectoryEvents:

    def __init__(self, path, mailer):

        self.path = path
        self.event_handler = PatternMatchingEventHandler(
            patterns=["*.jpg", "*.avi"])
        self.event_handler.on_created = self.process
        self.mailer = mailer

    def dispatch(self, event):
        self.process(event)

    def process(self, event):

        mailer = self.mailer

        # If there's a valid smtp-server, send email through it
        if mailer.server:
            print("[INFO] Sending mail to recipient...")
            mailer.send_mail(event.src_path)

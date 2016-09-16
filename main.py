#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import json
import sys
import time
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
import cloud_integration
from track_directory import DirectoryEvents
from mail import MailHandler
import motion


# Read the configuration file
def get_conf():

    # Construct the argument parser and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-c", "--conf", required=True, help="path to the JSON"
                    "configuration file")
    args = vars(ap.parse_args())
    conf = {}

    # Load the configuration
    try:
        conf = json.load(open(args["conf"]))
    except IOError, error:
        print("[ERROR] Configuration file not found!")
        return None

    return conf


def main():

    conf = get_conf()

    if not conf:
        sys.exit(0)

    print("[INFO] Starting cloud integration...")
    dropbox_client = cloud_integration.connect_dropbox(conf)
    print("[INFO] Checking media directory path...")
    media_dir = motion.motion_directory(conf)

    if not media_dir:
        sys.exit(0)

    # Emails are handled in MailHandler-class
    mailer = MailHandler(conf["send_mail_to"])
    mailer.validate_login()

    print("[INFO] Starting motion...")
    time.sleep(2)
    # Starting the process
    start = subprocess.call(['sudo', 'service', 'motion', 'start'])

    # Set the watchdog to track directory's events
    event_handler = DirectoryEvents(media_dir, mailer)
    observer = Observer()
    observer.schedule(event_handler.event_handler, path=media_dir)
    observer.start()

    # Start looping and waiting for images to pop in the folder and trigger
    # events
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n[INFO] Closing program...")

        # Close motion and watchdog
        motion = subprocess.call(['sudo', 'service', 'motion', 'stop'])
        observer.stop()

        if mailer.server:
            print("[INFO] Closing the smtp-server...")
            mailer.server.quit()

    observer.join()

if __name__ == '__main__':
    main()

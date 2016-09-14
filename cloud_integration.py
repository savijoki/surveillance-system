#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Dropbox imports for auth
from dropbox.client import DropboxOAuth2FlowNoRedirect
from dropbox.client import DropboxClient


def connectDropbox(conf):

    # If dropbox_key is not set, stop program and give informative print to
    # user
    if conf["dropbox_key"] != "APP_KEY" or conf["dropbox_secret"] != "SECRET":
        # connect to dropbox and start the session authorization process
        print "[INFO] Start authorizing application from Dropbox..."
        flow = DropboxOAuth2FlowNoRedirect(
            conf["dropbox_key"], conf["dropbox_secret"])
        print "[INFO] Authorizing application using link below:\n{}\n".format(flow.start())
        authCode = raw_input("Enter auth code here: ").strip()
        # # finish the authorization and grab the Dropbox client
        (accessToken, userID) = flow.finish(authCode)
        client = DropboxClient(accessToken)
        print "[SUCCESS] dropbox account linked"
        print '[INFO] Linked account: ', client.account_info()["display_name"]
        return client
    else:
        print "[ERROR] Add your dropbox information to conf.json!"
        return None

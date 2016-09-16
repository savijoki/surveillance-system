#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Check if media directory is set
def motion_directory(conf):

    media_dir = None

    # Check if media directory's path is set in conf.json
    if conf["motion_media_dir"] != "PATH_TO_DIR":
        media_dir = conf["motion_media_dir"]
        print "[INFO] Media directory is set: {}".format(media_dir)
    else:
        print "[ERROR] Add media directory's absolute path to conf.json!"

    return media_dir

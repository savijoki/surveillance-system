#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import json
import sys

import cloud_integration
import motion

def readConf():
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
        print "[ERROR] Configuration file not found!"
        return None
	
    return conf


def run():

    conf = readConf()
    
    if not conf:
        sys.exit(0)

    print "[INFO] Starting cloud integration..."
    dropbox_client = cloud_integration.connectDropbox(conf)
    
    print "[INFO] Checking media directory path..."
    media_dir = motion.motionDirectory(conf)
    
    if not media_dir:
        sys.exit(0)
    

if __name__ == '__main__':
    run()

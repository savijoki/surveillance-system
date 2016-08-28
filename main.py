#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import json

import cloud_integration

def readConf():
    # Construct the argument parser and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-c", "--conf", required=True, help="path to the JSON"
        "configuration file")
    args = vars(ap.parse_args())

    # Load the configuration
    conf = json.load(open(args["conf"]))
	
    return conf


def run():
    conf = readConf()

    dropbox_client = cloud_integration.connectDropbox(conf)



if __name__ == '__main__':
    run()

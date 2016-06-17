#!/usr/bin/env python
#-*- coding: UTF-8 -*-

import time

def log(message, path):
    log_path_basic = 'log/'
    f = open(log_path_basic + path, 'a')
    f.write('\n----------------- %s -----------------\n' % (time.ctime()))
    f.write(message + '\n')
    f.close()

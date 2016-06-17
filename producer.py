#!/usr/bin/env python
#-*- coding: UTF-8 -*-

from include.queue import rabbit
from include.helper import log
import json
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash
import sys

# set encoding
reload(sys)
sys.setdefaultencoding('utf-8')


# system config
DEBUG = True
# create our little application
app = Flask(__name__)
app.config.from_object(__name__)

# route
@app.route('/nsis', methods = ['POST'])

def down():
    id = int(request.form.get('id', ''))
    title = request.form.get('title', '')
    name = request.form.get('name', '')
    path = request.form.get('path', '')
    site = request.form.get('site', '')

    # validata
    if not isinstance(id, int):
        abort(400 , 'id必须为整数!')
    if (not title) or (not name) or (not path)or (not site):
        abort(400 , '参数不能为空!')

    data = {"id":id,"title":title,"name":name,"path":path,"site":site}
    q = rabbit()
    r, message = q.producer(json.dumps(data, ensure_ascii=False))

    if not r:
        path = 'consummer_error.log'
        log('意外错误：' + message, path)
        abort(500, '任务推送失败!')

    return 'success'

# run
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8088)

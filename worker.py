#!/usr/bin/env python
#-*- coding: UTF-8 -*-

from include.queue import rabbit
from include.helper import log
from include.config import get_config
from subprocess import check_output
from datetime import datetime
import json
import codecs
import os
import sys

# set encoding
reload(sys)
sys.setdefaultencoding('utf-8')
# get config
config = get_config()


def main():
    global config
    q = rabbit(config['rabbit'])
    q.consumer(callback)

def callback(ch, method, properties, body):   
    global config

    ms = ()   
    try:
        ms = json.loads(body)
    except Exception,e:
        log('JSON解析错误:' + body + '\n' + Exception + ': ' + e, 'consummer_error.log')

    if ms:
        try:
            nsi_path = config['common']['nsi_path']
            temp_path = config['common']['temp_path'] % ms['name']

            output_path = config['common']['output_path'] % ms['path']
            if not os.path.exists(output_path):
                os.makedirs(output_path)

            basic_down = config['common']['basic_down']

            replacements = {
                '${TITLE}':ms['title'],
                '${NAME}':ms['name'],
                '${ID}':str(ms['id']),
                '${INPUT}':basic_down + '\\' + ms['path'],
                '${SITE}':ms['site'],
                '${OUTDIR}':output_path,
                '${YEAR}':str(datetime.now().year),
                '${MONTH}':str(datetime.now().month),
                '${DAY}':str(datetime.now().day)
            }

            # 读取原始脚本
            f = codecs.open(nsi_path, encoding='GBK')
            content = f.read()
            f.close()
            # 替换原始脚本变量参数
            for src, target in replacements.iteritems():
                content = content.replace(src, target)
            # 写入临时脚本
            f = codecs.open(temp_path, 'w', encoding='GBK')
            f.write(content)
            f.close()        

            # 执行打包命令
            r = check_output(config['common']['command'] + temp_path, shell=True)

            # 删除临时脚本
            os.remove(temp_path)

            log(body + '\n' + r, 'compile.log')
        except Exception,e:
            log('命令执行错误:\n' + e + '\n' + body + '\n' + Exception + ': ' + e, 'consummer_error.log')


if __name__ == "__main__":
    main()

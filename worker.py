#!/usr/bin/env python
#-*- coding: UTF-8 -*-

from include.queue import rabbit
from include.helper import log
from subprocess import check_output
from datetime import datetime
import json
import codecs
import os
import sys

# set encoding
reload(sys)
sys.setdefaultencoding('utf-8')

def main():
    q = rabbit()
    q.consumer(callback)

def callback(ch, method, properties, body):    
    ms = ()   
    try:
        ms = json.loads(body)
    except Exception,e:
        log('JSON解析错误:' + body, 'consummer_error.log')

    if ms:
        try:
            nsi_path = 'D:\\nsis\\nsis\\nsi\pc6\\template.nsi'
            temp_path = 'D:\\nsis\\nsis\\nsi\pc6\\' + ms['name'] + '.nsi'

            output_path = 'D:\\nsis\\packaged\\' + ms['path']
            if not os.path.exists(output_path):
                os.makedirs(output_path)

            basic_down = 'D:\\nsis\\download'

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

            f = codecs.open(nsi_path, encoding='GBK')
            content = f.read()
            f.close()
            
            for src, target in replacements.iteritems():
                content = content.replace(src, target)

            f = codecs.open(temp_path, 'w', encoding='GBK')
            f.write(content)
            f.close()        

            r = check_output("D: & cd D:\\nsis\\nsis\\nsi\pc6 & D:\\nsis\\nsis\makensis.exe " + temp_path, shell=True)
            log(body + '\n' + r, 'compile.log')
        except Exception,e:
            log('命令执行错误:\n' + e + '\n' + body, 'consummer_error.log')


if __name__ == "__main__":
    main()

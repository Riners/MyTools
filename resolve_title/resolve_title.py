#!/usr/bin/env python
# -*- coding:UTF-8 -*-
from urllib import request, error
from bs4 import BeautifulSoup
urls = open('website.txt','r')
File = open('Result.txt','w+')
def log(s):
    File.write(s+'\n')
def main():
    seq = 0
    seq2 = 0
    for line in urls:
        seq += 1
        try:
            html = request.urlopen("http://" + line,timeout=3)
            html_doc = html.read()
            soup = BeautifulSoup(html_doc, 'html.parser')
            s = soup.title.string
            result = ('%d  %s \t %5s' % (seq, line.strip(), s))
            print(result)
            log(result)
        except error.URLError:
            seq2 += 1
            l = ('%d  %s  \t  Error:URL Open Error' % (seq, line.strip()))
            print(l)
            log(l)
    z = ("Success: %d\nFailed: %d\nTotal: %d" %(seq-seq2,seq2,seq))
    print(z)
    log(z)
    urls.close()
    File.close()
if __name__=='__main__':
    main()
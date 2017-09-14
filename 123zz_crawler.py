# -*- coding: utf-8 -*-

'''
1) Written by 細胞變大包(LIHKG) on 14-Sep-2017 (UTC+02:00)
2) I make no representations or warranties of any kind concerning the safety, suitability, lack of viruses,
inaccuracies, typographical errors, or other harmful components of this programe.
3) Have fun :)
'''

import sys, io, os, timeit
import urllib2
from bs4 import BeautifulSoup

argv = sys.argv
encoding = 'utf-8'

if len(argv) < 2:
    argv.append(0)
    argv.append(2000)
    argv.append('http://123zz.com')
elif len(argv) < 3:
    if not argv[1].isdigit():
        raise Exception('Usage: python 123zz_crawler.py [start page no.] [end page no.] [url]')
    argv[1] = int(argv[1])
    argv.append(argv[1]+2000)
    argv.append('http://123zz.com')
if len(argv) < 4:
    if not argv[1].isdigit() or not argv[2].isdigit():
        raise Exception('Usage: python 123zz_crawler.py [start page no.] [end page no.] [url]')
    argv[1] = int(argv[1])
    argv[2] = int(argv[2])
    if argv[1] > argv[2]:
        argv[1] , argv[2] = argv[2] , argv[1]
    argv.append('http://123zz.com')
# print(argv)

try:
    fid = io.open('database.txt', 'r', encoding=encoding)
    for last in fid: pass
    last = last.split(',')
    if last[0].isdigit():
        argv[1] = int(last[0]) + 1
    fid.close()
except:
    fid = io.open('database.txt', 'w', encoding=encoding)
    fid.write(u'檔案編號,刊登日期,中文名,英文名,欠款,所屬地區,公司,職業,住址,欠款財務公司,最後上班,狀態,備註,破產XX時間,私人欠債\n')
    fid.close()

if not os.path.exists('./photo'):
    os.makedirs('./photo')

fid = io.open('database.txt', 'a', encoding=encoding)
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:55.0) Gecko/20100101 Firefox/55.0'}
counter = 0
tic = timeit.default_timer()

for ii in range(argv[1], argv[2]+1):
    url = argv[3] + '/case/' + str(ii)
    entry = {u'檔案編號': '',
             u'刊登日期': '',
             u'中文名': '',
             u'英文名': '',
             u'欠款': '',
             u'所屬地區': '',
             u'公司': '',
             u'職業': '',
             u'住址': '',
             u'欠款財務公司': '',
             u'最後上班': '',
             u'狀態': '',
             u'備註': '',
             u'破產XX時間': '',
             u'私人欠債': ''}
    request = urllib2.Request(url, None, headers)
    response = urllib2.urlopen(request)
    soup = BeautifulSoup(response.read(), 'lxml')
    container = soup.html.body.find_all('div', attrs={'class':'container'})[1]

    img = container.find('div', attrs={'class':'thumbnail'}).find('img')
    if img is None:
        continue
    elif img['src'] == '/img/success.jpg':
        continue
    else:
        img_url = argv[3] + img['src']

    amount = container.find('span', attrs={'class': 'text-red-pantone lead'})
    amount = amount.string.replace(' ', '').replace(',', '').replace(u'港幣', '').replace(u'元', '')

    table = container.find('div', attrs={'class': 'panel panel-primary'}).find('div', attrs={'class': 'panel-body'})
    key = table.find_all('dt')
    value = table.find_all('dd')
    for jj in range(len(key)):
        key_ = key[jj].string
        try:
            value_ = value[jj].string.replace(',', '')
        except:
            value_ = ''
        entry[key_] += value_

    date = container.find('span', attrs={'class': 'pull-right text-red-pantone'})
    date = date.string.replace(' ', '').replace(u'刊登日期：', '')

    # create output string
    entry[u'檔案編號'] = str(ii)
    entry[u'刊登日期'] = date
    entry[u'欠款'] = amount
    output = ','.join([entry[u'檔案編號'], entry[u'刊登日期'], entry[u'中文名'], entry[u'英文名'],
                       entry[u'欠款'], entry[u'所屬地區'], entry[u'公司'], entry[u'職業'],
                       entry[u'住址'], entry[u'欠款財務公司'], entry[u'最後上班'], entry[u'狀態'],
                       entry[u'備註'], entry[u'破產XX時間'], entry[u'私人欠債']])

    # write to file & download photo
    with io.open('./photo/' + '_'.join([str(ii), entry[u'中文名'].replace('/', ''), entry[u'英文名']]).replace('/', '') + '.jpeg', 'wb') as image:
        image.write(urllib2.urlopen(urllib2.Request(img_url, None, headers)).read())
    fid.write(output + '\n')
    counter += 1

fid.close()
toc = timeit.default_timer()
print('%d entries downloaded (%.2f sec)' % (counter, toc - tic))

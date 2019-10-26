#!/usr/bin/python3
import os
import re
import requests
import subprocess

URLS=[
    ('remainunited',
        'https://www.remainunited.org/',
        re.compile('<meta name="csrf-token" content="[^"]+" />')),
    ('peoplesvote',
        'https://www.tactical-vote.uk/',
        re.compile('<meta name="csrf-token" content="[^"]+" />')),
    ('tacvote',
        'https://tactical.vote/',
        re.compile('^')),
    ('bestforbritain',
        'https://www.bestforbritain.org/getvoting',
        re.compile('|'.join([
            'default|mobile',
            '<div class="columns-1-flash">[\s\s]*?</div>',
            '<meta content="[^"]+" name="csrf-token" />',
            'window._auth_token = "[^"]+";',
            '<input name="authenticity_token" type="hidden" value="[^"]+"/>']))),
    ('unitetoremain',
        'https://unitetoremain.org/',
        re.compile('^')),
]

PATH='./urlchecks/'
UA='Mozilla/5.0 (Linux; Android 7.0; SM-G930V Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.125 Mobile Safari/537.36'
HEADERS={'User-Agent': UA}

def main():
    for fname, url, regex in URLS:
        page = requests.get(url, headers=HEADERS).text
        page = regex.sub('', page)
        diffcheck(PATH + fname, page)


def diffcheck(fname, page):
    old_fname = fname + "-old"
    os.rename(fname, old_fname)
    with open(fname, 'w', encoding='utf8') as f:
        f.write(page)
    subprocess.check_call(['diff', '-u', old_fname, fname])

if __name__ == '__main__':
    main()

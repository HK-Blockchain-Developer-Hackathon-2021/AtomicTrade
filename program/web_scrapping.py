from __future__ import division, unicode_literals 
import codecs
from bs4 import BeautifulSoup
import hashlib
import sys


html_file=""
html_file+=sys.argv[1]
htdoc = html_file[1:]
f=codecs.open(htdoc, 'r', 'utf-8')
document= BeautifulSoup(f.read(), "html.parser").get_text()
print(hashlib.sha256(document.encode()).hexdigest())

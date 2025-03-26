import requests

r=requests.get('http://www.jd.com')
r.encoding
print(r.text[:1000])

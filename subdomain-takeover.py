import requests

url="http://fan.football.sony.net/"
r=requests.get(url)

with open("jetsub.txt", "r") as ins:
    for url in ins:
	url="http://"+url[:-1]
	print url
	try:
      		r=requests.get(url,timeout=5)
	except:
		print "timeout"
	print r.status_code

	payload="pointed at WP Engine"
	payload2="heroku"
	if(payload in r.text or payload2 in r.text):
		print "Well we found one => " ,url



import requests
import sys
import os	
import subprocess
import sublist3r 
import argparse
class bcolors:
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERL = '\033[4m'
    ENDC = '\033[0m'
    backBlack = '\033[40m'
    backRed = '\033[41m'
    backGreen = '\033[42m'
    backYellow = '\033[43m'
    backBlue = '\033[44m'
    backMagenta = '\033[45m'
    backCyan = '\033[46m'
    backWhite = '\033[47m'

parser = argparse.ArgumentParser(description='Tool Arguments')

parser.add_argument('-f','--file', type=argparse.FileType('r'),help='File name')

parser.add_argument('-d', '--domain',dest='domain',help='domain name', required=False)
args = parser.parse_args()
domainname=args.domain

if args.file:

	file_name = args.file.name
	payload_list=["This domain is successfully pointed at WP Engine","NoSuchBucket","No such app","There isn't a GitHub Page here.","You're Almost There...","no-such-app","There's nothing here.","Sorry, this shop is currently unavailable.","The site you were looking for couldn't be found."]
	responses=[]
	query_urls=[]
	file_output_content=""

	with open(file_name, "r") as ins:
		number_of_urls  = sum(1 for line in open(file_name))
		cnt=1
		for url in ins:
			print  bcolors.BLUE +"[-] Scanning URL ("+ str(cnt)+"/"+str(number_of_urls)+")  "+url[:-1]+ bcolors.ENDC 
			response="failed"
			query_urls.append(url[:-1])
			p = subprocess.Popen('nslookup '+url+' 8.8.8.8', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
	
			result = p.communicate()[0]
			for line in result.split('\n'):
				if("canonical name" in line):
					query_urls.append(line[line.index('canonical name')+17:])
					line[line.index('canonical name')+14:-1]
			
			i=0
			for url in query_urls:
				url="http://"+url
				try:
			      		r=requests.get(url,timeout=10)
					response=r.text
					isFound=False
					for payload in payload_list:
						if(payload in response):
							isFound=True
					if(isFound and i>0):
						print bcolors.GREEN + "Well we may have found one => CNAME" ,query_urls[i], bcolors.ENDC
						print bcolors.YELLOW + "Original URL" , query_urls[0],bcolors.ENDC
						file_output_content=file_output_content+"possible CNAME URL : "+query_urls[i]+"\n"
						file_output_content=file_output_content+"original URL : " + query_urls[0]+"\n"
					elif(isFound):
						print bcolors.GREEN + "Well we may have found one => " ,query_urls[i], bcolors.ENDC 
						file_output_content=file_output_content+"possible URL : "+query_urls[i]+"\n"
					i+=1

				except:
					continue
					#print bcolors.YELLOW + url +" => timeout" + bcolors.ENDC
	
	
			responses=[]	
			query_urls=[]
			cnt+=1
		with open(file_name+"_attackresults.txt","w") as f:
			f.write(file_output_content)

		print bcolors.BLUE +"Possible URLs are written to : " +sys.argv[1]+ "_attackresults.txt" + bcolors.ENDC 

elif args.domain:
	domain=args.domain
	file_name=domain+".txt"
	subdomains = sublist3r.main(domain, 40, file_name, ports= None, silent=False, verbose= False, enable_bruteforce= False, engines=None)

	payload_list=["This domain is successfully pointed at WP Engine","NoSuchBucket","No such app","There isn't a GitHub Page here.","You're Almost There...","no-such-app","There's nothing here.","Sorry, this shop is currently unavailable.","The site you were looking for couldn't be found."]
	responses=[]
	query_urls=[]
	file_output_content=""

	with open(file_name, "r") as ins:
		number_of_urls = len(subdomains)
		cnt=1
		for url in ins:
			print  bcolors.BLUE +"[-] Scanning URL ("+ str(cnt)+"/"+str(number_of_urls)+")  "+url[:-1]+ bcolors.ENDC 
			response="failed"
			query_urls.append(url[:-1])
			p = subprocess.Popen('nslookup '+url+' 8.8.8.8', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
	
			result = p.communicate()[0]
			for line in result.split('\n'):
				if("canonical name" in line):
					query_urls.append(line[line.index('canonical name')+17:])
					line[line.index('canonical name')+14:-1]
			
			i=0
			for url in query_urls:
				url="http://"+url
				try:
			      		r=requests.get(url,timeout=10)
					response=r.text
					isFound=False
					for payload in payload_list:
						if(payload in response):
							isFound=True
					if(isFound and i>0):
						print bcolors.GREEN + "Well we may have found one => CNAME" ,query_urls[i], bcolors.ENDC
						print bcolors.YELLOW + "Original URL" , query_urls[0],bcolors.ENDC
						file_output_content=file_output_content+"possible CNAME URL : "+query_urls[i]+"\n"
						file_output_content=file_output_content+"original URL : " + query_urls[0]+"\n"
					elif(isFound):
						print bcolors.GREEN + "Well we may have found one => " ,query_urls[i], bcolors.ENDC 
						file_output_content=file_output_content+"possible URL : "+query_urls[i]+"\n"
					i+=1

				except:
					continue
					#print bcolors.YELLOW + url +" => timeout" + bcolors.ENDC
	
	
			responses=[]	
			query_urls=[]
			cnt+=1
		with open(file_name+"_attackresults.txt","w") as f:
			f.write(file_output_content)

		print bcolors.BLUE +"Possible URLs are written to : " +sys.argv[1]+ "_attackresults.txt" + bcolors.ENDC 

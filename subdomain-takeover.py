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
	
def write_to_file(file_name,content):
	with open(file_name+"_attackresults.txt","w") as f:
		f.write(content)
	print bcolors.BLUE +"Possible URLs are written to : " +file_name+ "_attackresults.txt" + bcolors.ENDC 

parser = argparse.ArgumentParser(description='Tool Arguments')

parser.add_argument('-f','--file', type=argparse.FileType('r'),help='File name')

parser.add_argument('-d', '--domain',dest='domain',help='domain name', required=False)
args = parser.parse_args()
domainname=args.domain

payload_dict={}
payload_dict["This domain is successfully pointed at WP Engine"]="WPEngine"
payload_dict["NoSuchBucket"]="AWS"
payload_dict["No such app"]="Heroku"
payload_dict["There isn't a GitHub Page here."]="Github"
payload_dict["You're Almost There"]="SquareSpace"
payload_dict["no-such-app"]="Heroku"
payload_dict["Sorry, this shop is currently unavailable"]="Shopify"
payload_dict["The site you were looking for couldn't be found"]="WPEngine"
payload_dict["No Such Account"]="SquareSpace"
payload_dict["The request could not be satisfied"]="Cloudfront"


if args.file:

	file_name = args.file.name
	payload_list=["This domain is successfully pointed at WP Engine","NoSuchBucket","No such app","There isn't a GitHub Page here.","You're Almost There...","no-such-app","There's nothing here.","Sorry, this shop is currently unavailable.","The site you were looking for couldn't be found."]
	responses=[]
	query_urls=[]
	file_output_content="Results \n"

	with open(file_name, "r") as ins:
		number_of_urls  = sum(1 for line in open(file_name))
		cnt=1
		try:
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
				      		r=requests.get(url,timeout=6)
						response=r.text
						isFound=False
						for payload in payload_dict:
							if(payload in response):
								service=payload_dict[payload]
								isFound=True
						if(isFound and i>0):
							print bcolors.GREEN + "Well we may have found one => CNAME" ,query_urls[i], "  Service ", service, bcolors.ENDC
							print bcolors.YELLOW + "Original URL" , query_urls[0],bcolors.ENDC
							file_output_content=file_output_content+"possible CNAME URL : "+query_urls[i]+"  Service "+ service+"\n"
							file_output_content=file_output_content+"original URL : " + query_urls[0]+"\n"
						elif(isFound):
							print bcolors.GREEN + "Well we may have found one => " ,query_urls[i], "  Service ", service,  bcolors.ENDC 
							file_output_content=file_output_content+"possible URL : "+query_urls[i]+"  Service "+ service+"\n"
						i+=1

					except:
						continue
						#print bcolors.YELLOW + url +" => timeout" + bcolors.ENDC
	
	
				responses=[]	
				query_urls=[]
				cnt+=1
			write_to_file(file_name,file_output_content)

		except KeyboardInterrupt:
			write_to_file(file_name,file_output_content)



elif args.domain:
	domain=args.domain
	file_name=domain+".txt"
	subdomains = sublist3r.main(domain, 40, file_name, ports= None, silent=False, verbose= False, enable_bruteforce= False, engines=None)
	responses=[]
	query_urls=[]
	file_output_content="Results \n"
	service=""
	with open(file_name, "r") as ins:
		number_of_urls = len(subdomains)
		cnt=1
		try:
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
				      		r=requests.get(url,timeout=6)
						response=r.text
						isFound=False
						for payload in payload_dict:
							if(payload in response):
								service=payload_dict[payload]
								isFound=True
						if(isFound and i>0):
							print bcolors.GREEN + "Well we may have found one => CNAME" ,query_urls[i], "  Service ", service, bcolors.ENDC
							print bcolors.YELLOW + "Original URL" , query_urls[0],bcolors.ENDC
							file_output_content=file_output_content+"possible CNAME URL : "+query_urls[i]+"  Service "+ service+"\n"
							file_output_content=file_output_content+"original URL : " + query_urls[0],"\n"
						elif(isFound):
							print bcolors.GREEN + "Well we may have found one => " ,query_urls[i], "  Service ", service,  bcolors.ENDC 
							file_output_content=file_output_content+"possible URL : "+query_urls[i]+"  Service "+ service+"\n"
						i+=1

					except:
						continue
						#print bcolors.YELLOW + url +" => timeout" + bcolors.ENDC
	
	
				responses=[]	
				query_urls=[]
				cnt+=1
			write_to_file(file_name,file_output_content)
		except KeyboardInterrupt:
     			write_to_file(file_name,file_output_content)
		

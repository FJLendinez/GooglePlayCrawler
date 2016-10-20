import os, sys
from PlayStoreCrawler.PlayStoreCrawler import MainProcess 

if(len(sys.argv)>1):
	if(sys.argv[1] == "-c"):
		print "cleaning previous results"
		top ="./Results"
		for root, dirs, files in os.walk(top, topdown=False):
    			for name in files:
				print "removing " + name + " file."
        			os.remove(os.path.join(root, name))
    			for name in dirs:
				print "removing " + name + " dir."
        			os.rmdir(os.path.join(root, name))
appsRoute =  os.getcwd() +"/apps"
apps = open(appsRoute,'r').read()
apps = apps.split("\n")[:-1]

for app in apps:
	print app
	MainProcess(app)

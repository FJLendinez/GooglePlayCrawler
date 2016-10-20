#!/usr/bin/python
# coding: utf-8 

from selenium import webdriver
from time import sleep
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import UnexpectedAlertPresentException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from Utils import *
import traceback, time

#This crawler actually print the comments with his related information about a given link of the Android Play Store
#It is so easy to use. Just use the command:
#	$python PlayStoreCrawler.py <link>
#Author:Francisco Javier Lendinez Tirado


#Open a Firefox window with the address given
def chargeDriver(address):
	#If you want to use Chrome, uncomment this following line
	Driver = webdriver.Chrome("/path/to/chrome/driver")
	
	#If you want to use Firefox with a personal configuration, uncomment this block
	#fp = webdriver.FirefoxProfile()
	#fp.set_preference("dom.max_chrome_script_run_time", 0)
	#fp.set_preference("dom.max_script_run_time", 0)
	#Driver = webdriver.Firefox(firefox_profile=fp)
	
	print address
	Driver.get(address)
	return Driver



#Find the element of the review
def findCommentInfo(rev, info):
	revInfo = rev.find_element_by_class_name(info)
	if(revInfo.is_displayed()):
		return revInfo
	else:
		return None

#Find and store the comments
def extractComments(Driver,File, AppName, Category, lang):
	
	#Create a dictionary
	DictRate = createDictRate(lang)
	#Init some vars
	stillComment = True
	Contador = 0
	#Loop of comments
	while(stillComment):
		try:
			start_general_time = time.time()
			WritterPermission = True
			stillComment = False
			#Get the expand-button
			Driver.implicitly_wait(0)
			elmts = Driver.find_elements_by_xpath("//button[contains(@class,'expand-next') and not(contains(@style,'display: none'))]")
			time.sleep(1)
			
			#Move and clicking
			for elem in elmts:
				stillComment = True
				elem.click()
				if lang == "en":
					print "Button clicked"
				else:
					print "Botón clickeado"
			#__________________________________

			#If there are not more comment, it breaks the loop and go out
			if not stillComment:
				break
			
			#Sistema de recuperación: Parte 2
			sleep(1)
			reviews = Driver.find_elements_by_xpath("//div[contains(@class,'expand-page') and contains(@style,'opacity: 1')]//div[contains(@class, 'single-review')]")
			#__________________________________

			start_time = time.time()
			#For each review
			for rev in reviews:
				text = ""
				#Header info
				revHeader = findCommentInfo(rev,"review-info")
				if revHeader is not None:
					Contador += 1
					RevDetails = revHeader.text
					SplitPoint = findSplitPoint(RevDetails, lang)
					RevDate = RevDetails[SplitPoint:len(RevDetails)].strip()
					RevNick = RevDetails[0:SplitPoint-1].strip()
					text += str(Contador)+"\t"+AppName+"\t"+Category+"\t"+RevNick+"\t"+RevDate+"\t"
				#Rates
				revRate = findCommentInfo(rev,"star-rating-non-editable-container")
				if revRate is not None:
					rate = revRate.get_attribute("aria-label").encode("utf-8").strip()
					WritterPermission = countRates(DictRate,rate)
					text +=str(rate[12])+"\t"
				#Text
				revText = findCommentInfo(rev,"review-body")
				if revText is not None:
					text +=revText.text+"\n"
				#Check final conditions to save or exit
				if(IsFinished(DictRate)):
					stillComment = False	
				if WritterPermission:
					ShowInfo(DictRate, start_general_time, lang)
					File.write(text.encode("utf-8"))
				else:
					print "Cap in comments"
			if(lang=="es"):
				print "Guardar " + str(len(reviews)) + " ficheros ha llevado " + str(time.time() - start_time)
			else:
				print "To save " + str(len(reviews)) + " files it takes " + str(time.time() - start_time)
		except UnexpectedAlertPresentException as UAPE:
			alert = Driver.switch_to_alert().accept()

#Execute all the functions
def MainProcess(address):
	try:
		name = ""
		Driver = chargeDriver(address)
		name = Driver.find_element_by_class_name("id-app-title").text
		print name
		cat = Driver.find_element_by_class_name("category").text
		print cat
		CSVFile = createCSV(name,cat)
		lang = address[-2:]
		if(lang!="es" and lang!="en"):
			raise Exception("Unsupported language")
		extractComments(Driver,CSVFile,name,cat, lang)
		Driver.quit()
	except:
		traceback.print_exc()
		raw_input("See the possible error and go in")
		Driver.quit()

#If you use the crawler as script and not as a library
if __name__ == '__main__':
 	if(len(sys.argv) > 1):
		address = sys.argv[1]
	else:
		print "It needs an address"
		exit()
	MainProcess(address)

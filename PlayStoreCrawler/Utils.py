#!/usr/bin/python
# coding: utf-8 
import os, time

#Just create a dictionary with default values
def createDictRate(lang):
	DictRate = {}
	if(lang == "en"):
		DictRate["Rated 1 stars out of five stars"] = 0
		DictRate["Rated 2 stars out of five stars"] = 0
		DictRate["Rated 3 stars out of five stars"] = 0
		DictRate["Rated 4 stars out of five stars"] = 0
		DictRate["Rated 5 stars out of five stars"] = 0
	if(lang=="es"):
		DictRate["Valoración: 1 estrellas de cinco"] = 0
		DictRate["Valoración: 2 estrellas de cinco"] = 0
		DictRate["Valoración: 3 estrellas de cinco"] = 0
		DictRate["Valoración: 4 estrellas de cinco"] = 0
		DictRate["Valoración: 5 estrellas de cinco"] = 0
	return DictRate

def findSplitPoint(text, lang):
	if(lang == "en"):
		months = ['January', 'February', 'March','April','May','June','July','August','September','October','November','December']
		for month in months:
			pos = text.find(month)
			if pos != -1:
				return pos
	else:
		return text.find(" de ") - 2
#Use the dictionary to check and count the number of comments
def countRates(DictRate,actualRate):
	if(DictRate[actualRate]<1000):
		DictRate[actualRate] = DictRate[actualRate] + 1
		return True		
	else:
		return False

#Just refresh and print
def ShowInfo(DictRate, start_time, lang):
	if(lang=="es"):
		os.system('cls' if os.name == 'nt' else 'clear')
		print "Obtener la hoja anterior ha costado " + str(time.time() - start_time)
		for k in DictRate.keys():
			print k+"\t"+str(DictRate[k])
	else:
		os.system('cls' if os.name == 'nt' else 'clear')
		print "To get the last page it cost " + str(time.time() - start_time)
		for k in DictRate.keys():
			print k+"\t"+str(DictRate[k])

#Check if the task is finished
def IsFinished(DictRate):
	toRet = True
	for k in DictRate.keys():
		if DictRate[k] < 1000:
			toRet = False
	return toRet

#Create the outputFile
def createCSV(name,category):
	Path = os.getcwd() + "/Results/"+ category 
	Route = Path +"/"+ name
	print Route
	if not os.path.exists(Path):
		os.makedirs(Path)
	CSVFile = open(Route,'a')
	Header = "ID\tAppName\tCategory\tNickname\tDate\tRating\tComment\n"
	CSVFile.write(Header)
	return CSVFile

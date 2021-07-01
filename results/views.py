import os,time

import urllib.parse as urlparse

from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.conf import settings



from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from time import sleep



DRIVER = 'chromedriver'
def get_results(request):
	username = request.POST.get('your_name')
	if request.method == 'POST' and len(username)==10:


		chrome_options=webdriver.ChromeOptions()
		chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
		chrome_options.add_argument("disable-dev-shm-usage")
		chrome_options.add_argument("disable-gpu")
		chrome_options.add_argument("disable-features=NetworkService")
		chrome_options.add_argument("no-sandbox")
		chrome_options.add_argument('headless') #Set the parameters of the option
		driver = webdriver.Chrome(chrome_options=chrome_options) # Open Google Chrome
		#driver = webdriver.Chrome("chromedriver.exe", options=opt)
		driver.get("https://jntukresults.edu.in/view-results-56736132.html")

		sbox = driver.find_element_by_class_name("txt")
		sbox.send_keys(username)

		submit = driver.find_element_by_class_name("ci")
		submit.click()
		time.sleep(1)
		rows = driver.find_elements_by_xpath("/html/body/div/div/div/div/center/div[1]/table/tbody/tr")
		cols = driver.find_elements_by_xpath("//*[@id='rs']/table/tbody/tr[6]/td")
		if(len(rows)==0 and len(cols)==0):
			context={
			"error":"Enter Correct registration number"
			}
			return redirect('get_results')
			#return render(request, 'wrongreg.html',context)
		else:
			l=[]
			k=[]
			p=[]
			for i in rows:
				l.append(i.text)
			for i in cols:
				k.append(i.text)

			v=len(l)
			for i in range(1,v-1):
				p.append(list(l[i].split(" "))[-2:])
			#print(p)

			def grade(q):
				if(q=="COMPLETED"):
					return 0
				if(q=="O"):
					return 10
				elif(q=="S"):
					return 9
				elif(q=="A"):
					return 8
				elif(q=="B"):
					return 7
				elif(q=="C"):
					return 6
				elif(q=="D"):
					return 5
				elif(q=="F"):
					return 0

			def percentage(p):
				a=0
				for i in p:
					a=a+grade(i[0])*int(i[1])
				return a
			def total(p):
				a=0
				f=0
				for i in p:
					if(i[0]=='F'):
						f=f+1
					else:
						a=a+int(i[1])
				return (a+3*f,f)
			t=total(p)
			cgpa = round(percentage(p)/t[0],2)
			percentage = round(((percentage(p)/t[0])-0.7)*10,2)
			driver.close()

			context = {
	        "cgpa": cgpa,
	        "percentage":percentage,
	        "username":username,
	        "f":t[1],
	    	}


			return render(request, 'results.html',context)
	elif(request.method == 'POST'):
		context={
		"error":"Enter Correct registration number"
		}
		return render(request, 'home.html',context)
	else:
		return render(request, 'home.html')
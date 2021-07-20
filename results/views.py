import os,time

import urllib.parse as urlparse

from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.conf import settings
from webdriver_manager.chrome import ChromeDriverManager



from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from time import sleep



DRIVER = 'chromedriver'
def get_results(request):
	username = request.POST.get('your_name')
	sem = request.POST.get('sem')
	year = request.POST.get('year')
	semlink=str(year)+str(sem)
	typeres=request.POST.get('type')
	if(semlink=="32"):
		username="999"

	link={
	'11':"https://jntukresults.edu.in/view-results-56735976.html",
	'12':"https://jntukresults.edu.in/view-results-56736023.html",
	'21':"https://jntukresults.edu.in/view-results-56736074.html",
	'22':"https://jntukresults.edu.in/view-results-56736111.html",
	'31':"https://jntukresults.edu.in/view-results-56736132.html",
	}
	l=["11","12","21","22","31"]

	if request.method == 'POST' and len(username)==10:

		#GOOGLE_CHROME_PATH = '/app/.apt/usr/bin/google_chrome'
		
		#CHROMEDRIVER_PATH = '/app/.chromedriver/bin/chromedriver'
		chrome_options=webdriver.ChromeOptions()
		chrome_options.add_argument("disable-dev-shm-usage")
		chrome_options.add_argument("disable-gpu")
		chrome_options.add_argument("disable-features=NetworkService")
		chrome_options.add_argument("no-sandbox")
		#chrome_options.binary_location = GOOGLE_CHROME_PATH
		chrome_options.add_argument('headless') #Set the parameters of the option
		#driver = webdriver.Chrome(chrome_options=chrome_options) # Open Google Chrome
		#driver = webdriver.Chrome(chrome_options=chrome_options)
		driver = webdriver.Chrome(executable_path=ChromeDriverManager().install(), chrome_options=chrome_options)
		if(typeres=="cgpa"):
			print("cgpa")
			p1=0
			cgpa=0
			f1=0
			for i in l:
				driver.get(link[i])
				sbox = driver.find_element_by_class_name("txt")
				sbox.send_keys(username)

				submit = driver.find_element_by_class_name("ci")
				submit.click()
				time.sleep(1)
				rows = driver.find_elements_by_xpath("/html/body/div/div/div/div/center/div[1]/table/tbody/tr")
				cols = driver.find_elements_by_xpath("//*[@id='rs']/table/tbody/tr[6]/td")
				if(len(rows)==0 and len(cols)==0):
					context={
					"error":"Enter Correct registration number and year"
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
					sgpa = round(percentage(p)/t[0],2)
					percentage = round(((percentage(p)/t[0])-0.7)*10,2)
					p1=p1+percentage
					cgpa=cgpa+sgpa
					f1=f1+int(t[1])
					print(cgpa)
			p1=round(p1/5,2)
			cgpa=round(cgpa/5,2)
			print(cgpa)
			context = {
		    "sgpa": cgpa,
		    "percentage":p1,
		    "username":username,
		    "f":"you have"+ " "+str(f1)+" " +"backlogs",
		    }
			return render(request, 'results.html',context)














		else:


			driver.get(link[semlink])

			sbox = driver.find_element_by_class_name("txt")
			sbox.send_keys(username)

			submit = driver.find_element_by_class_name("ci")
			submit.click()
			time.sleep(1)
			rows = driver.find_elements_by_xpath("/html/body/div/div/div/div/center/div[1]/table/tbody/tr")
			cols = driver.find_elements_by_xpath("//*[@id='rs']/table/tbody/tr[6]/td")
			if(len(rows)==0 and len(cols)==0):
				context={
				"error":"Enter Correct registration number and year"
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
				sgpa = round(percentage(p)/t[0],2)
				percentage = round(((percentage(p)/t[0])-0.7)*10,2)
				driver.close()

				context = {
		        "sgpa": sgpa,
		        "percentage":percentage,
		        "username":username,
		        "f":"you have"+ " "+str(t[1])+" " +"backlogs",
		    	}


			return render(request, 'results.html',context)
	elif(request.method == 'POST'):
		context={
		"error":"Enter Correct registration number"
		}
		return render(request, 'home.html',context)
	else:
		return render(request, 'home.html')

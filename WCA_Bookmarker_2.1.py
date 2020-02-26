#!/usr/bin/env python3
#WCA Bookmarker 2.1
#02/25/2020
#Brandon Mikel

#This version does not have GUI. It's meant to be run automatically.

#Import Modules
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time, smtplib, os

wcaUser=''
kitchenRocksNeverSly=''
compsEmail=[]

#Set Variables

wcaUser='2020WXYZ01' #WCA Username
kitchenRocksNeverSly='password' #WCA Password
country= 'All' #Set to All or select country
markFunction='Bookmark' #Set to 'Bookmark' or 'Un-Bookmark'
senderEmail='email@email.com' #Sending email (Must be gmail)
senderPass='password' #Sending email password
receiverEmail='email2@email.com' #Receiving Email
browserPath = "//users/username/geckodriver"

#Set Variables based on Mark
if markFunction == 'Bookmark':
    markElemID='not-bookmarked'
    printText1='The following competitions have been bookmarked:'
else:
    markElemID='bookmarked'
    printText1='The following competitions have been un-bookmarked:'

#Open Firefox
cap = DesiredCapabilities().FIREFOX
cap["marionette"] = True
browser = webdriver.Firefox(capabilities=cap, executable_path= browserPath)

#Go to WCA Site
browser.get('http://worldcubeassociation.org/users/sign_in')

#Log in as user for WCA Site
userElem=browser.find_element_by_id('user_login')
userElem.send_keys(wcaUser)
passwordElem=browser.find_element_by_id('user_password')
passwordElem.send_keys(kitchenRocksNeverSly)
submit=browser.find_element_by_name('commit')
submit.click()

#Go to Competition list
compURL='https://www.worldcubeassociation.org/competitions'
browser.get(compURL)
maxElem=browser.find_element_by_xpath('/html/body/div[3]/div/div[2]/div[@id="upcoming-comps"]/ul/li[1]/strong')
maxElemInt=int(str(maxElem.text)[23:26])

for i in range(2,maxElemInt+3):
    if country == 'All':
        try:
            listElem=browser.find_element_by_xpath('html/body/div[3]/div/div[2]/div[@id="upcoming-comps"]/ul/li[' + str(i) + ']/span[2]/div[1]/a')
            textElem=listElem.text
            listElem.click()
            time.sleep(0.5)

            #Bookmark Competition [All]
            try:
                bookmarkElem=browser.find_element_by_id(markElemID)
                bookmarkElem.click()
                time.sleep(0.5)
                compsEmail.append(str(textElem))
            except:
                ''
            
            browser.get(compURL)
        except:
            ''
    else:
        try:
            listCountry=browser.find_element_by_xpath('/html/body/div[3]/div/div[2]/div[@id="upcoming-comps"]/ul/li[' + str(i) + ']/span[2]/div[2]/strong')
            if listCountry.text == country:
                listElem=browser.find_element_by_xpath('html/body/div[3]/div/div[2]/div[@id="upcoming-comps"]/ul/li[' + str(i) + ']/span[2]/div[1]/a')
                textElem=listElem.text
                listElem.click()
                time.sleep(0.5)

                #Bookmark Competition [Country]
                try:
                    bookmarkElem=browser.find_element_by_id(markElemID)
                    bookmarkElem.click()
                    time.sleep(0.5)
                    compsEmail.append(str(textElem))
                except:
                    ''
            
                browser.get(compURL)
            else:
                ''
        except:
            ''
#send email with results
smtpObj=smtplib.SMTP('smtp.gmail.com',587)
smtpObj.ehlo()
smtpObj.starttls()
smtpObj.login(senderEmail,senderPass)
smtpObj.sendmail(senderEmail,receiverEmail,'Subject: WCA Daily Bookmarked Competitions \n\n' + printText1 + ' \r\n' + str(compsEmail))
smtpObj.quit()

#print results to shell and close browser
print(printText1+str(compsEmail))
browser.quit()

#Put computer to sleep
os.system("osascript -e 'tell application \"Finder\" to sleep'")







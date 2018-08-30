import os
import datetime
from dbfun import runquery,runinsert
#import urllib3
import requests, zipfile, io

#from datetime import date, month, year


def file_path(date1): #=====================================================add code to check id date1 is set
    #https://www.bseindia.com/download/BhavCopy/Equity/EQ010118_CSV.ZIP
    #date1 = str(date1)
    url = "https://www.bseindia.com/download/BhavCopy/Equity/"
    #year, month, date = (int(x) for x in date1.split('-'))
    #date = datetime.datetime.strptime(str(date1["date"]), "{'date': datetime.date(%Y, %m, %d)}")
    date = datetime.datetime.strptime(str(date1["date"]), "%Y-%m-%d")
    year = date.year
    month = date.month
    day = date.day
    #print(year)
    filename = "EQ"+ str("%02d" % day)+ str("%02d" % month)+ str(year)[-2:] +"_CSV.ZIP"
    extfilename = "EQ"+ str("%02d" % day)+ str("%02d" % month)+ str(year)[-2:] +".CSV"
    fileurl = url+ filename
    return fileurl, filename, extfilename

def download_file(fileurl, filename, extfilename, date):
    # download the file
    outputFilename = "downloaded/" + filename
    extractfilename = "extracted/" + filename
    if not os.path.isdir(extractfilename):
        #Downloading file
        print ("Downloading ",fileurl)
        try:
            r = requests.get(fileurl)
            with zipfile.ZipFile(io.BytesIO(r.content)) as myzip:
            #myzip.extract(extfilename, extractfilename)
                myzip.extractall()
        except IOError:
            print("IO Error")
        else:
            print("some error")
    print ("download complete")


def add_dates(num):
    x=num
    date2 = datetime.datetime.now() - datetime.timedelta(days = num)
    while x>0:
        try:
            date2 += datetime.timedelta(days=1)
            qry = "INSERT INTO bhav_data_status (date, status) VALUES (DATE_FORMAT('" + str("%s" % date2) + "', '%Y-%m-%d'), null) ON DUPLICATE KEY UPDATE status = status"
            #(" + str(date2 +",null)"     INSERT INTO bhav_data_status (date, status) VALUES('2018-07-03', null) ON DUPLICATE KEY UPDATE status = status
            runinsert(qry)
            print(qry)
            x-=1
        except KeyboardInterrupt:
            break
    return "Done"


def updatebhavedata():
    # check for extraction directories existence
    if not os.path.isdir('downloaded'):
        os.makedirs('downloaded')
    if not os.path.isdir('extracted'):
        os.makedirs('extracted')
    dates = runquery("select date from bhav_data_status where status is null")
    #dates = runquery("select DATE_FORMAT(date, '%Y-%m-%d') date from bhav_data_status where status is null")
    #d=0
    for date in dates:
        fileurl, filename, extfilename = file_path(date)
        datesa  = [fileurl, filename, "done"]
        download_file(fileurl, filename, extfilename, date)
        #d+=1
        print(fileurl+" - Done"+" "+str(date["date"]))
    return datesa

    #DATE_FORMAT(now()+1, '%Y-%m-%d')

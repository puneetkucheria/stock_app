import urllib, urllister
import zipfile
import urllib2
import os
import time
import pickle

# check for extraction directories existence
if not os.path.isdir('downloaded'):
    os.makedirs('downloaded')

if not os.path.isdir('extracted'):
    os.makedirs('extracted')

# open logfile for downloaded data and save to local variable
if os.path.isfile('downloaded.pickle'):
    downloadedLog = pickle.load(open('downloaded.pickle'))
else:
    downloadedLog = {'key':'value'}

# remove entries older than 5 days (to maintain speed)

# path of zip files
zipFileURL = "http://www.thewebserver.com/that/contains/a/directory/of/zip/files"

# retrieve list of URLs from the webservers
usock = urllib.urlopen(zipFileURL)
parser = urllister.URLLister()
parser.feed(usock.read())
usock.close()
parser.close()

# only parse urls
for url in parser.urls:
    if "PUBLIC_P5MIN" in url:

        # download the file
        downloadURL = zipFileURL + url
        outputFilename = "downloaded/" + url

        # check if file already exists on disk
        if url in downloadedLog or os.path.isfile(outputFilename):
            print "Skipping " + downloadURL
            continue

        print "Downloading ",downloadURL
        response = urllib2.urlopen(downloadURL)
        zippedData = response.read()

        # save data to disk
        print "Saving to ",outputFilename
        output = open(outputFilename,'wb')
        output.write(zippedData)
        output.close()

        # extract the data
        zfobj = zipfile.ZipFile(outputFilename)
        for name in zfobj.namelist():
            uncompressed = zfobj.read(name)

            # save uncompressed data to disk
            outputFilename = "extracted/" + name
            print "Saving extracted file to ",outputFilename
            output = open(outputFilename,'wb')
            output.write(uncompressed)
            output.close()

            # send data via tcp stream

            # file successfully downloaded and extracted store into local log and filesystem log
            downloadedLog[url] = time.time();
            pickle.dump(downloadedLog, open('downloaded.pickle', "wb" ))

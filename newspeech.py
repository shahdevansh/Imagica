import os
import re
import json
import urllib2
import nltk
import nltk.data
import sys
import time
from urllib import FancyURLopener
import urllib2
import simplejson
import cgkit
import Image
class MyOpener(FancyURLopener): 
    version = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11'
myopener = MyOpener()

print 'Here'
#tokenizer = nltk.data.load('nltk:tokenizers/punkt/english.pickle')
print "speak now"

os.system("arecord -d 3 -f cd -t wav out1.wav") #record voice for 3 seconds and store it in out.wav
os.system("flac --best -f out1.wav") # convert out.wav to flac format so as to use google voice recognation service

url = "https://www.google.com/speech-api/v1/recognize?xjerr=1&client=chromium&lang=en-US" #url for voice recognation
audio = open('out1.flac','rb').read() #reading audio file to pass it as an argument to the url
headers={'Content-Type': 'audio/x-flac; rate=44100'} #header information about audio file
request = urllib2.Request(url, data=audio, headers=headers) #send the request to url
response = urllib2.urlopen(request) #get the response string

x= json.loads(response.read()) #store the response in variable x which is a json string
print x

if(x['hypotheses']): #code to extract the recognized speech
    z=x['hypotheses'][0]['utterance']
    tokens=nltk.word_tokenize(z.lower())
    text=nltk.Text(tokens)
    tags=nltk.pos_tag(text)
    print tags
    for i in tags:
    	count= 0
	searchTerm = ""
	f = 0
	if i[1] == 'NN':
		f = 1
	    	searchTerm = i[0]
		searchTerm = searchTerm.replace(' ','%20')
	elif re.match(i[1],'VB*'):
		f = 1
		searchTerm = i[0] + "emoticon"
		searchTerm = searchTerm.replace(' ','%20')

	for j in range(0,1):
	 if f == 1:
	    url = ('https://ajax.googleapis.com/ajax/services/search/images?' + 'v=1.0&q='+searchTerm+'&start='+str(j)+'&userip=MyIP')
    	    print url
    	    request = urllib2.Request(url, None, {'Referer': 'testing'})
    	    response = urllib2.urlopen(request)

    	    # Get results using JSON
    	    results = simplejson.load(response)
    	    data = results['responseData']
    	    dataInfo = data['results']

    	    # Iterate for each result and get unescaped url
    	    myUrl = dataInfo[0]
            print myUrl['unescapedUrl']
            myopener.retrieve(myUrl['unescapedUrl'],str(count)+'.jpg')
	    image = Image.open(str(count) + '.jpg')
	    image.show()
	    count += 1
	    time.sleep(1)

    z=z.split(' ')
    print z
    if "is" in z:
	    print 'here'
    else:
	    print 'not here'



from nlc import NaturalLanguageClassifierInstance
import sys
import argparse
import requests

import urllib2
import csv
import base64
import json
import io
from collections import *
import operator
from termcolor import colored
from itertools import *
 
sample_url = 'https://gateway.watsonplatform.net/natural-language-classifier/api'
question_text = 'What is the name of my plan?'
NLC_container = {}

# Container: Cigna Benefits-P160201
if True:
    bm_username = '5cb28ce5-b30c-4b08-afe0-889140a41109'
    bm_password = 'qZOPxH7wpLXM'
    NLC_container[ bm_username ] = bm_password

# Container: IBM Benefits-P160101
if True:
    bm_username = '255592a6-fddd-4967-aad9-97b29c6c7817'
    bm_password = 'cYP6HsH41M4O'
    NLC_container[ bm_username ] = bm_password

# Container: SoC Benefits-P160131
if True:
    bm_username = '9ad19c8f-398a-462d-8a50-be767be012e5'
    bm_password = '1pWfKO54CrD1'
    NLC_container[ bm_username ] = bm_password


def test(classifierid, username, password, question):
	
	classifier_url = "https://gateway.watsonplatform.net/natural-language-classifier/api/v1/classifiers/" + classifierid + "/classify"
	base64string = base64.encodestring('%s:%s' % (username, password)).replace('\n', '')
	headers = {'Content-type': 'application/json', 'Accept': 'application/json',
	       'Authorization': 'Basic %s' % base64string}

      	#submit to NLC and get response back
      	data = json.dumps({'text': question})
      	request = urllib2.Request(classifier_url, data=data, headers=headers)
      	response = urllib2.urlopen(request)
      	json_response = json.loads(response.read())
        
      	tc_name = json_response["classes"][0]["class_name"]
      	tc_conf = json_response["classes"][0]["confidence"]
      	return tc_name, tc_conf
      	

if __name__ == "__main__":
    available = 0
    not_available = 0
    
    for bm_username, bm_password in NLC_container.iteritems():
        
        nlc_instance = NaturalLanguageClassifierInstance(bm_username, bm_password, sample_url)
        # print "Listing all classifiers : Total No. : %d" % len(nlc_instance.get_classifiers())
        
        for nlcInstance in nlc_instance.get_classifiers():
            # print nlcInstance.get_id() + ' ' + nlcInstance.get_name() + ' ' + nlcInstance.get_created_date() + ' ' + nlcInstance.get_status()
            classifier_id = nlcInstance.get_id()
            nlc_status = nlcInstance.get_status()
            
            if nlc_status == 'Available':
                available += 1
            else:
                not_available += 1
            
            # Checking status of classifier health (NLC container inventory)
            tc_name, tc_conf = test(classifier_id, bm_username, bm_password, question_text)
            
            print classifier_id + '\t(' + nlcInstance.get_name() + ')'
            print '\t=> Status: ' + nlc_status
            print '\t=> Response: ' + tc_name + '\t' + str(tc_conf)
            
    print 'NLC available:', available
    print 'NLC *not* available:', not_available
    print
    sys.exit(0)


#this script takes a json file in classifier format and uses it to test how well a classifier performs against it
#it produces an output indicating accuracy and recall@5
#command : python test.py testfile classifierid bm_username bm_password
#example : python test.py test.json FD87F2-nlc-82 dge726egfg83728 gh26w7gd

import urllib2
import json
import base64
import sys
import argparse
import io

def test(inputfile, classifierid, username, password, dumpresultfile):

	response_with_truth = []
	
	with open(inputfile) as f:
		test_data = json.load(f)    
	total = 0
	correct = 0
	top_5 = 0

	classifier_url = "https://gateway.watsonplatform.net/natural-language-classifier-experimental/api/v1/classifiers/" + classifierid + "/classify"
	base64string = base64.encodestring('%s:%s' % (username, password)).replace('\n', '')
	headers = {'Content-type': 'application/json', 'Accept': 'application/json', 'Authorization':'Basic %s' % base64string}
    
	for entry in test_data['training_data']:
		data = json.dumps({'text':entry['text']})
		request = urllib2.Request(classifier_url,data=data, headers=headers)
		response = urllib2.urlopen(request)
		total = total + 1
		json_response = json.loads(response.read())
		json_response['actual_classes'] = entry['classes']
		
		response_with_truth.append(json_response)
		
		if json_response['top_class'] in entry['classes']:
			correct=correct+1
		for top_classes in json_response['classes'][0:5]:
			if top_classes['class_name'] in entry['classes']:
				top_5 = top_5 + 1
		
		print 'currently got ' + str(correct) + ' correct out of ' + str(total)	
			
	print "******final results*********"
	print "correct: " + str(correct) +  " (percentage: " + str(correct*100/total) + "%)" 
	print "num of times in top 5: " + str(top_5) + " (percentage: " + str(top_5*100/total) + "%)" 
	print "total: " + str(total)
	
	if dumpresultfile != None:
		with io.open(dumpresultfile, 'w', encoding='utf-8') as f:
			f.write(unicode(json.dumps(response_with_truth, ensure_ascii=False, sort_keys=True, indent=4, separators=(',', ': '))))

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("testfile", help="A file containing the test set in classifier json format")
	parser.add_argument("classifier_id", help="The id of the classifier that is to be tested")
	parser.add_argument("bm_username", help="The bluemix username")
	parser.add_argument("bm_password", help="The bluemix password")
	parser.add_argument("-d", "--dumpresultfile", help="produces a json dump of the output to the file specified")
	args = parser.parse_args()
	test(args.testfile, args.classifier_id, args.bm_username, args.bm_password, args.dumpresultfile)
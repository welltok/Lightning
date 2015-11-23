# this script takes a json file in classifier format and uses it to test how well a classifier performs against it
# it produces an output indicating accuracy and recall@5

import urllib2
import csv
import base64
import json
import io
from collections import *
import operator
from termcolor import colored
from itertools import *
import argparse

def avg_lol(list_of_lists):
		avg_scores = dict()
		for class_name,classifications in list_of_lists.iteritems():
			total_guesses = len(classifications)
			correct_guesses = 0
			for classification in classifications:
				if classification[0] == class_name:
					correct_guesses += 1
			avg_scores[class_name] = float(correct_guesses) / float(total_guesses) 	
		return avg_scores


def count_lol(list_of_lists):
	counts = dict()
	for item in { item for sublist in list_of_lists for item in sublist }:
		counts[item] = sum(x.count(item) for x in list_of_lists)

	sorted_x = sorted(counts.items(), key=operator.itemgetter(1), reverse=True)
	return sorted_x




def test(inputfile, classifierid, username, password):
	response_with_truth = []
	f = open(inputfile, 'r+')
	test_data = csv.reader(f, delimiter=',')
	total = 0
	correct = 0
	top_5 = 0
	correct_confs = defaultdict(list)
	incorrect_confs = defaultdict(list)

	top5_classes = defaultdict(list)

	classifier_url = "https://gateway.watsonplatform.net/natural-language-classifier/api/v1/classifiers/" + classifierid + "/classify"
	base64string = base64.encodestring('%s:%s' % (username, password)).replace('\n', '')
	headers = {'Content-type': 'application/json', 'Accept': 'application/json',
	       'Authorization': 'Basic %s' % base64string}


	for entry in test_data:
		total+=1
		question = entry[0]
		correct_class = entry[1]
		data = json.dumps({'text': question})
		
		#submit to NLC and get response back
		request = urllib2.Request(classifier_url, data=data, headers=headers)
		response = urllib2.urlopen(request)
	 
		json_response = json.loads(response.read())

		
		tc_name = json_response["classes"][0]["class_name"]
		tc_conf = json_response["classes"][0]["confidence"]
		if tc_name == correct_class:
			correct +=1
			correct_confs[correct_class] += [tc_conf]
		else:		
			incorrect_confs[correct_class] += [tc_conf]

		#avg_conf[tc_name].append(tc_conf)




		top5_class = []
		top5_conf = []
		for top_classes in json_response['classes'][0:5]:
			if top_classes['class_name'] == correct_class:
				top_5 +=1
		for top_classes in json_response['classes'][0:1]:
	
			top5_class.append(top_classes['class_name'])

		top5_classes[correct_class].append(top5_class)
		    #if top_classes['class_name'] in entry[1]:
			#top_5 = top_5 + 1
			#top5Match = True
			#break



	#	avg_conf_scores = {reduce(lambda x, y: x + y, l) / len(l) for k,l in avg_conf.iteritems()}
	print colored("******Overall Classifier Statistics*********", 'blue')
	percent_correct = correct * 100 / total
	if percent_correct > 90:
		print "correct: " + str(correct) + " (percentage: " + colored(str(percent_correct) + "%)", 'green')
	else:
		print "correct: " + str(correct) + " (percentage: " + colored(str(percent_correct) + "%)", 'red')

	percent_correct = top_5 * 100 / total
	if percent_correct > 90:
		print "num of times in top 5: " + str(top_5) + " (percentage: " + colored(str(percent_correct) + "%)", 'green')
	else:
		print "num of times in top 5: " + str(top_5) + " (percentage: " + colored(str(percent_correct) + "%)", 'red')

	print "total: " + colored(str(total), 'green')
	print colored("******Breakdown by class*********", 'blue')


	#average confidence scores
	avg_corr_conf_scores = dict()
	for k,l in correct_confs.iteritems():
		avg_corr_conf_scores[k] = reduce(lambda x, y: x + y, l) / len(l)
	avg_incorr_conf_scores = dict()
	for k,l in incorrect_confs.iteritems():
		avg_incorr_conf_scores[k] = reduce(lambda x, y: x + y, l) / len(l)
	#average accuracy scores

	avg_acc_scores = avg_lol(top5_classes)

	misclass_dict =defaultdict(int)	
	all_classes = avg_acc_scores.keys()
	for k in all_classes:
		print k, ":",len(top5_classes[k])
		print "\tAvg. Accuracy:" + str(avg_acc_scores[k] * 100) + "%"

		if k in avg_corr_conf_scores:
			print "\tAvg. Conf (when correct):" +  str(avg_corr_conf_scores[k] * 100) + "%"
		else:
			print "\tAvg. Conf (when correct): N/A"
		if k in avg_incorr_conf_scores and avg_incorr_conf_scores[k] * 100 < 99:
			print "\tAvg. Conf (when incorrect):" +  str(avg_incorr_conf_scores[k] * 100) + "%"
		else:
			print "\tAvg. Conf (when incorrect): N/A"

		
		top_confusions = count_lol(top5_classes[k])[0:5]
		print "\tClassification errors:"
		for (tc,v) in  top_confusions:
			misclass_dict[k] += v
			if k != tc:
				print "\t\t", tc, v, "times"
		print "\n"
	print colored("******Incorrect Classification Percents*********\n", 'blue')
	sorted_mcs= sorted(misclass_dict.items(), key=operator.itemgetter(1), reverse=True)
	misclass_total = sum([pair[1] for pair in sorted_mcs])
	for (misclass,count) in  sorted_mcs:
		print str(misclass) + ":",str(float(count) / float(misclass_total) *100)+ "%"
		#print "Average confidence for " + str(k) +" is ",  avg_conf_scores[k]
	#for k,v in sorted(avg_conf_scores.items(), key=operator.itemgetter(1)):
		#print "Average confidence for " + str(k) +" is ",  colored(str(v), 'red')

		#if v < .9:
		#	print "Average confidence for " + str(k) +" is ",  colored(str(v), 'red')
		#else:
		#	print "Average confidence for " + str(k) +" is ",  colored(str(v), 'green')

	
if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("testfile", help="A file containing the test set in classifier json format")
	parser.add_argument("classifier_id", help="The id of the classifier that is to be tested")
	parser.add_argument("bm_username", help="The bluemix username")
	parser.add_argument("bm_password", help="The bluemix password")
	args = parser.parse_args()

	test(args.testfile, args.classifier_id, args.bm_username, args.bm_password)


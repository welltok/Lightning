#this script takes a json file in classifier format and breaks it into a train and a test json file given a percentage
#command : python split.py inputfile percent_train outputtrainfile outputtestfile
#example : python split.py nlc_data_train 80 train.json test.json


from random import random
import json
import io
import sys

def main(argv):

	if len(argv) != 4:
		print 'split.py inputfile percent_train outputtrainfile outputtestfile'

	with open(argv[0]) as f:
		total_data = json.load(f)
    
	train = []
	test = []
	
	percent_as_decimal = float(argv[1])/100
        print(percent_as_decimal)    
	for entry in total_data['training_data']:
		if random() < percent_as_decimal:
			train.append(entry)
		else:
			test.append(entry)
			
	train_output = {"language":"en","training_data":train}
	test_output = {"language":"en","training_data":test}

	with io.open(argv[2], 'w', encoding='utf-8') as trainf:
		trainf.write(unicode(json.dumps(train_output, ensure_ascii=False, indent=4)))

	with io.open(argv[3], 'w', encoding='utf-8') as testf:
		testf.write(unicode(json.dumps(test_output, ensure_ascii=False, indent=4)))
		
if __name__ == "__main__":
	main(sys.argv[1:])

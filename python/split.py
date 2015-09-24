#this script takes a csv file in classifier format and breaks it into a train and a test csv file given a percentage
#command : python split.py inputcsvfile percent_train outputtraincsvfile outputtestcsvfile
#example : python split.py nlc_data_train 80 train.csv test.csv


from random import random
import csv
import sys


def main(argv):
    if len(argv) != 4:
        print 'split.py inputfile percent_train outputtrainfile outputtestfile'

    csvFile = open(argv[0],'rb')
    print(csvFile.name)
    trainCsv = open(argv[2],'w')
    testCsv = open(argv[3],'w')
    csvTrainWriter = csv.writer(trainCsv, delimiter=',')
    csvTestWriter = csv.writer(testCsv, delimiter=',')

    with open(argv[0]) as f:
        total_data = csv.reader(csvFile, delimiter=',')

    percent_as_decimal = float(argv[1])/100

    for row in total_data:
        if random() < percent_as_decimal:
            csvTrainWriter.writerow([row[0], row[1]])
        else:
            csvTestWriter.writerow([row[0], row[1]])

    trainCsv.close()
    testCsv.close()
    csvFile.close()

if __name__ == "__main__":
    main(sys.argv[1:])
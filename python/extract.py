import csv
import xml.etree.ElementTree as ET
import argparse

# Extracts questions, PAUs from Ground Truth Snapshot XML and creates a CSV file for NLC training purposes
# Pre-Requisite : The XML must be exported from WEA ExperienceManager using the GroundTruthSnapshot export option
# Parameters :
# gttsnapshotxml - GTT Snapshot XML
# outputfile - output CSV
# numquestion - No. of questions to limit (NLC has a limitation of 20 MB size for the jSON and 10K training instance)
# classesreportfile - Reports the number of unique classes. Each line is a class, with the primary question as a key

#TODO # o
def extract(gttsnapshotxml, outputfile, numquestions, classesreportfile):

    print("No. of training instances requested : ", numquestions)

    root = ET.parse(gttsnapshotxml).getroot()
    csvFile = open(outputfile, 'w')
    dictionaryFlie = open(classesreportfile, 'w')
    questionFile = open("questionfile.csv",'w')

    csvWriter = csv.writer(csvFile, delimiter=',')
    questionFileWriter = csv.writer(questionFile,delimiter=',')

    tCount = 0
    count = 0
    questionDictionary = dict()
    classesDict = dict()
    classCount = 0

    for question in root.iter('question'):

	
        id = question.find('id').text if question.find('id') is not None else ""
        value = question.find('value').text if question.find('value') is not None else ""

        questionText = value.lstrip().rstrip()

        # Get primary question PAU
        predefinedAnswerUnit = question.find('predefinedAnswerUnit').text if question.find(
            'predefinedAnswerUnit') is not None else ""

        # Look for mapped question
        mappedQuestion = question.find('mappedQuestion') if question.find('mappedQuestion') is not None else ""

        # Check for valid question, has mapped question section and not PAU - This means secondary question
        if questionText != "" and predefinedAnswerUnit == "" and mappedQuestion != "":
            parentQuestionPau = ""
            parentQuestionPau = mappedQuestion.find('predefinedAnswerUnit') if mappedQuestion.find(
                'predefinedAnswerUnit') is not None else ""

            mappedQuestionText = mappedQuestion.find("value").text

            #We only keep the question if we haven't seen it before. We don't want to create mulitple lines in the CSV for duplicates. This will just confuse the NLC
            if questionDictionary.get(mappedQuestionText) is None or questionDictionary.get(mappedQuestionText) == "":
                csvWriter.writerow([mappedQuestionText.encode('utf-8'), parentQuestionPau.text])
                questionDictionary.update({mappedQuestionText: parentQuestionPau.text})
                classesDict.update({parentQuestionPau.text: mappedQuestionText})
                classCount += 1
                count += 1
                continue


            if parentQuestionPau != "":
                if questionDictionary.get(questionText) is None or questionDictionary.get(questionText) == "":
                    csvWriter.writerow([questionText.encode('utf-8'), parentQuestionPau.text])
                    questionDictionary.update({questionText: parentQuestionPau.text})
                    classesDict.update({parentQuestionPau.text: questionText.encode('utf-8')})
                    classCount += 1
                    count += 1
                else:
                    existingPau = questionDictionary.get(questionText)
                    if questionDictionary.get(questionText) is None or questionDictionary.get(questionText) == "":
                        csvWriter.writerow([questionText.encode('utf-8'), existingPau])
                        questionDictionary.update({questionText: existingPau.text})
                        count += 1
        elif questionText != "" and predefinedAnswerUnit != "" and mappedQuestion == "" and questionDictionary.get(questionText) is None:
            # This means primary question
            csvWriter.writerow([questionText.encode('utf-8'), predefinedAnswerUnit])
            classesDict.update({predefinedAnswerUnit: questionText})
            questionDictionary.update({questionText: predefinedAnswerUnit})
            count += 1
            classCount += 1
    print("No. of classes found : " + str(len(classesDict)))
    print("Total Questions Generated : " + str(count))
    for item in classesDict.items():
        dictionaryFlie.write(str(item))
        dictionaryFlie.write('\n')

    for item1 in questionDictionary.items():
        questionFile.write(str(item1))
        questionFile.write('\n')

    csvFile.close()
    dictionaryFlie.close()
    questionFile.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("gttsnapshotxml", help="Ground Truth Snapshot XML File")
    parser.add_argument("outputfile", help="Output CSV File ")
    parser.add_argument("numquestions", help="No. of questions requested, as integer",type=int)
    parser.add_argument("classesreportfile", help="Classes Report CSV, ture or false")
    args = parser.parse_args()
    extract(args.gttsnapshotxml, args.outputfile, args.numquestions, args.classesreportfile)



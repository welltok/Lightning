import csv
import xml.etree.ElementTree as ET
import argparse

# Extracts questions, PAUs from Ground Truth Snapshot XML and creates a CSV file for NLC training purposes
# Pre-Requisite : The XML must be exported from WEA ExperienceManager using the GroundTruthSnapshot export option
# Parameters :
# gttsnapshotxml - GTT Snapshot XML
# outputfile - output CSV
# numquestion - No. of questions to limit (NLC has a limitation of 20 MB size on the jSON and 10K training instance)
# classesreport - Reports the number of unique classes

def extract(gttsnapshotxml, outputfile, numquestions, classesreport):

    print("No. of training instances requested : ", numquestions)

    root = ET.parse(gttsnapshotxml).getroot()
    csvFile = open(outputfile, 'w')
    dictionaryFlie = open(classesreport, 'w')
    questionFile = open("questionfile.csv",'w')

    csvWriter = csv.writer(csvFile, delimiter=',')
    questionFileWriter = csv.writer(questionFile,delimiter=',')

    count = 0
    questionDictionary = dict()
    classesDict = dict()
    classCount = 0

    for question in root.iter('question'):

        id = question.find('id').text if question.find('id') is not None else ""
        value = question.find('value').text if question.find('value') is not None else ""

        # Special handle to look for context - Welltok Only
        context = value.find(',')
        planQuestion = value.find("If I am covered")

        # Required for Plan
        #if context <= 0 or planQuestion == -1:
        #    continue
        #if count == int(numquestions):
            #break

        # Remove the context from question (Applicable for Welltok only)
        if context > 0 and planQuestion >= 0:
            questionText = value[context + 1:value.__sizeof__()].rstrip("").lstrip("")
        else:
            questionText = value

        questionText = questionText.lstrip().rstrip()

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
            if (context > 0):
                mappedQuestionText = mappedQuestionText[context + 1:mappedQuestionText.__sizeof__()].rstrip().lstrip()

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
    parser.add_argument("gttsnapshotxml", help="Ground Truth Snapshot XML")
    parser.add_argument("outputfile", help="Output CSV")
    parser.add_argument("numquestions", help="No. of questions requested")
    parser.add_argument("classesreport", help="Classes Report CSV")
    args = parser.parse_args()
    extract(args.gttsnapshotxml, args.outputfile, args.numquestions, args.classesreport)



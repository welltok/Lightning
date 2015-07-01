import json
import xml.etree.ElementTree as ET
import argparse

# Extracts questions, PAUs from Ground Truth Snapshot XML and creates a JSON file for NLC training
# Pre-Requisite : The XML must be exported from WEA ExperienceManager using the GroundTruthSnapshot export option

def extract(gttsnapshotxml, outputfile, numquestions, classesreport):
    root = ET.parse(gttsnapshotxml).getroot()
    jsonFile = open(outputfile, 'w')
    dictionaryFlie = open(classesreport, 'w')
    training_data = []

    count = 0
    questionDictionary = dict()
    classesDict = dict()
    classCount = 0

    if numquestions == 0:
        numQuestions = 10000

    for question in root.iter('question'):

        id = question.find('id').text if question.find('id') is not None else ""
        value = question.find('value').text if question.find('value') is not None else ""
        newQuestion = value.find(',')

        if count == numquestions:
            break

        if newQuestion > 0:
            continue

        # Remove the context from question
        questionText = value[newQuestion + 1:value.__sizeof__()].rstrip("").lstrip("")
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
            if parentQuestionPau != "":
                if questionDictionary.get(questionText) is None or questionDictionary.get(questionText) == "":
                    training_data.append({"text": questionText, "classes": [parentQuestionPau.text]})
                    questionDictionary.update({questionText: parentQuestionPau.text})
                    classesDict.update({parentQuestionPau.text: questionText})
                    classCount += 1
                else:
                    existingPau = questionDictionary.get(questionText)
                    training_data.append({"text": questionText, "classes": [existingPau]})
                count += 1
    output = {"language": "en", "training_data": training_data}
    json.dump(output, jsonFile, indent=4)
    print("No. of classes " + str(len(classesDict)))

    for item in classesDict.items():
        dictionaryFlie.write(str(item))
        dictionaryFlie.write('\n')
    jsonFile.close()
    dictionaryFlie.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("gttsnapshotxml", help="Ground Truth Snapshot XML")
    parser.add_argument("outputfile", help="Output JSON")
    parser.add_argument("numquestions", help="No. of questions")
    parser.add_argument("classesreport", help="Classes Report CSV")
    args = parser.parse_args()
    extract(args.gttsnapshotxml, args.outputfile, args.numquestions, args.classesreport)



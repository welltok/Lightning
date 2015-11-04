from nlc import NaturalLanguageClassifierInstance
import sys
import argparse

# 3rd party imports
import requests

if __name__ == "__main__":
    sample_url = 'https://gateway.watsonplatform.net/natural-language-classifier/api'
    user = ''
    pw = ''

    # Pass this as arguments (Example : Python nlc.py <usernamer> <password>)
    parser = argparse.ArgumentParser()
    parser.add_argument("user", help="User Name")
    parser.add_argument("pw", help="Password")
    parser.add_argument("csvfile", help="CSV file that will be used to generate the classifier (probably the training file generated from split.py)")
    parser.add_argument("classifiername", help="Name of the classifier")
    args = parser.parse_args()
    nlc_instance = NaturalLanguageClassifierInstance(args.user, args.pw, sample_url)
    # 2. Train a classifier
    #moidfy the args to accept a csv file
    nlc_instance.train_classifier(args.classifiername,training_file=args.csvfile)


    sys.exit(0)

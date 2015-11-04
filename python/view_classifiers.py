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
    args = parser.parse_args()
    nlc_instance = NaturalLanguageClassifierInstance(args.user, args.pw, sample_url)
    # 2. Train a classifier
    #moidfy the args to accept a csv file

    print "Listing all classifiers : Total No. : %d" % len(nlc_instance.get_classifiers())
    for nlInstance in nlc_instance.get_classifiers():
        print nlInstance.get_id() + ' ' + nlInstance.get_name() + ' ' + nlInstance.get_created_date() + ' ' + nlInstance.get_status()


    sys.exit(0)

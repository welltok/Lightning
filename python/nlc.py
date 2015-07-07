__author__ = 'vdowling'

# Standard imports
import json
import sys

# 3rd party imports
import requests

# Local imports


class NaturalLanguageClassifierInstance(object):
	"""
		Class that wraps the functionality associated with a single NLC instance
	"""
	def __init__(self, username, password, url):
		if type(username) is not str or username == "":
			raise ValueError("Username provided is none or is not of proper type")
		elif type(password) is not str or password == "":
			raise ValueError("Password provided is none or is not of proper type")
		elif type(url) is not str or url == "":
			raise ValueError("Url provided is none or is not of proper type")
		else:
			self.username_ = username
			self.password_ = password
			self.url_ = url
			self.classifiers_ = list()
			resp = requests.get("%s/v1/classifiers" % self.url_, headers={"Content-Type": "application/json"}, auth=(self.username_, self.password_))
			if resp.ok:
				for classifier in resp.json().get('classifiers') if 'classifiers' in resp.json().keys() else []:
					classifier_url = classifier.get('url')
					classifier_obj = NaturalLanguageClassifier(self.username_, self.password_, classifier_url=classifier_url)
					self.classifiers_.append(classifier_obj)

	def train_classifier(self, classifier_name="CLASSIFIER", training_data=[], language='en', training_file=None):
		# Create the training object
		if training_file is not None:
			with open(training_file, 'rt') as infile:
				training_obj = json.load(infile)
		else:
			training_obj = {"name": classifier_name, "training_data": training_data, language: language}

		# Train the classifier, append it to the list of classifiers
		resp = requests.post("%s/v1/classifiers" % self.url_, data=json.dumps(training_obj), headers={"Content-Type": "application/json"}, auth=(self.get_username(), self.get_password()))
		if resp.ok:
			classifier_url = resp.json().get('url')
			print "[python] Classifier training. Classifier Information : %r" % resp.json()
			classifier_obj = NaturalLanguageClassifier(self.get_username(), self.get_password(), classifier_url)
			self.classifiers_.append(classifier_obj)
			return classifier_obj
		else:
			raise resp.raise_for_status()

	def get_classifier_by_id(self, classifier_id=None):
		for cls in self.get_classifiers():
			if cls.get_classifier_id() == classifier_id:
				return cls
		return None

	def get_classifiers(self):
		return self.classifiers_

	def get_url(self):
		return self.url_

	def get_username(self):
		return self.username_

	def get_password(self):
		return self.password_


class NaturalLanguageClassifier(object):
	"""
		Class that wraps the functionality for a single Natural Language Classifier
		This class assumes that the classifier has already been trained
	"""
	def __init__(self, username, password, classifier_id=None, classifier_url=None):
		if type(username) is not str or username == "":
			raise ValueError("Username provided is none or is not of proper type")
		elif type(password) is not str or password == "":
			raise ValueError("Password provided is none or is not of proper type")
		elif classifier_id is None and classifier_url is None:
			raise ValueError("Both the classifier id and the url is None. At least one of these must be provided")
		elif classifier_url is not None:
			resp = requests.get(classifier_url, headers={"Content-Type": "application/json"}, auth=(username, password))
			if resp.ok:
				json_obj = resp.json()
				self.username_ = username
				self.password_ = password
				self.classifier_url_ = classifier_url
				self.classifier_id_ = json_obj.get('classifier_id')
				self.classifier_name_ = json_obj.get('name')
				self.created_ = json_obj.get('created')
			else:
				raise resp.raise_for_status()
		else:
			self.username_ = username
			self.password_ = password
			gateway_url = 'https://gateway.watsonplatform.net/natural-language-classifier-experimental/api/v1/classifiers'
			resp = requests.get(gateway_url, headers={"Content-Type": "application/json"}, auth=(username, password))
			if resp.ok:
				classifier = [cls for cls in resp.json().get('classifiers') if cls.get('classifier_id') == classifier_id]
				if len(classifier) == 0:
					raise ValueError("No classifiers found with the id %r" % classifier_id)
				elif len(classifier) == 1:
					cls = classifier[0]
					self.classifier_url_ = cls.get('url')
					self.classifier_name_ = cls.get('name')
					self.created_ = cls.get('created')
					self.classifier_id_ = classifier_id
			else:
				raise resp.raise_for_status()

	def get_id(self):
		return self.classifier_id_

	def get_name(self):
		return self.classifier_name_

	def get_created_date(self):
		return self.created_

	def get_url(self):
		return self.classifier_url_

	def get_status(self):
		resp = requests.get(self.get_url(), headers={"Content-Type": "application/json"}, auth=(self.username_, self.password_))
		if resp.ok:
			return resp.json().get('status')
		else:
			raise ValueError("Unable to get classifier status")

	def get_status_description(self):
		resp = requests.get(self.get_url(), headers={"Content-Type": "application/json"}, auth=(self.username_, self.password_))
		if resp.ok:
			return resp.json().get('status_description')
		else:
			raise ValueError("Unable to get classifier status")

	def classify(self, text):
		if type(text) is not str or text == "":
			raise ValueError("Provided text is not of proper type or is empty")
		else:
			json_data = {"text": text}
			resp = requests.post(self.get_url(), data=json.dumps(json_data), headers={"Content-Type": "application/json"}, auth=(self.username_, self.password_))
			if resp.ok:
				return resp.json()
			else:
				raise resp.raise_for_status()


if __name__ == "__main__":
	sample_url = 'https://gateway.watsonplatform.net/natural-language-classifier-experimental/api'
	user = 'f57fac7d-a315-42af-8d8f-fc613a30c6ff'
	pw = 'BBLuwSp5WdHO'
	nlc_instance = NaturalLanguageClassifierInstance(user, pw, sample_url)
	print "Number of classifiers : %d" % len(nlc_instance.get_classifiers())
	sys.exit(0)
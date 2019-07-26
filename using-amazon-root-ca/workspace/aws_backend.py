#!/usr/bin/env python

import json
import os
import subprocess


class AwsiotViaShell:
	def __init__(self):
		self._caller_id = self._get_caller_id()
		self._region = self._get_region()
		self._list_policies = self._get_list_policies()

	@property
	def caller_id(self):
		return self._caller_id

	@property
	def region(self):
		return self._region

	@property
	def list_policies(self):
		return self._list_policies

	@staticmethod
	def _get_caller_id():
		subprocess.call(
			'aws sts get-caller-identity > .caller_id', shell=True
		)
		with open(".caller_id", "r") as caller_id_file:
			caller_id = json.load(caller_id_file)
		os.remove(".caller_id")

		return caller_id

	@staticmethod
	def _get_region():
		subprocess.call(
			'aws configure get region > .my_region',
			shell=True
		)
		with open(".my_region", "r") as region_file:
			region = region_file.read()
			region = region[:-1]
		os.remove(".my_region")

		return region

	@staticmethod
	def create_thing(thing_name):
		subprocess.call(
			'aws iot create-thing --thing-name "{0}" >> last.log'.format(thing_name),
			shell=True
		)

	@staticmethod
	def _get_list_policies():
		subprocess.call(
			'aws iot list-policies > .list_policies',
			shell=True
		)
		with open(".list_policies", "r") as list_policies_file:
			list_policies = json.load(list_policies_file)
		os.remove(".list_policies")

		return list_policies

	def _is_policy_exist(self, policy_name):
		if next(item for item in self.list_policies['policies'] if item["policyName"] == policy_name):
			return True
		else:
			return False

	def create_policy(self, policy_name, policy_document):
		if not self._is_policy_exist(policy_name):
			subprocess.call(
				'aws iot '
				'create-policy --policy-name "{0}" --policy-document file://{1} >> last.log'.format(policy_name, policy_document),
				shell=True
			)
		else:
			print("Warning: Using existing policy")

	@staticmethod
	def attach_thing_principal(thing_name, certificate):
		subprocess.call(
			'aws iot '
			'attach-thing-principal '
			'--thing-name {0} --principal {1} >> last.log'.format(str(thing_name), str(certificate['certificateArn'])),
			shell=True
		)

	@staticmethod
	def attach_policy_principal(policy_name, certificate):
		subprocess.call(
			'aws iot '
			'attach-principal-policy '
			'--policy-name {0} --principal {1} >> last.log'.format(str(policy_name), str(certificate['certificateArn'])),
			shell=True
		)

	def create_certificate_from_csr(self, csr_fingerprint_sha1):
		subprocess.call(
			'aws iot create-certificate-from-csr '
			'--region {0} '
			'--certificate-signing-request	file://{1}.csr '
			'--certificate-pem-outfile {2}.pem '
			'--set-as-active > .reg_cert'.format(self.region, csr_fingerprint_sha1, csr_fingerprint_sha1),
			shell=True
		)
		with open(".reg_cert", "r") as reg_cert_file:
			reg_certificate = json.load(reg_cert_file)
		os.remove(".reg_cert")

		return reg_certificate
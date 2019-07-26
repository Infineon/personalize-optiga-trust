#!/usr/bin/env python

import argparse
import json
import os
import base64
import sys
import glob
import hashlib
from aws_backend import AwsiotViaShell

from optigatrust.util.types import *
from optigatrust.pk import *
from optigatrust.x509 import *

private_key_slot_map = {
	'second': KeyId.USER_PRIVKEY_1,
	'0xE0E1': KeyId.USER_PRIVKEY_1,
	'0xE0F1': KeyId.USER_PRIVKEY_1,
	'third': KeyId.USER_PRIVKEY_2,
	'0xE0E2': KeyId.USER_PRIVKEY_2,
	'0xE0F2': KeyId.USER_PRIVKEY_2,
	'fourth': KeyId.USER_PRIVKEY_3,
	'0xE0E3': KeyId.USER_PRIVKEY_3,
	'0xE0F3': KeyId.USER_PRIVKEY_3
}

certificate_slot_map = {
	'second': ObjectId.USER_CERT_1,
	'0xE0E1': ObjectId.USER_CERT_1,
	'0xE0F1': ObjectId.USER_CERT_1,
	'third': ObjectId.USER_CERT_2,
	'0xE0E2': ObjectId.USER_CERT_2,
	'0xE0F2': ObjectId.USER_CERT_2,
	'fourth': ObjectId.USER_CERT_3,
	'0xE0E3': ObjectId.USER_CERT_3,
	'0xE0F3': ObjectId.USER_CERT_3
}


allowed_object_ids = [
	# Certificate Slots
	'0xe0e0', '0xe0e1', '0xe0e2', '0xe0e3',
	# Trust Anchor Slots
	'0xe0e8', '0xe0ef',
	# Arbitrary Data Objects
	'0xf1d0', '0xf1d1', '0xf1d2', '0xf1d3', '0xf1d4', '0xf1d5', '0xf1d6', '0xf1d7',
	'0xf1d8', '0xf1d9', '0xf1da', '0xf1db', '0xf1dc', '0xf1dd', '0xf1de',
	'0xf1e0', '0xf1e1'
]


def _break_apart(f, sep, step):
	return sep.join(f[n:n + step] for n in range(0, len(f), step))


def register_certificate(aws_instance, config_file, _slot):

	with open(config_file, "r") as csr_config:
		try:
			cfg = json.load(csr_config)
			cfg = cfg['csr_config']

			print("\nYour CSR configuration is following:\n{0}".format(json.dumps(cfg, sort_keys=True, indent=4)))

			if 'certificate_info' not in cfg:
				raise IOError("Your CSR configuration file should have a certificate_info field. Check out the example")
			if 'key_info' not in cfg:
				raise IOError("Your CSR configuration file should have a key_info field. Check out the example")
			if 'signature_info' not in cfg:
				raise IOError("Your CSR configuration file should have a signature_info field. Check out the example")
		except json.JSONDecodeError as err:
			raise IOError(
				"The config file incorrectly composed. Parser error. "
				"Unformated Message from parser: {0}".format(err.msg)
			)

	if _slot:
		if _slot not in private_key_slot_map:
			raise ValueError(
				"--slot has been used with wrong argument, allowed values {0}, you used {1}".
				format(private_key_slot_map, _slot)
			)
		_key_id_slot = private_key_slot_map[_slot]
	else:
		if cfg['key_info']['parameters']['slot'] not in private_key_slot_map:
			raise ValueError(
				"--slot has been used with wrong argument, allowed values {0}, you used {1}".
				format(private_key_slot_map, cfg['key_info']['parameters']['slot'])
			)
		_key_id_slot = private_key_slot_map[cfg['key_info']['parameters']['slot']]

	ecc_key = ecc.generate_keypair(cfg['key_info']['parameters']['curve'], _key_id_slot)

	builder = csr.Builder(cfg['certificate_info'], ecc_key)

	_csr_request = base64.b64encode(builder.build(ecc_key).dump())

	csr_request = '-----BEGIN CERTIFICATE REQUEST-----\n'
	csr_request += _break_apart(_csr_request.decode(), '\n', 64)
	csr_request += '\n-----END CERTIFICATE REQUEST-----'

	csr_fingerprint_sha1 = hashlib.sha1(_csr_request).hexdigest()

	with open(csr_fingerprint_sha1 + ".csr", "w+") as csr_file:
		csr_file.write(csr_request)

	aws_certificate = aws_instance.create_certificate_from_csr(csr_fingerprint_sha1)

	if not _slot:
		_id = cfg['key_info']['parameters']['slot']
	else:
		_id = _slot

	if _id not in certificate_slot_map:
		raise ValueError(
			"--id has been used with wrong argument, allowed values {0}, you used {1}".
			format(certificate_slot_map, _id)
		)
	_certificate_slot = certificate_slot_map[_id]

	cert.write_new(aws_certificate['certificatePem'], _certificate_slot)

	print("\nCertificate has been written:\n{0}".format(aws_certificate['certificatePem']))

	return aws_certificate


def register_thing_and_policy(aws_instance, config_file, aws_certificate):
	print("\nAttaching a thing and assigning a policy:\n")

	with open(config_file, "r") as aws_iot_config:
		try:
			cfg = json.load(aws_iot_config)
			cfg = cfg['aws_iot_config']

			print("\nYour AWS IoT configuration is following:\n{0}".format(json.dumps(cfg, sort_keys=True, indent=4)))

			if 'thing' not in cfg:
				raise IOError("Your AWS IoT configuration file should have a thing field. Check out the example")
			if 'policy' not in cfg:
				raise IOError("Your AWS IoT configuration file should have a policy field. Check out the example")
		except json.JSONDecodeError as err:
			raise IOError(
				"The config file incorrectly composed. Parser error. "
				"Unformated Message from parser: {0}".format(err.msg))

	aws_instance.create_thing(cfg['thing'])
	aws_instance.attach_thing_principal(cfg['thing'], aws_certificate)

	account_id = str(aws_instance.caller_id['Account'])
	region = str(aws_instance.region)

	this_file_directory = os.getcwd()
	policy_document = os.path.join(this_file_directory, 'my_policy.template')
	with open(policy_document, "r") as policy_document_file:
		policy_document = policy_document_file.read()

	# Replace Account ID and AWS Region
	policy_document = policy_document.replace('<aws-region>', region)
	policy_document = policy_document.replace('<aws-account-id>', account_id)
	with open("{0}.aws_iot_policy".format(cfg['policy']), "w") as policy_document_file:
		policy_document_file.write(policy_document)
		policy_document = "{0}.aws_iot_policy".format(cfg['policy'])

	aws_instance.create_policy(cfg['policy'], policy_document)
	aws_instance.attach_policy_principal(cfg['policy'], aws_certificate)

	print("\nYour OPTIGA(TM) Trust Sample has been successfully provisioned\n")


def user_config(max_number):
	# Calls for an infinite loop that keeps executing
	# until an exception occurs
	while True:
		try:
			test4num = int(input("Please select the required configuration:\n"))

		# If something else that is not the string
		# version of a number is introduced, the
		# ValueError exception will be called.
		except ValueError:
			# The cycle will go on until validation
			print("Error! This is not a number. Try again.")

		# When successfully converted to an integer,
		# the loop will end.
		else:
			if test4num <= max_number:
				break
			else:
				print("You have written a number out of range. Maximum is {0}", max_number)
	return test4num-1


def do_user_interface():
	files = glob.glob('*.jsn')

	print(
		"This is an script based OPTIGA(TM) Trust provisioning into user's AWS IoT Instance\n"
		"It will perform the following steps:\n"
		"1. Generate a Certificate Signing Request (CSR)\n"
		"2. Send the CSR to the preconfigured AWS IoT Instance\n"
		"3. Create a certificate out of CSR using AWS IoT instance as well activiating this certificate\n"
		"4. Receive the certificate from AWS\n"
		"5. Write back the certificate in the specified certificate slot on the security device\n"
		"6. Create a thing or attach an exisiting thing to the newly generated certificate\n"
		"7. Create a policy or attach an exisiting policy to the newly generated certificate\n"
	)

	print("Here are the configuration files in the directory:\n")
	for index, file in enumerate(files):
		print("{0}. {1}".format(index+1, file))

	config_number = user_config(len(files))

	aws_shell = AwsiotViaShell()

	aws_certificate = register_certificate(aws_shell, files[config_number], None)

	register_thing_and_policy(aws_shell, files[config_number], aws_certificate)


'''
#################################################################################################################
'''

parser = argparse.ArgumentParser(description="Communicate with your OPTIGA(TM) Trust sample")
group = parser.add_mutually_exclusive_group()
group.add_argument("-v", "--verbose", action="store_true")
group.add_argument("-q", "--quiet", action="store_true")
parser.add_argument(
	"--slot",
	default="second",
	choices=[
		# They all mean the same
		'second', '0xe0e1', '0xe0f1',
		'third', '0xe0e2', '0xe0f2',
		'fourth', '0xe0e3', '0xe0f3'
	],
	help="Use one the predefined slots; e.g. second, 0xe0e1, or 0xe0f1, they all mean the same"
)

parser.add_argument(
	"--cfg",
	metavar='CONFIG_FILE',
	help='1. Generate a Certificate Signing Request using the provided condig file\n'
	'2. Send it to preconfigures AWS IoT Instance\n'
	'3. Write resulting certificate into the chip'
)

args = parser.parse_args()

if args.cfg:
	if args.slot:
		slot = args.slot
	else:
		slot = None

	aws = AwsiotViaShell()

	registered_certificate = register_certificate(aws, args.cfg, slot)
	register_thing_and_policy(aws, args.cfg, registered_certificate)
	sys.exit(0)
else:
	do_user_interface()

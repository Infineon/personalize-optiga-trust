import argparse
import json
import base64
import hashlib
import sys
import binascii
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

object_slot_map = {
    '0xf1d0': ObjectId.DATA_TYPE1_0,
    '0xf1d1': ObjectId.DATA_TYPE1_1,
    '0xf1d2': ObjectId.DATA_TYPE1_2,
    '0xf1d3': ObjectId.DATA_TYPE1_3,
    '0xf1d4': ObjectId.DATA_TYPE1_4,
    '0xf1d5': ObjectId.DATA_TYPE1_5,
    '0xf1d6': ObjectId.DATA_TYPE1_6,
    '0xf1d7': ObjectId.DATA_TYPE1_7,
    '0xf1d8': ObjectId.DATA_TYPE1_8,
    '0xf1d9': ObjectId.DATA_TYPE1_9,
    '0xf1da': ObjectId.DATA_TYPE1_A,
    '0xf1db': ObjectId.DATA_TYPE1_B,
    '0xf1dc': ObjectId.DATA_TYPE1_C,
    '0xf1dd': ObjectId.DATA_TYPE1_D,
    '0xf1de': ObjectId.DATA_TYPE1_E,
    '0xf1e0': ObjectId.DATA_TYPE2_0,
    '0xf1e1': ObjectId.DATA_TYPE2_1
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


def parse_csr(_args):
    if not _args.csr:
        raise IOError('--csr command is used, but no config file provided. Exit.')

    with open(_args.csr, "r") as csr_config:
        try:
            cfg = json.load(csr_config)
            cfg = cfg['csr_config']

            if not _args.quiet or _args.verbose:
                print("\nYour configuration is following:\n{0}".format(json.dumps(cfg, sort_keys=True, indent=4)))
            if 'certificate_info' not in cfg:
                raise IOError("Your CSR configuration file should have a certificate_info field. Check out the example")
            if 'key_info' not in cfg:
                raise IOError("Your CSR configuration file should have a key_info field. Check out the example")
            if 'signature_info' not in cfg:
                raise IOError("Your CSR configuration file should have a signature_info field. Check out the example")
        except json.JSONDecodeError as err:
            raise IOError("The config file incorrectly composed. Parser error. "
                          "Unformated Message from parser: {0}".format(err.msg))

    if _args.slot:
        if _args.slot not in private_key_slot_map:
            raise ValueError("--slot has been used with wrong argument, allowed values {0}, you used {1}".
                             format(private_key_slot_map, _args.slot))
        _key_id_slot = private_key_slot_map[_args.slot]
    else:
        if cfg['key_info']['parameters']['slot'] not in private_key_slot_map:
            raise ValueError("--slot has been used with wrong argument, allowed values {0}, you used {1}".
                             format(private_key_slot_map, cfg['key_info']['parameters']['slot']))
        _key_id_slot = private_key_slot_map[cfg['key_info']['parameters']['slot']]

    ecc_key = ecc.generate_keypair(cfg['key_info']['parameters']['curve'], _key_id_slot)

    builder = csr.Builder(cfg['certificate_info'], ecc_key)

    _csr_request = base64.b64encode(builder.build(ecc_key).dump())

    csr_fingerprint_sha1 = hashlib.sha1(_csr_request).hexdigest()

    csr_request = '-----BEGIN CERTIFICATE REQUEST-----\n'
    csr_request += _break_apart(_csr_request.decode(), '\n', 64)
    csr_request += '\n-----END CERTIFICATE REQUEST-----'

    with open(csr_fingerprint_sha1 + ".csr", "w+") as csr_file:
        csr_file.write(csr_request)

    _return_value = {
        "filename": csr_fingerprint_sha1 + ".csr",
        "public_key": binascii.hexlify(bytearray(ecc_key.pkey)).decode()
    }

    if _args.query:
        if _args.query[0] not in _return_value:
            raise ValueError("The query argument is not within the available values. Available {0}, you gave {1}".
                             format(_return_value.keys(), _args.query))

        return_value = _return_value[_args.query[0]]
    else:
        return_value = _return_value

    sys.stdout.write(str(return_value))
    sys.stdout.flush()
    sys.exit(0)


def parse_write(_args):
    if not _args.write:
        raise IOError('--write command is used, but no data file provided. Exit.')

    if not _args.id:
        _id = 'second'
    else:
        _id = _args.id

    if _id not in certificate_slot_map:
        raise ValueError("--id has been used with wrong argument, allowed values {0}, you used {1}".
                         format(certificate_slot_map, _id))
    _certificate_slot = certificate_slot_map[_id]

    with open(_args.write, "r") as datafile:
        data = datafile.read()
        if not _args.quiet or _args.verbose:
            print("Your are going to write the following file:\n{0}".format(data))
        cert.write_new(data, _certificate_slot)

    if not _args.quiet or _args.verbose:
        print("Certificate has been written")


'''
#################################################################################################################
'''

parser = argparse.ArgumentParser(description="Communicate with your OPTIGA(TM) Trust sample")
group = parser.add_mutually_exclusive_group()
group.add_argument("-v", "--verbose", action="store_true")
group.add_argument("-q", "--quiet", action="store_true")
parser.add_argument("--query", nargs=1, metavar='QUERY_ARGUMENT',
                    help="Define the query argument you want to extract from the output")
parser.add_argument("--csr", metavar='CONFIG_FILE',
                    help="Instructs the script to generate a Certificate Signing Request."
                         "Give the script the configuration file for your CSR (fields like Common Name, "
                         "AWS IoT Thing Name, etc)")
parser.add_argument("--write", metavar='DATA_TO_WRITE', help="Write provided data to the chip.")
parser.add_argument("--read",
                    metavar='OBJECT_ID',
                    choices=allowed_object_ids,
                    help="Certificate Slots: 0xe0e0-0xe0e3\n"
                         "Trust Anchor slots: 0xe0e8 and 0xe0ef\n"
                         "100 bytes: 0xf1d0-0xf1de\n"
                         "1500 bytes: 0xf1e0, 0xf1e1")
parser.add_argument("--slot",
                    default="second",
                    choices=[
                        # They all mean the same
                        'second', '0xe0e1', '0xe0f1',
                        'third', '0xe0e2', '0xe0f2',
                        'fourth', '0xe0e3', '0xe0f3'
                    ],
                    help="Use one the predefined slots; e.g. second, 0xe0e1, or 0xe0f1, they all mean the same")
parser.add_argument("--id",
                    metavar='OBJECT_ID',
                    choices=allowed_object_ids,
                    help="USe to define which ID to use with your write command \n"
                         "Certificate Slots: 0xe0e0-0xe0e3\n"
                         "Trust Anchor slots: 0xe0e8 and 0xe0ef\n"
                         "100 bytes: 0xf1d0-0xf1de\n"
                         "1500 bytes: 0xf1e0, 0xf1e1")

args = parser.parse_args()

if args.csr:
    parse_csr(args)
    sys.exit(0)
if args.write:
    parse_write(args)
    sys.exit(0)
else:
    parser.print_help()
    sys.exit(0)




# Generate a Certificate Signing Request (CSR)

Prerequisites:
1. Connect your OPTIGA™ Trust sample to the OPTIGA™ Personalization Board
2. Download this repository

```bash
$ cd <path-to-personalize-optiga-trust>/using-amazon-root-ca/workspace

#Generates a CSR using Trust X secret key. The parameters of the CSR can be found in config.jsn
$ python ..\..\optiga.py --csr config_nistp256_ecdsa_secondslot.jsn	
```
* `--csr` Instructs the script to generate a Certificate Signing Request with a given config file as an input
* `--query` an optional parameter which can be used to output a specific field out of the output
* `--quit, -q` optional, don't output the user information

Here you have an option, either use one of prepared config files; e.g. `config_nistp256_ecdsa_secondslot.jsn`, or configure one based on your needs.
Note: For the ECDSA signature hash algorithm selection is based on the curev used< e.g. `secp256r1` means zou have to use `sha256`, for the `secp384r1` the `sha384` is the selection  

Example `config_nistp256_ecdsa_secondslot.jsn`:

```json
{
        "csr_config": {
                "certificate_info": {
                        "country_name": "DE",
                        "state_or_province_name": "Bayern",
                        "organization_name": "Infineon Technologies AG",
                        "common_name": "OPTIGA(TM) Trust IoT"
                },
                "key_info": {
                        "algorithm_id": "ec",
                        "parameters": {
                                "curve": "secp256r1",
                                "slot": "0xE0F1"
                        }
                },
                "signature_info": {
                        "algorithm_id": "ecdsa",
                        "parameters": {
                                "hash_alg": "sha256"
                        }
                }
        },
        "aws_iot_config": {
                "thing": "my_thing",
                "policy": "my_policy"
        }
}
```

* If you want to use another Object ID (Certificate/Private Key Slot) - modify the field "key_info"/"parameters"/"slot": "0xE0F1"
-> to the selected slot; e.g. "0xE0F1", "0xE0F2", "0xE0F3"
* If you want to use NIST P384 curve - modify the field "key_info"/"parameters"/"curve": "secp256r1" to "secp384r1", also you need to update the used hash algorithm -  "signature_info"/"parameters"/"hash_alg": "sha256" to "sha384"
* If you want to use another **Thing** or **Policy** consider changing names in the configuration file "aws_iot_config"/"thing": "my_thing" -> "my_new_thing", or "aws_iot_config"/"policy":"my_policy" -> "my_new_plicy". Moreover, the policy is generated based on the template 'my_policy.template', you can modify it based on your needs.

<details>
<summary>Expected output</summary>

```console
Your configuration is following:
{
    "certificate_info": {
        "common_name": "OPTIGA(TM) Trust IoT",
        "country_name": "DE",
        "organization_name": "Infineon Technologies AG",
        "state_or_province_name": "Bayern"
    },
    "key_info": {
        "algorithm_id": "ec",
        "parameters": {
            "curve": "secp256r1",
            "slot": "0xE0F1"
        }
    },
    "signature_info": {
        "algorithm_id": "ecdsa",
        "parameters": {
            "hash_alg": "sha256"
        }
    }
}
{'filename': '47478ea636328de8488a50236e79aa40720afc6f.csr', 'public_key': '0342000421d44d1bbe9f0357fc4ca506f38399c016457d0c3d419f284fd318c1ef7ef41b215e3a45570cb2700a1ba375fd4d6f1562f66afe519b4295e26b7a6bb432540b'}
```
</details>

***

A certificate signing request (CSR) wil be created. **Optionally**, perform a verification of the CSR to check that the public key matches the signature in the CSR. This action requires from you MSYS2/CygWIN/MinGW installation completed as well as having an openssl package installed.

```console
#Verfies the CSR.
$ openssl req -in <name-of-your-csr-eg-47478ea636328de8488a50236e79aa40720afc6f>.csr -noout -text -verify
```
<details>
<summary>Expected Output</summary>

```console
Certificate Request:
    Data:
        Version: 0 (0x0)
        Subject: C=DE, ST=Bayern, O=Infineon Technologies AG, CN=OPTIGA(TM) Trust IoT
        Subject Public Key Info:
            Public Key Algorithm: id-ecPublicKey
                Public-Key: (256 bit)
                pub:
                    04:21:d4:4d:1b:be:9f:03:57:fc:4c:a5:06:f3:83:
                    99:c0:16:45:7d:0c:3d:41:9f:28:4f:d3:18:c1:ef:
                    7e:f4:1b:21:5e:3a:45:57:0c:b2:70:0a:1b:a3:75:
                    fd:4d:6f:15:62:f6:6a:fe:51:9b:42:95:e2:6b:7a:
                    6b:b4:32:54:0b
                ASN1 OID: prime256v1
                NIST CURVE: P-256
        Attributes:
        Requested Extensions:
            X509v3 Basic Constraints:
                CA:FALSE
            X509v3 Extended Key Usage:
                TLS Web Server Authentication, TLS Web Client Authentication
            X509v3 Key Usage: critical
                Digital Signature, Key Encipherment
    Signature Algorithm: ecdsa-with-SHA256
         30:44:02:20:04:aa:6c:83:15:5c:89:46:bc:85:fb:9e:5b:b5:
         28:88:2d:59:c5:95:17:74:44:9f:a8:90:1e:0b:d4:8c:62:74:
         02:20:69:a1:7e:78:32:0d:87:d1:8d:61:07:90:88:10:c2:23:
         e0:ee:5a:5f:00:9c:a7:66:99:49:d8:79:c1:00:97:b8
verify OK
```
</details>

***

# Request a certificate from your self-signed CA with the CSR

```console
$ cd root/ca
$ openssl ca -config root_openssl.cnf -extensions usr_cert -policy policy_loose -in <name-of-your-csr-eg-47478ea636328de8488a50236e79aa40720afc6f>.csr -out <name-of-your-csr-eg-47478ea636328de8488a50236e79aa40720afc6f>.pem
```

<deatils>
<summary>Expected Output</summary>

```console
$ openssl ca -config root_openssl.cnf -extensions usr_cert -policy policy_loose -in f97a9ce0678f301db8d7e83730ca58ae59684391.csr -out f97a9ce0678f301db8d7e83730ca58ae59684391.pem -notext
Using configuration from root_openssl.cnf
Check that the request matches the signature
Signature ok
Certificate Details:
        Serial Number: 4096 (0x1000)
        Validity
            Not Before: Jul  4 18:06:00 2019 GMT
            Not After : Jul 13 18:06:00 2020 GMT
        Subject:
            countryName               = DE
            stateOrProvinceName       = Bayern
            organizationName          = Infineon Technologies AG
            commonName                = OPTIGA(TM) Trust IoT
        X509v3 extensions:
            X509v3 Basic Constraints:
                CA:FALSE
            Netscape Cert Type:
                SSL Client, S/MIME
            Netscape Comment:
                OpenSSL Generated Client Certificate
            X509v3 Subject Key Identifier:
                7F:AC:4D:BB:86:F3:74:69:EA:FD:34:FA:E2:0A:10:0A:B9:C0:30:7B
            X509v3 Authority Key Identifier:
                keyid:75:F6:8F:EB:32:B7:AB:33:58:79:59:33:35:9E:50:33:9C:29:D3:DC

            X509v3 Key Usage: critical
                Digital Signature, Non Repudiation, Key Encipherment
            X509v3 Extended Key Usage:
                TLS Web Client Authentication, E-mail Protection
Certificate is to be certified until Jul 13 18:06:00 2020 GMT (375 days)
Sign the certificate? [y/n]:y


1 out of 1 certificate requests certified, commit? [y/n]y
Write out database with 1 new entries
Data Base Updated
```
</details>

# Upload the resulting certificate on the OPTIGA™ Trust chip

```console
$python ../../../../optiga.py --write <name-of-your-csr-eg-47478ea636328de8488a50236e79aa40720afc6f>.pem --slot second
```
* `--write` Write provided data to the chip. In this case the certificate
* `--slot` Use one the predifined slots; e.g. `second`

<details>
<summary>Expected Output</summary>

```console
Your are going to write the following file:
-----BEGIN CERTIFICATE-----
MIIC0TCCAbmgAwIBAgIVALmaH1acmr608DlaqGY85JlQTh+nMA0GCSqGSIb3DQEB
CwUAME0xSzBJBgNVBAsMQkFtYXpvbiBXZWIgU2VydmljZXMgTz1BbWF6b24uY29t
IEluYy4gTD1TZWF0dGxlIFNUPVdhc2hpbmd0b24gQz1VUzAeFw0xOTA2MDUxNzQ2
MTBaFw00OTEyMzEyMzU5NTlaMGAxCzAJBgNVBAYTAkRFMQ8wDQYDVQQIDAZCYXll
cm4xITAfBgNVBAoMGEluZmluZW9uIFRlY2hub2xvZ2llcyBBRzEdMBsGA1UEAwwU
T1BUSUdBKFRNKSBUcnVzdCBJb1QwWTATBgcqhkjOPQIBBggqhkjOPQMBBwNCAASL
EB9ueiqRJy25snptYqV8FGJRt/sZGKAtVJYTks1jb/vPboKmxNtrQ7gYwxG6oRI2
zr7IxLZ6gehTUCD58Yzuo2AwXjAfBgNVHSMEGDAWgBTH2N2DqyO96bRF13DBcRjY
JCY9MDAdBgNVHQ4EFgQUqrD6FLnwLKAeCVtmqpRU4WVgLFEwDAYDVR0TAQH/BAIw
ADAOBgNVHQ8BAf8EBAMCB4AwDQYJKoZIhvcNAQELBQADggEBAFb/JMbxbBuG4FoY
ZngWz10yOHh0oE46EwZP4DsEXFhbdl30c+j70U65QM/6hyQCzakDodMYURcXUXkT
9OVRNRxQHXfYqdGl/v32Onl7GHp/I/ToftQWGIPeWu6dMzzdnPhm6P9npsQfKR39
vTcDEllVTX2iEwiXqSUnvfWVE/hr7/nTPsVeK3hD0jn42JEqYFBSZwICkG0E5kPc
yVSQe3x2jvPrp36+t3+m8elH5t1Vzx9uN2tyDxTVsc+iI9pe3IBdNtoRnmAeMyjA
UI5ieko2W26EsFNhEFRZwRO3KEker8WyxOPI6vPRQlhfz0bq2aUayVj3tB3DUKE5
rH5E17Q=
-----END CERTIFICATE-----

Certificate has been written

```
</details>

## Personalization completed
The Thing is successfully personalized. Move yout OPTIGA(TM) Trust to the AWS IoT edge for testing. 

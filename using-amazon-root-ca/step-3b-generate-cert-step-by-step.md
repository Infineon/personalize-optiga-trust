# Generate a Certificate Signing Request (CSR)

Prerequisites:
1. Connect your OPTIGA™ Trust sample to the OPTIGA™ Personalization Board
2. Download this repository

```bash
$ cd <path-to-personalize-optiga-trust>/using-amazon-root-ca/workspace

#Generates a CSR using Trust X secret key. The parameters of the CSR can be found in config.jsn
$ python ../../optiga.py --csr config_nistp256_ecdsa_secondslot.jsn	
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

# Request a certificate from your AWS IoT instance with the CSR

A Certificate Signing Request (CSR) contains a newly generated Public Key with matching Secret Key which is stored in OPTIGA™ Trust chip will be uploaded to AWS IoT.
The AWS IoT Core receives the CSR and will use the enclosed public key to verify against the signature.
Once verfied, AWS CA will issue a digital certificate. 
The digital certificate will be registered on AWS IoT registry and a copy of the certificate will be downloaded and store in Trust X Certificate slot. The personalization process by default stores the certificate slot in 0xE0E1.

**1. Checks the current endpoint address**
```console
$ aws iot describe-endpoint
{
    "endpointAddress": "XXXXXXXXXXXXX.iot.us-west-2.amazonaws.com"
}
```
***

**2. Gets the certificate ARN from us-west-2 server. Change to the appropriate server location. Record the ARN locally. ARN uniquely identifies the uploaded certificate.**
```console
$ aws iot create-certificate-from-csr --region <your-region-identifier-eg-us-west-2> --certificate-signing-request file://<name-of-your-csr-eg-47478ea636328de8488a50236e79aa40720afc6f>.csr --certificate-pem-outfile <name-of-your-csr-eg-47478ea636328de8488a50236e79aa40720afc6f>.pem --set-as-active --query certificateArn > optiga.aws_arn
```

In the end the file `<name-of-your-csr-eg-47478ea636328de8488a50236e79aa40720afc6f>.pem` will contain the resulting certificate which should be written back onto the chip

**3. Upload the resulting certificate on the OPTIGA™ Trust chip**

```console
#Upload the CSR, retrieve the digital certificate signed by AWS CA and stored in Trust X
$ python ..\..\optiga.py --write <name-of-your-csr-eg-47478ea636328de8488a50236e79aa40720afc6f>.pem --slot second
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

***
# Adding a Thing to AWS IoT Thing Registry

## In the nutshell

```console
#Creates a Thing in AWS Registry
$ aws iot create-thing --thing-name "IoT_Object_With_OPTIGA_Trust"

#Extract the ARN
$ export AWS_ARN=$(sed 's/.//;s/.$//' optiga.aws_arn)

#Confirm the value of the ARN
$ echo $AWS_ARN

#Attach the Thing with the certificate
$ aws iot attach-thing-principal --thing-name "IoT_Object_With_OPTIGA_Trust" --principal $AWS_ARN

#Create the Policy
$ aws iot create-policy --policy-name IoT_Thing_Weak_Policy --policy-document file://IoT_Thing_Weak_Policy

#Attach the Policy to the certificate
$ aws iot attach-principal-policy --policy-name "IoT_Thing_Weak_Policy" --principal $AWS_ARN
```
***


**1. Creates a Thing called “IoT_Object_With_OPTIGA_Trust” and register on AWS IoT Core Registry**

```console
#Creates a Thing in AWS Registry
$ aws iot create-thing --thing-name "IoT_Object_With_Trust_X"
```
<details>
<summary>Expected output:</summary>

```console
{
    "thingArn": "arn:aws:iot:us-west-2:065398228892:thing/IoT_Object_With_OPTIGA_Trust",
    "thingName": "IoT_Object_With_Trust_X",
    "thingId": "9208211e-9657-4e6c-84f5-56e1f26c9704"
}
```
</details>


***


**2. Creates a temporary variable that stores the ARN.**
Attach the Thing to the certificate.

```console
#Extract the ARN
$ export AWS_ARN=$(sed 's/.//;s/.$//' optiga.aws_arn)

#Confirm the value of the ARN
$ echo $AWS_ARN

#Attach the Thing with the certificate
$ aws iot attach-thing-principal --thing-name "IoT_Object_With_OPTIGA_Trust" --principal $AWS_ARN

```

***

**3. Create and attach the policy to a certificate.<br>**
_Note: This is a INSECURE policy and must be further fine-tune after initial configuration._

_Note: YOu should have a file named IoT_Thing_Weak_Policy in order to proceed here. The content might look like the following:_

```console
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": "iot:Connect",
            "Resource": "arn:aws:iot:<aws-region>:<aws-account-id>:*"
        },
        {
            "Effect": "Allow",
            "Action": "iot:Publish",
            "Resource": "arn:aws:iot:<aws-region>:<aws-account-id>:*"
        },
        {
            "Effect": "Allow",
            "Action": "iot:Subscribe",
            "Resource": "arn:aws:iot:<aws-region>:<aws-account-id>:*"
        },
        {
            "Effect": "Allow",
            "Action": "iot:Receive",
            "Resource": "arn:aws:iot:<aws-region>:<aws-account-id>:*"
        }
    ]
}
```

where the values <aws-region> and <aws-account> correspond to you AWS configuration. 
You can use the following commands to extract the region you use or the account-id

```console
# Get Your region
$ aws configure get region
eu-central-1
```
    
```console
# Get your Account ID
$ aws sts get-caller-identity
{
    "UserId": "Your-User-ID",
    "Account": "Your-Account-Id-use-it-for-policy",
    "Arn": "Your-arn-id"
}
```

```console
#Create the Policy
$ aws iot create-policy --policy-name IoT_Thing_Weak_Policy --policy-document file://IoT_Thing_Weak_Policy
```
<details>
<summary>Policy Details</summary>

```console
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": "iot:*",
      "Resource": "*"
    }
  ]
}
```
</details>

```console
#Attach the Policy to the certificate
$ aws iot attach-principal-policy --policy-name "IoT_Thing_Weak_Policy" --principal $AWS_ARN

```
<details>
<summary>Expected Output</summary>

```console
{
    "policyName": "IoT_Thing_Weak_Policy",
    "policyArn": "arn:aws:iot:us-west-2:065398228892:policy/IoT_Thing_Weak_Policy",
    "policyDocument": "{\n  \"Version\": \"2012-10-17\",\n  \"Statement\": [\n    {\n      \"Effect\": \"Allow\",\n      \"  }\n  ]\n}\n",
    "policyVersionId": "1"
}
```
</details>

***

## Personalization completed
The Thing is successfully personalized. Move yout OPTIGA™ Trust to the AWS IoT edge for testing. 

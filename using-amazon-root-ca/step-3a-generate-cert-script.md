# OPTIGA™ Trust chip provisioning in one script

The following actions are performed by the script, if you want to make it step-by-step please follow this [link](step-3b-generate-cert-step-by-step.md):
1. Generate a Certificate Signing Request (CSR)
2. Send the CSR to the preconfigured AWS IoT Instance
3. Create a certificate out of CSR using AWS IoT instance as well activiating this certificate
4. Receive the certificate from AWS
5. Write back the certificate in the specified certificate slot on the security device
6. Create a thing or attach an exisiting thing to the newly generated certificate
7. Create a policy or attach an exisiting policy to the newly generated certificate

Prerequisites:
1. Connect your OPTIGA™Trust sample to the OPTIGA™ Personalization Board
2. Download this repository

Simply start the script from the place you have prepared in the prevuous step

```bash
$ cd <path-to-personalize-optiga-trust>/using-amazon-root-ca/workspace
# 
$ python generate-cert-script.py
```

Here you have an option, either use one of prepared config files; e.g. `config_nistp256_ecdsa_secondslot.jsn`, or configure one based on your needs.

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
C:\Users\Yushev\git\ayushev\personalize-optiga-trust\using-amazon-root-ca\workspace>python generate-cert-script.py
This is an script based OPTIGA(TM) Trust provisioning into user's AWS IoT Instance
It will perform the following steps:
1. Generate a Certificate Signing Request (CSR)
2. Send the CSR to the preconfigured AWS IoT Instance
3. Create a certificate out of CSR using AWS IoT instance as well activiating this certificate
4. Receive the certificate from AWS
5. Write back the certificate in the specified certificate slot on the security device
6. Create a thing or attach an exisiting thing to the newly generated certificate
7. Create a policy or attach an exisiting policy to the newly generated certificate

Here are the configuration files in the directory:

1. config_nistp256_ecdsa_secondslot.jsn
2. config_nistp256_ecdsa_thirdslot.jsn
Please select the required configuration:
1

Your CSR configuration is following:
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

Certificate has been written:
-----BEGIN CERTIFICATE-----
MIIC0TCCAbmgAwIBAgIVAIjssxZeRn6VtTfx7CW6wJKgQx4sMA0GCSqGSIb3DQEB
CwUAME0xSzBJBgNVBAsMQkFtYXpvbiBXZWIgU2VydmljZXMgTz1BbWF6b24uY29t
IEluYy4gTD1TZWF0dGxlIFNUPVdhc2hpbmd0b24gQz1VUzAeFw0xOTA3MDExNDM4
MzVaFw00OTEyMzEyMzU5NTlaMGAxCzAJBgNVBAYTAkRFMQ8wDQYDVQQIDAZCYXll
cm4xITAfBgNVBAoMGEluZmluZW9uIFRlY2hub2xvZ2llcyBBRzEdMBsGA1UEAwwU
T1BUSUdBKFRNKSBUcnVzdCBJb1QwWTATBgcqhkjOPQIBBggqhkjOPQMBBwNCAARo
T8GdEKomHeBGYof2+lXB3S0VysUXbmhUC2jSWGhejdYiH781xIvKuXs+fclP97/r
WVmRqFimBMn622SQIh9uo2AwXjAfBgNVHSMEGDAWgBRG/va4JJyEpDgsrPXL65UI
007GODAdBgNVHQ4EFgQUTKu/FntsExJ+gFvq+24iANCHo8kwDAYDVR0TAQH/BAIw
ADAOBgNVHQ8BAf8EBAMCB4AwDQYJKoZIhvcNAQELBQADggEBAAKzehcVvKeez7yh
eL3wdUepMTV4GjQi2NPoNh1Jtf0G412/ktIxxBOnPVo4ZYq8yL6LOfn7U+2/sO97
ROVsnMp22QC91MQtF7XLPeADF5oyyDFmdHlz3k5F3N4HvXJcj6MuAbq3VWL/FaDh
xbuvcQ2qgk0VcLmhy/VvIeOwWjmU9TkYx/OTzmhKCmAh/D0WTnzYx8xvdc3jJrua
G8Vil/VAOoeWsgMy+xg8PNdO+Q40ZZ3GmEzg7BcC/aBglcu9noomWGiNMou+5qJK
KQjTL6mfix9b2iHp2GsHNn+vU01uu0gWSc1ycGowvkspsRwu0wb6ssLpKN3RDRh1
li2uXYA=
-----END CERTIFICATE-----


Attaching a thing and assigning a policy:


Your AWS IoT configuration is following:
{
    "policy": "my_policy",
    "thing": "my_thing"
}
Warning: Using existing policy

Your OPTIGA(TM) Trust Sample has been successfully provisioned
```
</details>

***

## Personalization completed
The Thing is successfully personalized. Move yout OPTIGA™ Trust to the AWS IoT edge for testing. 

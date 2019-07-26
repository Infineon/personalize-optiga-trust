# Personalize your OPTIGA™ Trust sample

* [Description](#description)
* [Required Hardware and Software](#required-hardware)
* [Summary](#summary)
* [X.509 Certificates and Private Keys on OPTIGA™ Trust](#x509-certificates-and-private-keys-on-optiga-trust)
* [PKI Options](#pki-options)
    * [Default](#default)
    * [Default with the Infineon Root ECC CA but with configurable X.509 End-Device certificates](#default-with-the-infineon-root-ecc-ca-but-with-configurable-x509-end-device-certificates)
    * [Cutomer CA](#cutomer-ca)
    * [Cloud Provider CA](#cloud-provider-ca)
    * [Infineon Intermediate CA at Customers AWS IoT Core Instance](#infineon-intermediate-ca-at-customers-aws-iot-core-instance)
* [Contributing](#contributing)
* [License](#license)

## Description

This repository contains one of Application Notes for [OPTIGA™ Trust X](https://github.com/Infineon/optiga-trust-x) and [OPTIGA™ Trust M](https://github.com/Infineon/optiga-trust-m) security chip.

* You can find more information about the security chip in the core repositories
  * [OPTIGA™ Trust X](https://github.com/Infineon/optiga-trust-x)
  * [OPTIGA™ Trust M](https://github.com/Infineon/optiga-trust-m)

## Required Hardware
For this application note you need to have:
* OPTIGA™ Trust Personalisation Board, alternativly you can use an FTDI FT260 equiped board, such as FTDI FT260S/Q(TSSOP/WQFN) USB-to-I2C bridge
* OPTIGA™ Trust X or M

## Summary
In this guide you may find the following examples:
* [Issue a certificate using Amazon Root CA](using-amazon-root-ca)
   * How to issue a certificate for an OPTIGA™ Trust sample using a Certificate Signing Requiest (CSR), Amazon Root CA and your AWS IoT instance
   * How to provision/register an OPTIGA™ Trust at your AWS IoT instance
* [Issue a certificate from a self-signed CA within your AWS IoT Instance](using-amazon-self-signed-ca)
   * How to issue your own self-signed CA certificate with OpenSSL
   * How to generate a Certificate Signing Request (CSR) with OPTIGA™ Trust and sign it with the CA
   * How to register your new CA on your AWS IoT Instance
   * How to generate an end-device certificate and write it back to one of available certificate slots on the device
* [Issue a certificate from a self-signed CA](using-amazon-and-self-signed-ca)
   * How to issue your own self-signed CA certificate with openSSL
   * How to generate a Certificate Signing Request (CSR) with OPTIGA™ Trust and sign it with the CA
   * How to generate an end-device certificate and write it back to one of available certificate slots on the device

## X.509 Certificates and Private Keys on OPTIGA™ Trust

![](https://github.com/Infineon/Assets/blob/master/Pictures/optiga_trust_m_and_trust_x.jpg)

Each OPTIGA™ Trust Secure Element has four certificate slots and four (six for the OPTIGA™ Trust M1) private key slots, **each certificate slot can carry up-to 1728 bytes of data, which means each slot can hold a chain of X.509 certificates**.

<details>
   <summary> <em> OPTIGA™ Trust X Objects Map </em> </summary>
   <img src="https://github.com/Infineon/Assets/raw/master/Pictures/optiga_trust_x_ac_metadata.png" >
</details>

More about OPTIGA™ Trust X Objects Map, Access Conditions, Metadata of Objects you may find [here](https://github.com/Infineon/optiga-trust-x/wiki/Metadata-and-Access-Conditions)

## PKI Options

There are many options available to personalize the security solution based on the **Order Volume** and the **Application Area**. Basic usecases are described below.

### Default

If not modified by a request, the default PKI setup is **always** applied. This means one ECC NIST P-256 X.509 End-Device certificate is provisioned in the first certificate slot (0xE0E0) and one assotiated private key is in the corresponding private key slot (0xE0F0).

This certificate and private key are implanted into the security chips at the secure Infineon environment.

<details>
<summary> <em> Default PKI Setup Scheme </em> </summary>
<img src="https://github.com/Infineon/Assets/blob/master/Pictures/optiga_trust_m_infineon_root_ca.jpg"  width=60% height=%60>
</details>

Below you might find a typical example of the end-device certificate (for a OPTIGA™ Trust X) which is pre-provisioned in the default PKI setup.
<details>
<summary> <em> A sample OPTIGA™  Trust X certificate parsed by OpenSSL </em>  </summary>


```console
Certificate:
    Data:
        Version: 3 (0x2)
        Serial Number: 16909066 (0x102030a)
    Signature Algorithm: ecdsa-with-SHA256
        Issuer: C=DE, O=Infineon Technologies AG, OU=OPTIGA(TM), CN=Infineon OPTIGA(TM) Trust X Test CA 000
        Validity
            Not Before: May 10 20:19:01 2016 GMT
            Not After : May  5 20:19:01 2036 GMT
        Subject:
        Subject Public Key Info:
            Public Key Algorithm: id-ecPublicKey
                Public-Key: (256 bit)
                pub:
                    04:a0:28:0e:73:9f:32:7a:8e:81:3b:5a:15:45:56:
                    64:97:43:dc:22:a6:03:63:84:6d:08:72:dd:bd:38:
                    8b:7c:c2:aa:62:25:13:0f:0f:0f:d5:73:d6:5b:fe:
                    07:66:77:0f:a3:a9:c6:31:5d:80:d3:76:14:32:15:
                    67:6b:6c:18:61
                ASN1 OID: prime256v1
                NIST CURVE: P-256
        X509v3 extensions:
            X509v3 Basic Constraints: critical
                CA:FALSE
            X509v3 Key Usage: critical
                Digital Signature
            X509v3 Certificate Policies:
                Policy: 1.2.276.0.68.1.20.1
            X509v3 Authority Key Identifier:
                keyid:42:E3:5D:56:E5:6C:8E:8D:02:71:8C:9E:F2:33:C9:47:3B:82:53:6C
    Signature Algorithm: ecdsa-with-SHA256
         30:44:02:20:1d:9c:64:5d:ed:af:c8:3b:16:58:a6:f1:d1:81:
         c4:52:52:cd:43:c0:2a:4d:70:a7:b1:17:64:24:84:0f:39:95:
         02:20:43:12:b7:b0:1d:61:28:2b:2f:6f:63:40:ed:b0:b0:d0:
         81:31:50:6b:a4:72:f3:a9:09:7c:2d:e3:28:fa:6d:99

```
</details>

For different products (OPTIGA™ Trust X and OPTIGA™ Trust M) different Intermdiate CAs are used. The Root CA stays the same. Below you may find all of them:
1. [OPTIGA™ ECC Root CA](https://github.com/Infineon/optiga-trust-x/blob/master/certificates/Infineon%20ECC%20Root%20CA%20C%20v01%2000.crt)
2. [OPTIGA™ Trust **X** Intermediate CA](https://github.com/Infineon/optiga-trust-x/blob/master/certificates/Infineon%20OPTIGA(TM)%20Trust%20X%20CA%20101.pem)
3. [OPTIGA™ Trust **M** Intermediate CA](https://github.com/Infineon/optiga-trust-m/blob/master/certificates/Infineon%20OPTIGA(TM)%20Trust%20M%20CA%20101.pem)

### Default with the Infineon Root ECC CA but with configurable X.509 End-Device certificates

The deafult PKI setup is taken, but a new Customer Intermediate CA is created based on customer requirements. All OPTIGA™ Trust chips then get a personalised End-Device Certificates based on this modified PKI.

### Cutomer CA

A Customer decideds to use its own PKI. In this case the flow is following:

1. Infineon generates a new keypair (public and **private keys**) for the customer
2. Infineon constructs a Certificate Signing request (CSR)
3. Infineon sends the CSR to the customer
4. The customer generates a new certificate based on the CSR 
5. The customer signs the certificate with the Customer CA private key
6. The customer sends the certificate back to Infineon.
7. Infineon saves this certificate along with the **private key** generated at step (1) as an Intermediate Customer CA 
8. All OPTIGA™ Trust chips preloaded with credentials issued by the Intermediate Customer CA and sign them with the **private key** generated at step (1)

<details>
<summary> <em> A figure showing the setup to make use of a customer CA </em> </summary>
<img src="https://github.com/Infineon/Assets/blob/master/Pictures/optiga_trust_m_customer_root_ca.jpg" width=60% height=%60>
</details>

<details>
<summary> <em> A figure showing the sequence diagram for the setup to make use of a customer CA </em>  </summary>
<img src="https://github.com/Infineon/Assets/blob/master/Pictures/optiga_trust_m_customer_root_ca_seq.jpg">
</details>

### Cloud Provider CA
    
A customer decides to use an Infrustructure provided by the Cloud Provider. Usually it's a provisioning not for a big volume, as it requires a lot of data exchange per sample. This Use case doesn't require Infineon and can be implemented by everybody. The instructions for the AWS IoT Core Cloud can be found [here](using-amazon-root-ca)

The flow is following:
1. The customer connects its PC/Embedded Linux to an OPTIGA™ Trust sample
2. The customer generates a keypair on the chip and exports the public key
3. The customer constructs a Certificate Signing request (CSR) (by means of a provided python engine)
4. The customer establishes a secure communication channel with a Cloud Provider; e.g. login/password
5. The customer sends the CSR to the customers Cloud Provider instance
6. The Cloud Provider signs this request with its own private key and sends it (a new certificate) back to the customer
7. The customer writes the certificate onto the OPTIGA™ Trust hardware in the corresponding to the private key generated at step (2)

<details>
<summary> <em> A figure showing the setup to make use of a Cloud Provider PKI </em> </summary>
<img src="https://github.com/Infineon/Assets/blob/master/Pictures/optiga_trust_m_cloud_ca.jpg" width=60% height=%60>
</details>

<details>
<summary> <em> A figure showing the sequence diagram for the setup to make use of a Cloud Provider PKI </em> </summary>
<img src="https://github.com/Infineon/Assets/blob/master/Pictures/optiga_trust_m_cloud_ca_seq.jpg">
</details>
  
### Infineon Intermediate CA at Customers AWS IoT Core Instance

A customer decides to provision all available OPTIGA™ Trust 

<details>
<summary> <em>  A figure showing the setup to make use of an Infineon Intermediate CA at the Cloud Provider PKI (AWS as an example) </em> </summary>
<img src="https://github.com/Infineon/Assets/blob/master/Pictures/optiga_trust_m_aws_reg_code_seq.jpg">
</details>

## Contributing
Please read [CONTRIBUTING.md](https://github.com/Infineon/optiga-trust-x/blob/master/CONTRIBUTING.md) for details on our code of conduct, and the process for submitting pull requests to us.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details

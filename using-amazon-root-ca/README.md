# Personalize your OPTIGA™ Trust sample using Amazon Root CA

## Required Hardware
For this application note you need to have:
* OPTIGA™ Trust Personalisation Board, alternativly you can use an FTDI FT260 equiped board, such as FTDI FT260S/Q(TSSOP/WQFN) USB-to-I2C bridge. __Note: This board isn't required if you use RPi__
* OPTIGA™ Trust X or M

## Summary
This guide demonstrates how to issue a certificate using Amazon Root CA and includes the following steps:
   * How to issue a certificate for an OPTIGA™ Trust sample using:
       * Certificate Signing Requiest (CSR)
       * One of Amazon Root CAs 
       * Your AWS IoT instance
   * How to provision/register an OPTIGA™ Trust at your AWS IoT instance

## X.509 Certificates and Private Keys on OPTIGA™ Trust

![](https://github.com/Infineon/Assets/blob/master/Pictures/optiga_trust_m_and_trust_x.jpg)

Each OPTIGA™ Trust Secure Element has four certificate slots and four (six for the OPTIGA™ Trust M1) private key slots, **each certificate slot can carry up-to 1728 bytes of data, which means each slot can hold a chain of X.509 certificates**.

<details>
   <summary> <em> OPTIGA™ Trust X Objects Map </em> </summary>
   <img src="https://github.com/Infineon/Assets/raw/master/Pictures/optiga_trust_x_ac_metadata.png" >
</details>

<details>
   <summary> <em> OPTIGA™ Trust M rev.1 Objects Map </em> </summary>
   <img src="https://github.com/Infineon/Assets/raw/master/Pictures/optiga_trust_m_datastore_overview_v3.jpg" >
</details>

More about OPTIGA™ Trust X Objects Map, Access Conditions, Metadata of Objects you may find [here](https://github.com/Infineon/optiga-trust-x/wiki/Metadata-and-Access-Conditions)

For available PKI options you can refer to the [main document](../README.md)

## Personalisation flow

**Note**
In most cases this type of provisioning isn't intenden for a big volume, as it requires a lot of data exchange per sample. 
This Use case doesn't require Infineon and can be implemented by everyone. 

The flow is following:
1. Connect PC/Embedded Linux to an OPTIGA™ Trust sample
2. Generate a keypair on the chip and export the public key
3. Construct a Certificate Signing request (CSR) (by means of a provided python engine)
4. Establish a secure communication channel with a Cloud Provider; e.g. login/password
5. Send the CSR to Amazon CA
6. Amazon CA signs this request with its own private key and sends it (a new certificate) back
7. Write the certificate onto the OPTIGA™ Trust hardware in the corresponding to the private key generated at step (2)

This flow can be done either via a single python script, or step-by-step.

<details>
<summary> <em> A figure showing the setup to make use of a AWS IoT PKI </em> </summary>
<img src="https://github.com/Infineon/Assets/blob/master/Pictures/optiga_trust_m_cloud_ca.jpg" width=60% height=%60>
</details>

<details>
<summary> <em> A figure showing the sequence diagram for the setup to make use of a AWS IoT PKI </em> </summary>
<img src="https://github.com/Infineon/Assets/blob/master/Pictures/optiga_trust_m_cloud_ca_seq.jpg">
</details>

## Start the personalization by following the first step: [AWS Account and Permission](step-1-aws-account-and-permissions.md)

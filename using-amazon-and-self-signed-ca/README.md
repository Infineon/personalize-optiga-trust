# Personalize your OPTIGA™ Trust sample using AWS and a user defined CA 

## Required Hardware
For this application note you need to have:
* OPTIGA™ Trust Personalisation Board, alternativly you can use an FTDI FT260 equiped board, such as FTDI FT260S/Q(TSSOP/WQFN) USB-to-I2C bridge
* OPTIGA™ Trust X or M

## Summary
Issue a certificate from a self-signed CA within your AWS IoT Instance
* How to issue your own self-signed CA certificate with OpenSSL
* How to generate a Certificate Signing Request (CSR) with OPTIGA™ Trust and sign it with the CA
* How to register your new CA on your AWS IoT Instance
* How to generate an end-device certificate and write it back to one of available certificate slots on the device

## X.509 Certificates and Private Keys on OPTIGA™ Trust

![](https://github.com/Infineon/Assets/blob/master/Pictures/optiga_trust_m_and_trust_x.jpg)

Each OPTIGA™ Trust Secure Element has four certificate slots and four (six for the OPTIGA™ Trust M1) private key slots, **each certificate slot can carry up-to 1728 bytes of data, which means each slot can hold a chain of X.509 certificates**.

<details>
   <summary> <em> OPTIGA™ Trust X Objects Map </em> </summary>
   <img src="https://github.com/Infineon/Assets/raw/master/Pictures/optiga_trust_x_ac_metadata.png" >
</details>

More about OPTIGA™ Trust X Objects Map, Access Conditions, Metadata of Objects you may find [here](https://github.com/Infineon/optiga-trust-x/wiki/Metadata-and-Access-Conditions)

For available PKI options you can refer to the [main document](../README.md)

## Personalisation flow

The flow is following:


This flow can be done either via a single python script, or step-by-step.

<details>
<summary> <em> A figure showing the setup to make use of  </em> </summary>
</details>

<details>
<summary> <em> A figure showing the sequence diagram for the setup to make use of  </em> </summary>
<img src="">
</details>

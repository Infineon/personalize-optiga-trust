# OPTIGA™ Trust M sample registration on AWS IoT

[Any](https://docs.aws.amazon.com/freertos/latest/userguide/freertos-prereqs.html) AWS IoT demo has common first steps.
These are:
1. Setting Up Your AWS Account and Permissions
2. Registering Your MCU Board with AWS IoT
3. Downloading FreeRTOS
4. Configuring the FreeRTOS Demos

If you choose to connect with the AWS IoT using pre-provisioned OPTIGA™ Trust secure element it slightly modifies the aformendtioned procedure, namely "Registering Your MCU Board with AWS IoT" and "Configuring the FreeRTOS Demos". All other steps remain the same.

The updated sections follow.

## 1. Registering Your MCU Board with AWS IoT

You can follow the [the generic guidelines](https://docs.aws.amazon.com/freertos/latest/userguide/get-started-freertos-thing.html), except for the subsection "To create an IoT thing, private key, and certificate for your device", the new content is described below:

1. Browse to the [AWS IoT console](https://console.aws.amazon.com/iotv2/).
1. In the navigation pane, choose **Manage**, and then choose **Things**.
1. If you do not have any IoT things registered in your account, the **You don't have any things yet** page is displayed. If you see this page, choose **Register a thing**. Otherwise, choose **Create**.
1. On the **Creating AWS IoT things** page, choose **Create a single thing**.
1. On the **Add your device to the thing registry** page, enter a name for your thing, and then choose **Next**.
1. Follow [the guideline](#appendix-registering-optiga-trust-on-aws-iot) below to register your secure element. After succesfull registration you should see a new certificate appear.
1. Select the certificate and choose **Attach a policy** to attach a policy to your certificate that grants your device access to AWS IoT operations.
1. Choose the policy you just created and choose **Register thing**.

## 2. Configuring the FreeRTOS Demos

You can skip the Section "To format your AWS IoT credentials", as the required credentials are already stored on the secure element in the required format.

Note: As part of this excersise, you need to update two pkcs#11 labels. The secure element uses then to understand which certificate and private keys to use for the actual secure communication. For this please update these two macroses `pkcs11configLABEL_DEVICE_PRIVATE_KEY_FOR_TLS`, `pkcs11configLABEL_DEVICE_CERTIFICATE_FOR_TLS` from `"0xE0F1"`, `"0xE0E1"` to 
`"0xE0F0"`, `"0xE0E0"` respectively. These macroses can be found in `aws_demos/config_files/iot_pkcs11_config.h` file 

## Appendix. Registering OPTIGA™ Trust on AWS IoT

### Option 1.  You DO have the certificate from your OPTIGA™ Trust

After you have successfuly passed the registration of your Shield2Go Board, you should have the ```certificate.pem``` file, which has a content similar to the one below

<details> 
 <summary><em> Sample certificate.pem file </em></summary>
  
```
-----BEGIN CERTIFICATE-----
MIIB2DCCAX6gAwIBAgIEMrfqdTAKBggqhkjOPQQDAjByMQswCQYDVQQGEwJERTEh
MB8GA1UECgwYSW5maW5lb24gVGVjaG5vbG9naWVzIEFHMRMwEQYDVQQLDApPUFRJ
R0EoVE0pMSswKQYDVQQDDCJJbmZpbmVvbiBPUFRJR0EoVE0pIFRydXN0IE0gQ0Eg
MTAxMB4XDTE5MDYxODA2MzAxMloXDTM5MDYxODA2MzAxMlowHDEaMBgGA1UEAwwR
SW5maW5lb24gSW9UIE5vZGUwWTATBgcqhkjOPQIBBggqhkjOPQMBBwNCAATMVR43
UAe5xlyhrr9dS2yqV72AhdlIfmGbAVmkJ+1eWpe129ffuYDNK1w89PGcLDNChwdK
6D4DXcOYMAsRXCobo1gwVjAOBgNVHQ8BAf8EBAMCAIAwDAYDVR0TAQH/BAIwADAV
BgNVHSAEDjAMMAoGCCqCFABEARQBMB8GA1UdIwQYMBaAFDwwjFzViuijXTKA5FSD
sv/Nhk0jMAoGCCqGSM49BAMCA0gAMEUCIQDI3Yqc2C/tiFb1K9Xuecy5WyGU6KQ2
zrmTnvTbO6Zw9gIgPplLHW8+wT0KcVajD5DLrfwBYz5DZIFDPBZFaXcndq0=
-----END CERTIFICATE-----
```
</details>

For the next step you need to make sure you have access to the [AWS IoT Multi-Account Registration Feature](https://pages.awscloud.com/iot-core-early-registration.html).
Register your certificate with the following command
```
aws iot register-certificate-without-ca --certificate-pem file://certificate.pem --status ACTIVE
```

### Option 2. You DON'T have the certificate from your OPTIGA™ Trust

If you don't have a way to get the certificate of your OPTIGA Trust M sample, but you do have one of the following kits
1. [OPTIGA™ Trust M evaluation kit](https://www.infineon.com/cms/en/product/evaluation-boards/optiga-trust-m-eval-kit/)

You can still get the certificate of your sample, for this you need to flash the kit with a prepared example (image file), and copy the output of the example in a `certificate.pem` file.
The steps are following:
1. Download missing components
  * Segger J-Link tool v6.00 or greater for flashing software on XMC. [Download for Windows, Linux, Mac](https://www.segger.com/downloads/jlink/#J-LinkSoftwareAndDocumentationPack)
  * [Tera Term](https://osdn.net/projects/ttssh2/releases/) (recommended)
2. Flash the binary
  * Power up the kit by connecting Micro USB cable between PC and Debugger micro USB (**X101** Port on the board).
  * Run JFlashLite.exe from JLink installation folder. It shows a notice window. Click OK.
  * Click on **Device** to select a target device
    * Select Infineon as Manufacturer and Device as XMC4800-2048, and then click OK
  * Select hex file (`bin/xmc4800_optiga_example.hex`) to be flashed under **Data File** and click on **Program Device**. It then shows the programming progress window.
  * Flash download completed
3. Get the output
  Connect the USB/Serial converter cable to the Infineon Shield2Go Adapter. This allows your board to send logging and debugging information in a form that you can view on your development machine. To set up a serial connection:

  * Connect the RX pin to your USB/Serial converter's TX pin.
  * Connect the TX pin to your USB/Serial converter's RX pin.
  * Connect your serial converter's ground pin to one of the GND pins on your board. The devices must share a common ground.

  Power is supplied from the USB debugging port, so do not connect your serial adapter's positive voltage pin to the board.

  Note
  Some serial cables use a 5V signaling level. The XMC4800 board and the Wi-Fi Click module require a 3.3V. Do not use the board's IOREF jumper to change the board's signals to 5V.

  With the cable connected, you can open a serial connection on a terminal emulator such as GNU Screen. The baud rate is set to 115200 by default with 8 data bits, no parity, and 1 stop bit.


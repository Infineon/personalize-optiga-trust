<a name="top"></a>

# Table of Content

* [Objectives](#objectives)
* [Setup preparation](#setup-preparation)
  * [Microsoft Windows 8/10](#microsoft-windows-810)
  * [Linux](#linux)
  * [Raspberry Pi 3](#raspberry-pi-3)
* [Configuration of the OpenSSL environment](#configuration-of-the-openssl-environment)
  * [Certificate Authority (CA) Preparation](#certificate-authority-ca-preparation)
  * [Create a Certificate Authority (CA)](#create-a-certificate-authority-ca)

# Objectives

The objective of this OPTIGA™ Trust personalization is to create a credential using a self-signed User CA. The credential consists of 2 parts namely the Public and Private Key. The Public Key must be authenticated using the CA. The CA will verifies the identity using the CSR process. After verification, a digital certificate signed by the CA will be generated. This digital certificate will be stored at OPTIGA™ Trust certificate slot.

In this example, we demonstrate a simple private own Certificate Authority (CA) setup where one had the ownership of a PKI with the capability to issue its own certificate. 

**Security Note:**
_It is a good security practice to use an intermediate certificate to provide an added level of security as the CA does not need to issue certificates directly from the CA root certificate. However, to easier the setup process, this is omitted._

In this setup guide, we will create a new Certificate Authority using OpenSSL. In order to illustrate this scenario, Windows MSYS2 environment is setup as a Certificate Authority. This is a one-time process and multiple certificates can be issued by the CA once it is setup. 

# Setup preparation

## Microsoft Windows 8/10

### Hardware Required
* An unlocked OPTIGA™ Trust X/M1 sample, [S2GO Security OPTIGA™ Trust X](https://www.infineon.com/cms/en/product/evaluation-boards/s2go-security-optiga-x/), or S2GO Security OPTIGA™ Trust M1 (link pending)
* OPTIGA™ Trust Personalisation Board or FTDI FT260S/Q(TSSOP/WQFN) USB-to-I2C bridge.
* FTDI D2XX Driver [Driver for Windows](https://www.ftdichip.com/Drivers/D2XX.htm)
* Windows 7 OS and above. Note: Windows XP is not supported.


### Environment Setup

_Note: in the following instruction, "#" is the comments within the console which explains the meaning of the following command. Meanwhile, "$" is the command prompt followed by the console command. Note that the "$" is not required to be entered as the command._

**1. Download and run the installer [Git Bash for Windows](https://gitforwindows.org/)**

---

**2. Download and run the installer [Python for Windows 3.7.x or older](https://www.python.org/downloads/windows/)**

_Note: After starting the installer, one of two options may be selected:_
![](https://github.com/Infineon/Assets/blob/master/Pictures/win_installer.png)

**_Note You need to make sure that both "Install pip and Add Python 3.x to PATH" options are applied"_**

* Use the following commands to verify that Python and pip are both installed correctly. Open Git Bash console
```bash
C:\> python --version
Python 3.7.1
C:\> pip3 --version
pip 18.1 from c:\program files\python37\lib\site-packages\pip (python 3.7)
``` 

---

**3. Install `optigatrust` Python module**

```console
# OPTIGA(TM) Trust Python package installation
$ pip3 install optigatrust
``` 

---


**4. Download this repository**
Either via git or a [direct download](https://github.com/ayushev/personalize-optiga-trust/archive/master.zip) (.zip file)

***

## Linux

### Hardware Required

* An unlocked OPTIGA™ Trust X/M1 sample, [S2GO Security OPTIGA™ Trust X](https://www.infineon.com/cms/en/product/evaluation-boards/s2go-security-optiga-x/), or S2GO Security OPTIGA™ Trust M1 (link pending)
* OPTIGA(TM) Trust Personalisation Board or FTDI FT260S/Q(TSSOP/WQFN) USB-to-I2C bridge.
* Tested in Ubuntu 16.04 LTS and similar concepts applies to other variant of Linux OS.

### Environment Setup

_Note: in the following instruction, "#" is the comments within the console which explains the meaning of the following command. Meanwhile, "$" is the command prompt followed by the console command. Note that the "$" is not required to be entered as the command._

_Note: for many system you need to run installation commands in a superuser mode. OYu can temporaly escalate your access right with the `sudo` prefix to those cpmmands_

* **1. Update your system**
  * type in the terminal window
  ```bash
  $ sudo apt-get update
  ``` 

---


* **2. libusb drivers**
   * _Note: Unplug and plugin your device (try out a differnt port in case of your the device isn#t recognised)_
   ```bash
   $ sudo apt-get install libusb-1.0-0-dev libusb-1.0-0
   ``` 

---


* **3. Python and pip**
  * Install Python and pip (Package Manager for Python) tools
  ```bash
  $ sudo apt-get install python3.7 python3-pip
  ```
  * Check your installation
  ```bash
  $ pip3 --version
  # Example output
  pip 19.0.1 from /usr/lib/python3/dist-packages (python 3.7)
  ``` 

---


* **4. OpenSSL engine**
  ```bash
  $ sudo apt-get install openssl
  ``` 

---


* **5. OPTIGA(TM) Trust* python package*
  * Install the *optigatrust* using pip.
  ```bash
  $ pip3 install optigatrust
  ``` 

---


* **6. Download this repository**
Either via git or a [direct download](https://github.com/ayushev/personalize-optiga-trust/archive/master.zip) (.zip file)


## Raspberry Pi 3

### Hardware Required

* An unlocked OPTIGA™ Trust X/M1 sample, [S2GO Security OPTIGA™ Trust X](https://www.infineon.com/cms/en/product/evaluation-boards/s2go-security-optiga-x/), or S2GO Security OPTIGA™ Trust M1 (link pending)
<details> 
 <summary><em> Connection Example </em></summary>
 <img src="https://github.com/Infineon/Assets/raw/master/Pictures/optiga_trust_x_rpi3_setup.jpg">
</details>

### Environment Setup

_Note: in the following instruction, "#" is the comments within the console which explains the meaning of the following command. Meanwhile, "$" is the command prompt followed by the console command. Note that the "$" is not required to be entered as the command._

_Note: for many system you need to run installation commands in a superuser mode. OYu can temporaly escalate your access right with the `sudo` prefix to those cpmmands_

* **1. Update your system**
  * type in the terminal window
  ```bash
  $ sudo apt-get update
  ```

---

* **2. Python and pip**
  * Install Python and pip (Package Manager for Python) tools
  ```bash
  $ sudo apt-get install python3.7 python3-pip
  ```
  * Check your installation
  ```bash
  $ pip3 --version
  # Example output
  pip 19.0.1 from /usr/lib/python3/dist-packages (python 3.7)
  ``` 

---


* **3. OpenSSL engine**
  ```bash
  $ sudo apt-get install openssl
  ``` 

---

* **4. OPTIGA™ Trust python package**
  * Install the *optigatrust* using pip.
  ```bash
  $ pip3 install optigatrust
  ``` 

---


* **5. Download this repository**
Either via git or a [direct download](https://github.com/ayushev/personalize-optiga-trust/archive/master.zip) (.zip file)

---

* **6. Configure I2C Interface**
<details>
<summary> Configure I2C Interface with raspi-config or manually </summary>
 
## Configuring I2C on the Raspberry Pi

This guide assumes that release 2015-01-31 or later of the Raspbian Operating
System is being used.

An I2C bus is broken out to pins 3 (SDA) and 5 (SCL) on the P1 header. The
number of steps that need to be performed to configure this I2C bus for usage
by user `pi` on Raspbian without root privileges is highly dependent in the
version of Raspbian being used.

### Configuring I2C with raspi-config (preferred)

With Raspbian Jessie 2015-11-21 or later the complete configuration can be
performed with the `raspi-config` software configuration tool which can be run
from a terminal window as follows:

```
sudo raspi-config
```

In the `raspi-config` user interface navigate to `Interfacing Options >> I2C`
and answer the question `"Would you like the ARM I2C interface to be enabled?"`
with `<Yes>`. After the next reboot user `pi` will be able to use the I2C bus
without root privileges.

### Configuring I2C Manually

On older versions of Raspbian (prior to Raspbian Jessie 2015-11-21) the
`raspi-config` tool can still be used to configure the I2C bus, but additional
steps typically need to be performed.

#### Step 1 - Enable I2C

To enable I2C ensure that `/boot/config.txt` contains the following line:

```
dtparam=i2c_arm=on
```

#### Step 2 - Enable user space access to I2C

To enable userspace access to I2C ensure that `/etc/modules` contains the
following line:

```
i2c-dev
```

#### Step 3 - Setting the I2C baudrate

The default I2C baudrate is 100000. If required, this can be changed with the
`i2c_arm_baudrate` parameter. For example, to set the baudrate to 400000, add
the following line to `/boot/config.txt`:

```
dtparam=i2c_arm_baudrate=400000
```

#### Step 4 - I2C access without root privileges

If release 2015-05-05 or later of the Raspbian Operating System is being used,
this step can be skipped as user `pi` can access the I2C bus without root
privileges.

If an earlier release of the Raspbian Operating System is being used, create a
file called `99-i2c.rules` in directory `/etc/udev/rules.d` with the following
content:

```
SUBSYSTEM=="i2c-dev", MODE="0666"
```

This will give all users access to I2C and sudo need not be specified when
executing programs using i2c-bus. A more selective rule should be used if
required.

#### Step 5 - Reboot the Raspberry Pi

After performing the above steps, reboot the Raspberry Pi.

</details>

---

* **7. Optionally select the i2c-bcm2708 I2C driver**
  If the output of the `uname -a` produces an output which show the Linux Kernel Version greater than 4.14 you might have the `i2c-bcm2835` I2C driver loaded by default. You can use `lsmod` command to see whther this is true for you. In this case you need to select another I2C driver `i2c-bcm2708`. You can do the following steps to perform the change

  ```bash
  $ sudo nano /boot/config.txt
  # add ‘dtoverlay=i2c-bcm2708’
  $ sudo reboot
  ```

  Check the change by calling `lsmod` once again. You should see `i2c-bcm2708` as a loaded module.

---

* **8. Create a softlink to the actually used i2c interface**
OPTIGA() Trust device is searching for `/dev/optiga_trust_i2c` device, thus you need to create a softlink pointing to it. In raspberry Pi3 if you don't have other i2c connected devices the i2c-1 interface can be taken.

  ```bash
  $ ln -s /dev/i2c-1 /dev/optiga_trust_i2c
***

# Configuration of the OpenSSL environment

## Certificate Authority (CA) Preparation
Prepare the Root-CA directory with the following sequence of commands (assuming you are in the root folder of the repository):

```console
#Setting up the CA structure. Should be executed from the personalize-optiga-trust/using-amazon-and-self-signed-ca folder
$ cd workspace && \
mkdir -p root/ca && \
cd root/ca && \
mkdir certs crl newcerts private && \
chmod 700 private && \
touch index.txt && \
chmod 777 index.txt && \
touch index.txt.attr && \
touch serial && \
chmod 777 serial && \
echo 1000 > serial
```

An OpenSSL Certificate Authority (CA) uses a configuration file to define its behavior. A sample of a configuration file, both for the root-CA and the intermediate-CA, is provided with in root_openssl.cnf file

Copy the root-configuration file with the following commands.

```console
#Copy the openssl configuration file to current folder. Take note of the period denoting current folder.
$ cp ../../root_openssl.cnf .
```

Verify the created directory structure

```console
#Display the current folder structure
$ ls -l
```

<details>
<summary>Expected Output</summary>

In general, a OpenSSL folder structure as seen below is created:

```console
$ tree ~/root
root
└── ca
    ├── certs
    ├── crl
    ├── index.txt
    ├── index.txt.attr
    ├── newcerts
    ├── private
    ├── root_openssl.cnf
    └── serial

5 directories, 4 files

```
</details>

## Create a Certificate Authority (CA)
The structure of the Root-CA is defined and a certificate for a functional CA is needed. First, the cryptographic root key pair is created. The key is stored in the file private/ca.key.pem. Then the private key is used to create a self-signed CA certificate ca.cert.pem. In a production environment, this pair of information, the Certificate and especially the private key must be stored securely. The private key can be password encrypted as shown below.

### Create a CA key pair and certificate
Generate the ECC keypair for the CA.

```console
#Generate a CA keypair.
$ openssl ecparam -name prime256v1 -genkey -out private/ca.key.pem
```

<details>
<summary>Expected Output</summary>

The newly generated private key should look similar to below:

```console
#Display the CA private key.
$ cat private/ca.key.pem
-----BEGIN EC PARAMETERS-----
BggqhkjOPQMBBw==
-----END EC PARAMETERS-----
-----BEGIN EC PRIVATE KEY-----
MHcCAQEEII10cC2NMOcE4H6gtuVB9gmPQ6VLnK63ZkVbrAFDUxynoAoGCCqGSM49
AwEHoUQDQgAECQb4x48GSDN+wMf42P/IE6UMFziqWvv00GBs75W9dYQIP4IICmMA
0eQWSMGEMRU3dtKe7+VVbMAHcErM4xw9sQ==
-----END EC PRIVATE KEY-----
```
</details>


Optionally, encrypt the CA private key with the following AES command. You will be prompted with a password. 
The original file can be removed. Subsequent, usage of the private key needs to be decrypted with the password.

```console
#Optionally encrypt the key pair with AES for secure local storage.
$ openssl enc -aes256 -in private/ca.key.pem -out private/ca.key.pem.enc

#Decrypt 
$ openssl aes256 -d -in private/ca.key.pem.enc -out private/ca.key.pem.dec
```

_Note: Going forward, ca.key.pem refers to the unencrypted CA private key._

Generates a self-signed CA certificate. The CA certificate contains the public key previously generated and self-signed by the corresponding private key.

```console
#Generate a self-sign CA certificate.
$ openssl req -config root_openssl.cnf -key private/ca.key.pem -new -x509 -days 7300 -sha256 -extensions v3_ca -out certs/ca.cert.pem

You are about to be asked to enter information that will be incorporated
into your certificate request.
What you are about to enter is what is called a Distinguished Name or a DN.
There are quite a few fields but you can leave some blank
For some fields there will be a default value,
If you enter '.', the field will be left blank.
-----
Country Name (2 letter code) [DE]:
State or Province Name [Germany]:
Locality Name []:
Organization Name [Infineon Technologies AG]:
Organizational Unit Name []:
Common Name []:
Email Address []:

#Display the content of CA certificate.
$ openssl x509 -noout -text -in certs/ca.cert.pem
```
***

**NEXT STEP: [Step 2. Generate a Certificate Signing Request ](https://github.com/ayushev/personalize-optiga-trust/blob/master/using-self-signed-ca/step-2-generate-new-cert-step-by-step.md)**

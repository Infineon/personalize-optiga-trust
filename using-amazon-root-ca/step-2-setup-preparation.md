<a name="top"></a>

# Table of Content

* [Objectives](#objectives)
* [Setup preparation](#setup-preparation)
  * [Microsoft Windows 8/10](#microsoft-windows-810)
  * [Linux](#linux)
  * [Raspberry Pi 3](#raspberry-pi-3)
* [Configuration of AWS Account using AWS CLI](#configuration-of-aws-account-using-aws-cli)

# Objectives

The objective of this Trust X personalization is to register the credential of an edge device on AWS IoT Registry. The credential consists of 2 parts namely the Public and Private Key. The Public Key must be authenticated using a CA. The CA will verifies the identity using the CSR process. After verification, a digital certificate signed by the CA will be generated. This digital certificate will be stored both at the AWS IoT Registry and Trust X certificate slot. The Public Key stored on the AWS Registry will be used to verify the identity of the edge node before establishing the secure connection.

Important:
The digital certificate used to identify the public key is stored in OID **0xE0E1** and the private key is stored in OID **0xE0F1**.

# Setup preparation

## Microsoft Windows 8/10

### Objectives

The objective of this Trust X personalization is to register the credential of an edge device on AWS IoT Registry. The credential consists of 2 parts namely the Public and Private Key. The Public Key must be authenticated using a CA. The CA will verifies the identity using the CSR process. After verification, a digital certificate signed by the CA will be generated. This digital certificate will be stored both at the AWS IoT Registry and Trust X certificate slot. The Public Key stored on the AWS Registry will be used to verify the identity of the edge node before establishing the secure connection.

Important:
The digital certificate used to identify the public key is stored in OID **0xE0E1** and the private key is stored in OID **0xE0F1**.

### Hardware Required
* An unlocked OPTIGA™ Trust X or [Infineon Trust X Shield2Go](https://www.infineon.com/cms/en/product/evaluation-boards/s2go-security-optiga-x/)
* OPTIGA™ Trust Personalisation Board or FTDI FT260S/Q(TSSOP/WQFN) USB-to-I2C bridge.
* FTDI D2XX Driver [Driver for Windows](https://www.ftdichip.com/Drivers/D2XX.htm)
* Windows 7 OS and above. Note: Windows XP is not supported.


### Environment Setup

* ## General requirements:
* **This repository**
   * You can directly download it using the download button on the [main page](../../../)
* **FTDI D2XX Direct [Drivers](https://www.ftdichip.com/Drivers/D2XX.htm)**
   * _Note: Unplug and plugin your device (try out a differnt port in case of your the device isn#t recognised)_
* **Python and pip**
  * To install Python and pip (Windows)
  * Download the Python Windows x86-64 installer from the downloads page of Python.org.
  * Run the installer.
  * Choose Add Python 3 to PATH.
  * Choose Install Now.
* **AWS Command Line Interface (CLI)**
  * Open the Command Prompt App from the Start menu
  * Use the following commands to verify that Python and pip are both installed correctly.
  ```bash
  C:\> python --version
  Python 3.7.1
  C:\> pip3 --version
  pip 18.1 from c:\program files\python37\lib\site-packages\pip (python 3.7)
  ```
  * Install the AWS CLI using pip.
  ```bash
  C:\> pip3 install awscli boto3
  ```
  * Verify that the AWS CLI is installed correctly.
  ```bash
  C:\> aws --version
  aws-cli/1.16.116 Python/3.6.8 Windows/10 botocore/1.12.106
  ```
* **OPTIGA™ Trust* python package**
  * Install the *optigatrust* using pip.
  ```bash
  C:\> pip3 install optigatrust
  ```

_**Note: The following instructions should be settled only once:**_

<details>

<summary> Add the AWS CLI Executable to Your Command Line Path </summary>

After installing the AWS CLI with pip, add the aws program to your operating system's PATH environment variable. With an MSI installation, this should happen automatically, but you might need to set it manually if the aws command doesn't run after you install it.

If this command returns a response, then you should be ready to run the tool. The where command, by default, shows where in the system PATH it found the specified program:

```bash
C:\> where aws
C:\Program Files\Amazon\AWSCLI\bin\aws.exe
```

You can find where the aws program is installed by running the following command.

```bash
C:\> where c:\ aws
C:\Program Files\Python37\Scripts\aws
```

If instead, the where command returns the following error, then it is not in the system PATH and you can't run it by simply typing its name.

```bash
C:\> where c:\ aws
INFO: Could not find files for the given pattern(s).
```

In that case, run the where command with the /R path parameter to tell it to search all folders, and look then you must add the path manually. Use the command line or Windows Explorer to discover where it is installed on your computer.

```bash
C:\> where /R c:\ aws
c:\Program Files\Amazon\AWSCLI\bin\aws.exe
c:\Program Files\Amazon\AWSCLI\bincompat\aws.cmd
c:\Program Files\Amazon\AWSCLI\runtime\Scripts\aws
c:\Program Files\Amazon\AWSCLI\runtime\Scripts\aws.cmd
...
```

The paths that show up depend on which method you used to install the AWS CLI.

Typical paths include:

* Python 3 and pip3 – C:\Program Files\Python37\Scripts\
* Python 3 and pip3 --user option on earlier versions of Windows – %USERPROFILE%\AppData\Local\Programs\Python\Python37\Scripts
* Python 3 and pip3 --user option on Windows 10 – %USERPROFILE%\AppData\Roaming\Python\Python37\Scripts

_Note_

Folder names that include version numbers can vary. The examples above reflect the use of Python version 3.7. Replace as needed with the version number you are using.

To modify your PATH variable (Windows):
* *Press the Windows key and enter environment variables.*
* *Choose Edit environment variables for your account.*
* *Choose PATH, and then choose Edit.*
* *Add the path to the Variable value field. For example: C:\new\path*
* *Choose OK twice to apply the new settings.*
* *Close any running command prompts and reopen the command prompt window.*

</details>


***

## Linux

### Hardware Required

* An unlocked OPTIGA™ Trust X or [Infineon Trust X Shield2Go](https://www.infineon.com/cms/en/product/evaluation-boards/s2go-security-optiga-x/)
* OPTIGA™ Trust Personalisation Board or FTDI FT260S/Q(TSSOP/WQFN) USB-to-I2C bridge.
* Tested in Ubuntu 16.04 LTS and similar concepts applies to other variant of Linux OS.

### Environment Setup

_Note: in the following instruction, "#" is the comments within the console which explains the meaning of the following command. Meanwhile, "$" is the command prompt followed by the console command. Note that the "$" is not required to be entered as the command._

_Note: for many system you need to run installation commands in a superuser mode. OYu can temporaly escalate your access right with the `sudo` prefix to those cpmmands_

* **Update your system**
  * type in the terminal window
  ```bash
  $ sudo apt-get update
  ```
* **libusb drivers**
   * _Note: Unplug and plugin your device (try out a differnt port in case of your the device isn#t recognised)_
   ```bash
   $ sudo apt-get install libusb-1.0-0-dev libusb-1.0-0
   ```
* **Python and pip**
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
* **AWS Command Line Interface (CLI)**
  * Install the AWS CLI using pip.
  ```bash
  $ pip3 install awscli
  ```
  * Verify that the AWS CLI is installed correctly.
  ```bash
  $ aws --version
  aws-cli/1.16.116
  ```
* **OPTIGA™ Trust* python package*
  * Install the *optigatrust* using pip.
  ```bash
  $ pip3 install optigatrust
  ```

***

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

* **3. AWS Command Line Interface (CLI)**
  * Install the AWS CLI using pip.
  ```bash
  $ pip3 install awscli
  ```
  * Verify that the AWS CLI is installed correctly.
  ```bash
  $ aws --version
  aws-cli/1.16.116
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
  If the output of the `uname -a` produces an output which show the Linux Kernel Version older than 4.14 you might have the `i2c-bcm2835` I2C driver loaded by default. You can use `lsmod` command to see whther this is true for you. In this case you need to select another I2C driver `i2c-bcm2708`. YOu can do the following steps to perform the change

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
  ```

***

# Configuration of AWS Account using AWS CLI


In order to perform any interaction with AWS cloud, the credential must be input using the aws configure command. Details of how to obtain those information can be found in the Quickly Configuring the AWS CLI link.

[External link: Quickly Configuring the AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-configure.html)

```bash
#Enters AWS CLI login credentials.
$ aws configure
AWS Access Key ID [None]: XXXXXXXXXXXXXXXXXXXX
AWS Secret Access Key [None]: XXXXXXXXXXXXX/XXXXXXX/XXXXXXXXXXXXXXXXX
Default region name [None]: XXXXXXXX
Default output format [None]: json
```

Once the credential is provided, you can check the current active region.

```console
#Get a description of the current connected endpoint
$ aws iot describe-endpoint
```

[Top](#top)

**NEXT STEP:**
* Step 3. Generate new certificate
  * [Option a: With a single script](https://github.com/ayushev/personalize-optiga-trust/blob/master/using-amazon-root-ca/step-3a-generate-cert-script.md)
  * [Option b: Using step-by-step guidance](https://github.com/ayushev/personalize-optiga-trust/blob/master/using-amazon-root-ca/step-3b-generate-cert-step-by-step.md)

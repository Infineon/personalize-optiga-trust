## I get `OSError: Failed to initialise the chip. Exit`

If you have this python exception, it means one of the following:
* **Hardware connection**. If you use Shield2Go the red LED should be on and all the lines (SDA, SCL, VCC, GND, RST) should be connected
* **Python version**. Currently it should be 3.7+ all scrypts should be called either via python3 directly or via python if it points to the correct version of python
  * Note. Raspberry Pi 3 doesn't have Python 3.7 by default, you can follow this guidance to install it https://github.com/instabot-py/instabot.py/wiki/Installing-Python-3.7-on-Raspberry-Pi
* **Raspbian Kernel Version**. If the output of the `uname -a` produces an output which shows the Linux Kernel Version newer than 4.14 you might have the `i2c-bcm2835` I2C driver loaded by default. You can use `lsmod` command to see whether this is true for you. In this case you need to select another I2C driver `i2c-bcm2708`. You can do the following steps to perform the change

  ```bash
  $ sudo nano /boot/config.txt
  # add ‘dtoverlay=i2c-bcm2708’
  $ sudo reboot
  ```

  Check the change by calling `lsmod` once again. You should see `i2c-bcm2708` as a loaded module.

## I get `OSError: Failed to initialise the chip. Exit`

If you have this python exception, it means one of the following:
* **Hardware connection**. If you use Shield2Go the red LED should be on and all the lines (SDA, SCL, VCC, GND, RST) should be connected
* **Python version**. Currently it should be 3.7+ all scrypts should be called either via python3 directly or via python if it points to the correct version of python
  * Note. Raspberry Pi 3 doesn't have Python 3.7 by default, you can follow this guidance to install it https://github.com/instabot-py/instabot.py/wiki/Installing-Python-3.7-on-Raspberry-Pi


# PYTHON

The keyboard HMI needs to run as root because it listen to all keyboard events:

$ sudo python3 py-keyboard-hmi/main.py



# RASBERRY

Connect to rasberry via Wireless:

$ nmap 192.168.206.0-255
$ ssh pi@192.168.206.212 

seems that 192.168.x.212 is taken by rasberry py on maken-net


Connect to raberry via Ethernet (no DHCP server)
The rasberryPi use link-local, if the dhcp server is not found.
So, if you connect the rasberry to your local computer, you may use:
(make sure your local computer also use link-local)

ssh pi@169.254.241.43

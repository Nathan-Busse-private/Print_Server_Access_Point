# I need help creating a print server project using a raspberry pi 1
# Let me explain:
#______________________________________________________________________________________________________________________________


# Why I Am making this Raspberry Pi 1 model A print server:
#----------------------------------------------------------

# I can't install drivers for my HP Smart Tank 581 All-in-one printer as my windows installer v5.0 is malfunctioning. 

# I know what's the problem and it cannot be fixed without formatting the c drive completely as 
# v5.0 has no redistributable file.  

# I don't want to format and install windows 7 again as there is a lot of sensitive data on the drive and, 
# it is nearly a 13 year old laptop. 

# This is just a work around until, I can afford a new laptop.


# Objectives:
#--------------------------------------------

# Must utilize the CUPS open-source printing system as well as samba aswell as a custom python scrip.
# The HP Smart Tank 580 - 590 series printers is able to distribute and execute 
# print jobs from devices connected to the same network as the printer,
# which is achieved thanks to the printers utilizing I.P.P ( Internet Print Protocol ) 

# The continuity of my printer setup on ALL client device OS's should be maintained even if the Raspberry Pi
# experiences interruptions and restarts due to power loss.

# The Python script must manage and create the print server which transfers the print jobs to printer through the network.

# If the script is interrupted by any means it must cancel and ignore any print incomming or stored queues and
# cancel any active print job if the scrit is interrupted and or the printer loses power in the middle of printing a page
# to avoid print jams and other hardware failure caused by power failure.

# Script must auto start upon boot.

# The printserver must be discovered by network and is compatible with all platforms including windows 7.

# The script must colab with "cups open-source printing system" as well as samba setup

# The client is not required to install printer drivers

# The raspberry pi is connected via ethernet

# The printer communicates with the raspberry pi through the network via ipp.

# All clients as well as the raspberry pi and printer are connected to the same network.

# The raspberry pi print server must be dicovered over network displaying using its hostname as the device name instead of displaying the printer name.

# I am using python 3.9.2

# I plan on using pycups module

# I will provide my current script for you to work off of and modify without removing current features of the script I have provided to you. 




# Why I went with Web Services on Devices (WSD) protocol, I have no clue....

# How I realized my HP Smart Tank 581 All-in-one printer utilizes I.P.P:
#-----------------------------------------------------------------------

# -It connects to our Routor and its IP and port csn be seen in the router's Gateway.
# -Any device connected to the same netwotk as the printer can access the printer.
# -A print server can be created by using a Raspberry Pi 1 model A running a custom 
#  Python script to manage and create the print server which transfers the print jobs to printer through the network.
# -The Raspberry Pi 1 model A is connected to the router via an ethernet connection.
# -The HP Smart Tank 581 All-in-one printer communicates with the Raspberry Pi 1 model A wirelessly because 
#  the printer is connected to the router's network.
# -To put it simply the Raspberry Pi 1 model A is essentialy an Access Point between 
#  devices and the printer that share the same network.


# Hostname Commands
#-------------------

# hostname: printserver
# hostname -I: 192.168.0.120

# Names, Addresses and connection
#---------------------------------

# Raspberry Pi Hostname: printserver
# Raspberry Pi_IPv4_address: 192.168.0.120
# Printer_IPv4_address: 192.168.0.102
# CUPS_web_UI_URL: https://printserver:631
# Queue name: HP_Smart_Tank_580-590_series
# Connection: ipps://HP%20Smart%20Tank%20580-590%20series%20%5BF8FE59%5D._ipps._tcp.local/

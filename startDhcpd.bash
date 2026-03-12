#! /bin/bash -x

# This script setup and start the isc-dhcp-server
# This can be usefull to connect device as rasberrypi on the laptop directly

# set the static ip addr used by the dhcpd server
sudo ip addr flush dev enp0s31f6
sudo ip addr add 192.168.2.1/24 dev enp0s31f6

# in the isc-dhcp-server config need to have the interface where the server will listen
# eg: in /etc/default/isc-dhcp-server
# INTERFACESv4="enp0s31f6"


# The dhcpd server need also to be configure properly
# eg: /etc/dhcp/dhcpd.conf 
# subnet 192.168.2.0 netmask 255.255.255.0 {
#    range 192.168.2.100 192.168.2.200;
#    default-lease-time 600;
#    max-lease-time 7200;
#}


# start the dhcp service
sudo systemctl restart isc-dhcp-server

# check the status
sudo systemctl status isc-dhcp-server

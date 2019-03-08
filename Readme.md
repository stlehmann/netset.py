# Netset.py

A Network configuration tool for the commandline.

## Features

* create network configuration profiles
* change quickly between different network configurations
* access current network status
* fast access from commandline

## Usage

**You need administrative rights on your PC in order to change the network settings.**

### Create a static network profile

```
c:\> netset add myprofile --ip 192.168.1.110 -m 255.255.255.0 -g 192.168.1.1
```

Creates a new network profile named myprofile with the following configuration:

* ip address: 192.168.1.110
* subnetmask: 255.255.255.0
* gateway: 192.168.1.1

### Create s dynamic network profile with DHCP

```
c:\> netset add dhcp --dhcp
```

Creates a new network profile with DHCP enabled.

### List available profiles

```
c:\> netset ls

Name      IP-Address     Subnetmask     Gateway
--------  -------------  -------------  -----------
dhcp*     DHCP           -              -
myconfig  192.168.1.110  255.255.255.0  192.168.1.1
```

List all available network profiles.


### Load a network profile

```
c:\> netset load myconfig
Successfully changed to config "myconfig".

Current Network Status:

IP: 192.168.1.110
Subnetmask: 255.255.255.0
Gateway: 192.168.1.1
```

### Show the current network status

```
c:\> netset status

Current Network Status:

IP: 192.168.1.110
Subnetmask: 255.255.255.0
Gateway: 192.168.1.1
```

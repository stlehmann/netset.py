# Netset.py

A Network configuration tool for the commandline.

## Features

* create network configuration profiles
* change quickly between different network configurations
* access current network status
* fast access from commandline

## Usage


### Create a static network profile

```
c:\> netset.py add myprofile --ip 192.168.1.110 -m 255.255.255.0 -g 192.168.1.1
```

Creates a new network profile named myprofile with the following configuration:

* ip address: 192.168.1.110
* subnetmask: 255.255.255.0
* gateway: 192.168.1.1

### Create s dynamic network profile with DHCP

```
c:\> netset.py add static --dhcp
```

Creates a new network profile with DHCP enabled.

### List available profiles

```
c:\> netset.py list

Name      IP-Address     Subnetmask     Gateway
--------  -------------  -------------  -----------
dhcp*     DHCP           -              -
myconfig  192.168.1.110  255.255.255.0  192.168.1.1
```

List all available network profiles.


### Load a network profile

```
c:\> netset.py load myconfig
Successfully changed to config "myconfig".

Current Network Status:

IP: 192.168.1.110
Subnetmask: 255.255.255.0
Gateway: 192.168.1.1
```

### Show the current network status

```
c:\> netset.py status

Current Network Status:

IP: 192.168.1.110
Subnetmask: 255.255.255.0
Gateway: 192.168.1.1
```
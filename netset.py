#! c:\miniconda\python
from collections import namedtuple
import time
import sys
import click
import wmi

TIMEOUT_SECONDS = 120

# static configuration
Config = namedtuple('Config', 'name dhcp ip subnetmask gateway')

configs = {
    'dhcp': Config('dhcp', True, None, None, None),
    'static': Config('static', False, '192.168.1.110', '255.255.255.0', '192.168.1.0')
}

def get_nic():
    nic_configs = wmi.WMI().Win32_NetworkAdapterConfiguration(IPEnabled=True)
    nic = nic_configs[0]
    return nic


def ip_address(nic):
    ip = nic.wmi_property('IPAddress')
    return ip.value[0]


def subnetmask(nic):
    subnet = nic.wmi_property('IPSubnet')
    return subnet.value[0]


def gateway(nic):
    gateway = nic.wmi_property('DefaultIPGateway')
    return gateway.value[0]

def dhcp_enabled(nic):
    dhcp = nic.wmi_property('DHCPEnabled')
    return dhcp.value


def config_active(config):
    nic = get_nic()
    if config.dhcp:
        return dhcp_enabled(nic)
    return (config.ip == ip_address(nic) and
            config.subnetmask == subnetmask(nic) and
            config.gateway == gateway(nic))

@click.group()
def cli():
    pass


@cli.command()
def list():
    """ list available network configurations """
    nic = get_nic()
    for key, config in configs.items():
        active = config_active(config)
        s = '{token} {x.name}: {x.ip}'.format(
            token='>' if active else ' ', x=config)
        click.echo(s)


@cli.command()
def status():
    """ show current network status """
    s = 'DHCP\n' if dhcp_enabled() else ''
    s += ('IP: {ip}\nSubnetmask: {subnetmask}\n'
           'Gateway: {gateway}'.format(
                ip=ip_address(),
                subnetmask=subnetmask(),
                gateway=gateway()
            ))
    click.echo(s)


@cli.command()
@click.argument('config')
def load(config):
    config_name = config
    config = configs[config]
    nic = get_nic()
    if config.dhcp:
        nic.EnableDHCP()
    else:
        nic.EnableStatic(IPAddress=[config.ip],SubnetMask=[config.subnetmask])
        nic.SetGateways(DefaultIPGateway=[config.gateway])

    t0 = time.perf_counter()

    while not abs(time.perf_counter() - t0) > TIMEOUT_SECONDS:
        if config_active(config):
            click.echo('Successfully changed to config "{}".'.format(config_name))
            break
        time.sleep(1)
    else:
        click.echo('Timeout')


if __name__ == '__main__':
    cli()
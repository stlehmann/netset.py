#! python
from collections import namedtuple
from tabulate import tabulate
import os
import time
import click
import wmi
import pickle


__version__ = "0.0.3"

TIMEOUT_SECONDS = 120
CONFIG_FILENAME = "netset.pkl"


# Save list function
list_ = list


# static configuration
Config = namedtuple("Config", "name dhcp ip subnetmask gateway")
configs = {
    "dhcp": Config("dhcp", True, None, None, None),
    "static": Config("static", False, "192.168.1.110", "255.255.255.0", "192.168.1.0"),
}


def get_nic():
    nic_configs = wmi.WMI().Win32_NetworkAdapterConfiguration(IPEnabled=True)
    nic = nic_configs[0]
    return nic


def ip_address(nic):
    ip = nic.wmi_property("IPAddress")
    return ip.value[0]


def subnetmask(nic):
    subnet = nic.wmi_property("IPSubnet")
    return subnet.value[0]


def gateway(nic):
    gateway = nic.wmi_property("DefaultIPGateway")
    try:
        return gateway.value[0]
    except TypeError:
        return


def dhcp_enabled(nic):
    dhcp = nic.wmi_property("DHCPEnabled")
    return dhcp.value


def config_active(config):
    nic = get_nic()
    if config.dhcp:
        return dhcp_enabled(nic)
    return (
        config.ip == ip_address(nic)
        and config.subnetmask == subnetmask(nic)
        and config.gateway == gateway(nic)
    )


def get_active_configs():
    nic = get_nic()

    active_dhcp = dhcp_enabled(nic)
    active_ip = ip_address(nic)
    active_subnetmask = subnetmask(nic)
    active_gateway = gateway(nic)

    for key, config in configs.items():
        if active_dhcp and config.dhcp:
            yield config.name
        else:
            if (active_ip, active_subnetmask, active_gateway) == (
                config.ip,
                config.subnetmask,
                config.gateway,
            ):
                yield config.name


def save_configs():
    global configs
    with open(CONFIG_FILENAME, "wb") as f:
        pickle.dump(configs, f)


@click.group()
def cli():
    pass


@cli.command()
@click.argument("name")
@click.option("--dhcp", is_flag=True, help="dhcp on")
@click.option("--ip", "-i", help="ip address")
@click.option("--mask", "-m", help="subnet mask")
@click.option("--gateway", "-g", help="gateway")
def add(name, dhcp, ip, mask, gateway):
    """Add a configuration."""
    global configs
    new_cfg = Config(name, dhcp, ip, mask, gateway)
    configs[name] = new_cfg
    save_configs()


@cli.command()
@click.argument("name")
def rm(name):
    """Remove a config from list."""
    global configs
    configs.pop(name)
    save_configs()


@cli.command()
def ls():
    """List configurations."""
    active_configs = list_(get_active_configs())

    def list_data(x):
        active = "*" if x.name in active_configs else ""
        if x.dhcp:
            return "{}{}".format(x.name, active), "DHCP", "-", "-"
        else:
            return "{}{}".format(x.name, active), x.ip, x.subnetmask, x.gateway

    """ list available network configurations """
    headers = ["Name", "IP-Address", "Subnetmask", "Gateway"]
    table = [list_data(x) for _, x in configs.items()]
    click.echo("\nNetset Profiles:\n")
    click.echo(tabulate(table, headers))


def _status():
    nic = get_nic()
    s = "DHCP\n" if dhcp_enabled(nic) else ""
    s += "IP: {ip}\nSubnetmask: {subnetmask}\n" "Gateway: {gateway}".format(
        ip=ip_address(nic), subnetmask=subnetmask(nic), gateway=gateway(nic)
    )
    click.echo("\nCurrent Network Status:\n")
    click.echo(s)


@cli.command()
def status():
    """Show current network status."""
    _status()


@cli.command()
@click.argument("config")
def load(config):
    """Load a configuration."""
    config_name = config
    config = configs[config]
    nic = get_nic()
    if config.dhcp:
        nic.EnableDHCP()
    else:
        nic.EnableStatic(IPAddress=[config.ip], SubnetMask=[config.subnetmask])
        nic.SetGateways(DefaultIPGateway=[config.gateway])

    t0 = time.perf_counter()

    while not abs(time.perf_counter() - t0) > TIMEOUT_SECONDS:
        if config_active(config):
            click.echo('Successfully changed to config "{}".'.format(config_name))
            _status()
            break
        time.sleep(1)
    else:
        click.echo("\nTimeout")


def main():
    """Entrypoint."""
    global configs
    config_filepath = CONFIG_FILENAME
    if os.path.isfile(config_filepath):
        with open(config_filepath, "rb") as f:
            configs = pickle.load(f)

    cli()


if __name__ == "__main__":
    main()

#! /usr/bin/env python
"""
Class with REST Api GET and POST libraries

Example: python rest_api_lib.py vmanage_hostname username password

PARAMETERS:
    vmanage_hostname : Ip address of the vmanage or the dns name of the vmanage
    username : Username to login the vmanage
    password : Password to login the vmanage

Note: All the three arguments are manadatory
"""
import requests
import sys
import json
import click
import os
import tabulate
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

SDWAN_IP = os.environ.get("SDWAN_IP")
SDWAN_USERNAME = os.environ.get("SDWAN_USERNAME")
SDWAN_PASSWORD = os.environ.get("SDWAN_PASSWORD")

if SDWAN_IP is None or SDWAN_USERNAME is None or SDWAN_PASSWORD is None:
    print("CISCO SDWAN details must be set via environment variables before running.")
    print("   export SDWAN_IP=10.10.30.190")
    print("   export SDWAN_USERNAME=admin")
    print("   export SDWAN_PASSWORD=admin")
    print("")
    exit("1")

class rest_api_lib:
    def __init__(self, vmanage_ip, username, password):
        self.vmanage_ip = vmanage_ip
        self.session = {}
        self.login(self.vmanage_ip, username, password)

    def login(self, vmanage_ip, username, password):
        """Login to vmanage"""
        base_url_str = 'https://%s:8443/'%vmanage_ip

        login_action = '/j_security_check'

        #Format data for loginForm
        login_data = {'j_username' : username, 'j_password' : password}

        #Url for posting login data
        login_url = base_url_str + login_action
        url = base_url_str + login_url

        sess = requests.session()
        #If the vmanage has a certificate signed by a trusted authority change verify to True
        login_response = sess.post(url=login_url, data=login_data, verify=False)

    
        if b'<html>' in login_response.content:
            print ("Login Failed")
            sys.exit(0)

        self.session[vmanage_ip] = sess

    def get_request(self, mount_point):
        """GET request"""
        url = "https://%s:8443/dataservice/%s"%(self.vmanage_ip, mount_point)
        #print url
        response = self.session[self.vmanage_ip].get(url, verify=False)
        data = response.content
        return data

    def post_request(self, mount_point, payload, headers={'Content-Type': 'application/json'}):
        """POST request"""
        url = "https://%s:8443/dataservice/%s"%(self.vmanage_ip, mount_point)
        payload = json.dumps(payload)
        print (payload)

        response = self.session[self.vmanage_ip].post(url=url, data=payload, headers=headers, verify=False)
        data = response.json()
        return data

sdwanp = rest_api_lib(SDWAN_IP, SDWAN_USERNAME, SDWAN_PASSWORD)

@click.group()
def cli():
    """Command line tool for deploying templates to CISCO SDWAN.
    """
    pass

@click.command()
def device_list():
    """Retrieve and return network devices list.

        Returns information about each device that is part of the fabric.

        Example command:

            ./sdwan.py device_list

    """
    click.secho("Retrieving the devices.")

    response = json.loads(sdwanp.get_request('device'))
    items = response['data']

    headers = ["Host-Name", "Device Type", "Device ID", "System IP", "Site ID", "Version", "Device Model"]
    table = list()

    for item in items:
        tr = [item['host-name'], item['device-type'], item['uuid'], item['system-ip'], item['site-id'], item['version'], item['device-model']]
        table.append(tr)
    try:
        click.echo(tabulate.tabulate(table, headers, tablefmt="fancy_grid"))
    except UnicodeEncodeError:
        click.echo(tabulate.tabulate(table, headers, tablefmt="grid"))

@click.command()
def template_list():
    """Retrieve and return templates list.

        Returns the templates available on the vManage instance.

        Example command:

            ./sdwan.py template_list

    """
    click.secho("Retrieving the templates available.")

    response = json.loads(sdwanp.get_request('template/device'))
    items = response['data']

    headers = ["Template Name", "Device Type", "Template ID", "Attached devices", "Template version"]
    table = list()

    for item in items:
        tr = [item['templateName'], item['deviceType'], item['templateId'], item['devicesAttached'], item['templateAttached']]
        table.append(tr)
    try:
        click.echo(tabulate.tabulate(table, headers, tablefmt="fancy_grid"))
    except UnicodeEncodeError:
        click.echo(tabulate.tabulate(table, headers, tablefmt="grid"))

@click.command()
@click.option("--template", help="Name of the template you wish to retrieve information for")
def attached_devices(template):
    """Retrieve and return devices associated to a template.

        Example command:

            ./sdwan.py attached_devices --template abcd1234567890

    """

    url = "template/device/config/attached/{0}".format(template)

    response = json.loads(sdwanp.get_request(url))
    items = response['data']
    
    headers = ["Host Name", "Device IP", "Site ID", "Host ID", "Host Type"]
    table = list()

    for item in items:
        tr = [item['host-name'], item['deviceIP'], item['site-id'], item['uuid'], item['personality']]
        table.append(tr)
    try:
        click.echo(tabulate.tabulate(table, headers, tablefmt="fancy_grid"))
    except UnicodeEncodeError:
        click.echo(tabulate.tabulate(table, headers, tablefmt="grid"))

@click.command()
@click.option("--template", help="Name of the template to deploy")
@click.option("--target", help="Hostname of target network device.")
@click.option("--hostname", help="Hostname you wish the target has")
@click.option("--sysip", help="System IP you wish the target has")
@click.option("--loopip", help="Loopback interface IP address")
@click.option("--geip", help="Gigabit0/0 interface IP address")
@click.option("--siteid", help="Site ID")
#@click.argument("parameters", nargs=-1)
def attach(template, target, hostname, sysip, loopip, geip, siteid):
    """Attach a template with Cisco SDWAN.

        Provide all template parameters and their values as arguments.

        Example command:

          ./sdwan.py attach --template TemplateID --target TargetID --hostname devnet01.cisco.com 
          --sysip 1.1.1.1 --loopip 2.2.2.2/24 --geip 3.3.3.3/24 --siteid 999
    """
    click.secho("Attempting to attach template.")

    payload = {
        "deviceTemplateList":[
        {
            "templateId":str(template),       
            "device":[ 
            {
                "csv-status":"complete",
                "csv-deviceId":str(target),
                "csv-deviceIP":str(sysip),
                "csv-host-name":str(hostname),
                "/1/loopback1/interface/ip/address":str(loopip),
		        "/0/ge0/0/interface/ip/address":str(geip),
                "//system/host-name":str(hostname),
                "//system/system-ip":str(sysip),
                "//system/site-id":str(siteid),
                "csv-templateId":str(template),
                "selected":"true"
            }
            ],
            "isEdited":"false", 
            "isMasterEdited":"false" 
        }
        ]
    }

    response = sdwanp.post_request('template/device/config/attachfeature', payload)
    print (response)

@click.command()
@click.option("--target", help="ID of the  to detach")
@click.option("--sysip", help="System IP of the system to detach")
def detach(target, sysip):
    """Detach a template with Cisco SDWAN.

        Provide all template parameters and their values as arguments.

        Example command:

          ./sdwan.py detach --target TargetID --sysip 1.1.1.1
    """
    click.secho("Attempting to detach template.")

    payload = {
        "deviceType":"vedge",
        "devices":[  
            {
                "deviceId":str(target),
                "deviceIP":str(sysip)
            }
        ]
    }

    response = sdwanp.post_request('template/config/device/mode/cli', payload)
    print (response)

cli.add_command(attach)
cli.add_command(detach)
cli.add_command(device_list)
cli.add_command(attached_devices)
cli.add_command(template_list)

if __name__ == "__main__":
    cli()
   
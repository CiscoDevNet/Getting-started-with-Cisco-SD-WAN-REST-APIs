# Getting started with Cisco SD-WAN REST APIs

The Cisco SD-WAN Solution (a.k.a Viptela) is a cloud-delivered overlay WAN architecture that facilitates digital and cloud transformation for enterprises. It significantly reduces WAN costs and time to deploy new services.

Cisco SD-WAN builds a robust security architecture that's crucial for hybrid networks. It provides a strong policy framework.

The solution has been deployed in every major industry. It solves many critical enterprise problems, including:

* Establishing transport-independent WAN for lower cost and higher diversity
* Meeting SLA for business-critical and real-time applications
* Providing end-to-end segmentation for protecting critical enterprise compute resources
* Extending seamlessly into the public cloud
* Providing optimal user experience for SaaS applications

### Project SD-WAN

The goals of this application are two fold. First is to show how simple it is to
develop applications that extend the Cisco SD-WAN fabric by using the REST API
it provides. Second is to help IT operations teams that are managing Cisco SD-WAN fabrics to make the transition to an automated and programmable infrastructure.

The main application is a CLI tool through which users can see a list of the devices that are part of the fabric, the configuration templates, which devices are associated to which templates, and options to attach and detach configuration templates to specific devices.

Example usage:

`./sdwan.py attach --template TemplateID --target TargetID --hostname
devnet01.cisco.com    --sysip 1.1.1.1 --loopip 2.2.2.2/24 --geip
3.3.3.3/24 --siteid 999`

### Requirements

To use this application you will need:

* Python 3.6+
* Cisco SD-WAN 18+
* A Cisco SD-WAN account with permissions to attach and detach templates

### Install and Setup

Clone the code to your local machine.

```
git clone https://github.com/ai-devnet/Getting-started-with-Cisco-SD-WAN-REST-APIs.git
cd Getting-started-with-Cisco-SD-WAN-REST-APIs
```

Setup Python Virtual Environment (requires Python 3.6+)

```
python3.6 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Setup local environment variables for your Cisco SD-WAN fabric. Provide the info for your Cisco SD-WAN environment.

Examples:

```
export SDWAN_IP=10.10.30.190
export SDWAN_USERNAME=admin
export SDWAN_PASSWORD=admin
```

### Using the application

Once installed and setup, you can now get started.

Investigate the built-in help with the tool.

`./sdwan.py --help`

OUTPUT

```
Usage: sdwan.py [OPTIONS] COMMAND [ARGS]...

  Command line tool for deploying templates to CISCO SDWAN.

Options:
  --help  Show this message and exit.

Commands:
  attach            Attach a template with Cisco SDWAN.
  attached_devices  Retrieve and return devices associated to a...
  detach            Detach a template with Cisco SDWAN.
  device_list       Retrieve and return network devices list.
  template_list     Retrieve and return templates list.
```

Look at the available templates. Each template will provide the number of devices already attached and the template ID.

`./sdwan.py template_list`

OUTPUT

```
Retrieving the templates available.

| Template Name        | Device Type   | Template ID                          |   Attached devices |   Template version |
|----------------------|---------------|--------------------------------------|--------------------|--------------------|
| VEDGE_BASIC_TEMPLATE | vedge-cloud   | 72babaf2-68b6-4176-92d5-fa8de58e19d8 |                  0 |                 15 |
```

Retrieve the list of devices that make up the SD-WAN fabric with ./sdwan.py device_list.

`$ ./sdwan.py device_list`

OUTPUT

```
Retrieving the devices.

| Host-Name   | Device Type   | Device ID                            | System IP   |   Site ID | Version   | Device Model   |
|-------------|---------------|--------------------------------------|-------------|-----------|-----------|----------------|
| vmanage     | vmanage       | 4854266f-a8ad-4068-9651-d4e834384f51 | 4.4.4.90    |       100 | 18.3.1.1  | vmanage        |
| vsmart      | vsmart        | da6c566f-eb5f-4731-a89a-ff745661027c | 4.4.4.70    |       100 | 18.3.0    | vsmart         |
| vbond       | vbond         | 455407de-9327-467e-a0d2-d3444659dbb2 | 4.4.4.80    |       100 | 18.3.1    | vedge-cloud    |
| vedge01     | vedge         | 4af9e049-0052-47e9-83af-81a5825f7ffe | 4.4.4.60    |       200 | 18.3.1    | vedge-cloud    |
| vedge02     | vedge         | f3d4159b-4172-462c-9c8d-8db76c31521d | 4.4.4.61    |       300 | 18.3.1    | vedge-cloud    |
| vedge03     | vedge         | 100faff9-8b36-4312-bf97-743b26bd0211 | 4.4.4.62    |       400 | 18.3.1    | vedge-cloud    |
| vedge04     | vedge         | 46c18a49-f6f3-4588-a49a-0b1cc387f179 | 4.4.4.63    |       500 | 18.3.1    | vedge-cloud    |
```

Attaching a template is as easy as calling the *attach* option of the application and passing in the requested parameters.

`./sdwan.py attach --template TemplateID --target TargetID --hostname devnet01.cisco.com --sysip 1.1.1.1 --loopip 2.2.2.2/24 --geip 3.3.3.3/24 --siteid 999`

To detach a template from a specific device you need to call the detach option of the application and pass in the parameters for the target device ID and the system-ip of that device:

`./sdwan.py detach --target TargetID --sysip 1.1.1.1`

### POSTMAN

I've also included a POSTMAN environment and collection in the `postman` folder.

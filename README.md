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

`./sdwan.py attach --template db4c997a-7212-4ec1-906e-ed2b86c3f42f --variables Site-3-vEdge-Variables.yaml`

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
export vManage_IP=10.10.20.90
export vManage_PORT=8443
export vManage_USERNAME=admin
export vManage_PASSWORD=C1sco12345
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
  attached-devices  Retrieve and return devices associated to a...
  detach            Detach a template with Cisco SDWAN.
  device-list       Retrieve and return network devices list.
  template-list     Retrieve and return templates list.
```

Look at the available templates. Each template will provide the number of devices already attached and the template ID.

`./sdwan.py template-list`

OUTPUT

```
Retrieving the templates available.
╒═════════════════════════════╤═════════════════╤══════════════════════════════════════╤════════════════════╤════════════════════╕
│ Template Name               │ Device Type     │ Template ID                          │   Attached devices │   Template version │
╞═════════════════════════════╪═════════════════╪══════════════════════════════════════╪════════════════════╪════════════════════╡
│ vSmart_Template             │ vsmart          │ 90f26d2d-8136-4414-84de-4e8df52374e6 │                  1 │                  9 │
├─────────────────────────────┼─────────────────┼──────────────────────────────────────┼────────────────────┼────────────────────┤
│ Site_1_and_2_cEdge_Template │ vedge-CSR-1000v │ c566d38e-2219-4764-a714-4abeeab607dc │                  2 │                 13 │
├─────────────────────────────┼─────────────────┼──────────────────────────────────────┼────────────────────┼────────────────────┤
│ Site_3_vEdge_Template       │ vedge-cloud     │ db4c997a-7212-4ec1-906e-ed2b86c3f42f │                  1 │                 13 │
├─────────────────────────────┼─────────────────┼──────────────────────────────────────┼────────────────────┼────────────────────┤
│ DC_cEdge_Template           │ vedge-CSR-1000v │ 24d4be69-8038-48a3-b546-c6df199b6e29 │                  1 │                 14 │
╘═════════════════════════════╧═════════════════╧══════════════════════════════════════╧════════════════════╧════════════════════╛
```

Retrieve the list of devices that make up the SD-WAN fabric with ./sdwan.py device-list.

`$ ./sdwan.py device-list`

OUTPUT

```
Retrieving the devices.
╒═══════════════╤═══════════════╤══════════════════════════════════════════╤═════════════╤═══════════╤════════════════╤═════════════════╕
│ Host-Name     │ Device Type   │ Device ID                                │ System IP   │   Site ID │ Version        │ Device Model    │
╞═══════════════╪═══════════════╪══════════════════════════════════════════╪═════════════╪═══════════╪════════════════╪═════════════════╡
│ vmanage       │ vmanage       │ 81ac6722-a226-4411-9d5d-45c0ca7d567b     │ 10.10.1.1   │       101 │ 19.2.2         │ vmanage         │
├───────────────┼───────────────┼──────────────────────────────────────────┼─────────────┼───────────┼────────────────┼─────────────────┤
│ vsmart        │ vsmart        │ f7b49da3-383e-4cd5-abc1-c8e97d345a9f     │ 10.10.1.5   │       101 │ 19.2.2         │ vsmart          │
├───────────────┼───────────────┼──────────────────────────────────────────┼─────────────┼───────────┼────────────────┼─────────────────┤
│ vbond         │ vbond         │ ed0863cb-83e7-496c-b118-068e2371b13c     │ 10.10.1.3   │       101 │ 19.2.2         │ vedge-cloud     │
├───────────────┼───────────────┼──────────────────────────────────────────┼─────────────┼───────────┼────────────────┼─────────────────┤
│ dc-cedge01    │ vedge         │ CSR-61CD2335-4775-650F-8538-4EC7BDFFD04C │ 10.10.1.11  │       100 │ 16.12.3.0.3752 │ vedge-CSR-1000v │
├───────────────┼───────────────┼──────────────────────────────────────────┼─────────────┼───────────┼────────────────┼─────────────────┤
│ site1-cedge01 │ vedge         │ CSR-807E37A3-537A-07BA-BD71-8FB76DE9DC38 │ 10.10.1.13  │      1001 │ 16.12.3.0.3752 │ vedge-CSR-1000v │
├───────────────┼───────────────┼──────────────────────────────────────────┼─────────────┼───────────┼────────────────┼─────────────────┤
│ site2-cedge01 │ vedge         │ CSR-DE6DAB19-BA1A-E543-959C-FD117F4A6205 │ 10.10.1.15  │      1002 │ 16.12.3.0.3752 │ vedge-CSR-1000v │
├───────────────┼───────────────┼──────────────────────────────────────────┼─────────────┼───────────┼────────────────┼─────────────────┤
│ site3-vedge01 │ vedge         │ 0140a336-5fd5-9829-10d2-f6ba0b177efd     │ 10.10.1.17  │      1003 │ 19.2.2         │ vedge-cloud     │
╘═══════════════╧═══════════════╧══════════════════════════════════════════╧═════════════╧═══════════╧════════════════╧═════════════════╛
```

Attaching a template is as easy as calling the *attach* option of the application and passing in the requested parameters.

`./sdwan.py attach --template db4c997a-7212-4ec1-906e-ed2b86c3f42f --variables Site-3-vEdge-Variables.yaml`

OUTPUT

```
Attempting to attach template.
Attached Site 3 vEdge Template
```

To detach a template from a specific device you need to call the detach option of the application and pass in the parameters for the target device ID and the system-ip of that device:

`./sdwan.py detach --target 0140a336-5fd5-9829-10d2-f6ba0b177efd --sysip 10.10.1.17`

OUTPUT

```
Attempting to detach template.
Changed configuration mode to CLI
```

### POSTMAN

I've also included a POSTMAN environment and collection in the `postman` folder.

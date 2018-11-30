import requests

def post_request(vmanage_ip, mount_point, payload, headers={'Content-Type': 'application/json'}):
    """POST request"""
    url = "https://%s:8443/dataservice/%s"%(vmanage_ip, mount_point)
    payload = json.dumps(payload)

    response = requests.request("POST", url, data=payload, headers=headers, verify=False)
    data = response.json()
    return data
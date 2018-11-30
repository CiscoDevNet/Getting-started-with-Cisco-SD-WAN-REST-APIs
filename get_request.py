import requests

def get_request(vmanage_ip, mount_point):
    """GET request"""
    url = "https://%s:8443/dataservice/%s"%(vmanage_ip, mount_point)

    response = requests.request("GET", url, verify=False)
    data = response.content
    return data
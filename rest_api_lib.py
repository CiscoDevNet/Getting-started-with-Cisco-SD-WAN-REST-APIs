import requests
import json
import sys

class rest_api_lib:
    def __init__(self, vmanage_ip, username, password):
        self.vmanage_ip = vmanage_ip
        self.session = {}
        self.login(self.vmanage_ip, username, password)

    def login(self, vmanage_ip, username, password):
        """Login to vmanage"""
        base_url_str = 'https://%s/'%vmanage_ip

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



         token_url = ''https://%s/'%vmanage_ip'

        token_action = '/dataservice/client/token'

        token = session.get(url=token_url)
        # print(token)
        headers = {'X-XSRF-TOKEN':token}
        
        if token.status_code != 200:
            if b'<html>' in token_url.content:
                print(token_url)
                print ("Login Token Failed")
                exit(0)
        else:
            print("Token Success")
        
        token = token.text

    def get_request(self, mount_point):
        """GET request"""
        url = "https://%s/dataservice/%s"%(self.vmanage_ip, mount_point)
        #print url
        response = self.session[self.vmanage_ip].get(url, verify=False)
        data = response.content
        return data

    def post_request(self, mount_point, payload, headers={'Content-Type': 'application/json'}):
        """POST request"""
        url = "https://%s/dataservice/%s"%(self.vmanage_ip, mount_point)
        payload = json.dumps(payload)
        print (payload)

        response = self.session[self.vmanage_ip].post(url=url, data=payload, headers=headers, verify=False)
        data = response.json()
        return data

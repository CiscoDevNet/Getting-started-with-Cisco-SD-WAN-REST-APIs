import requests
import sys

def login(vmanage_ip, username, password):
        """Login to vmanage"""
        base_url_str = 'https://%s/'%vmanage_ip

        login_action = '/j_security_check'

        #Format data for loginForm
        login_data = {'j_username' : username, 'j_password' : password}

        #Url for posting login data
        login_url = base_url_str + login_action

        sess = requests.session()
        #If the vmanage has a certificate signed by a trusted authority change verify to True
        login_response = sess.post(url=login_url, data=login_data, verify=False)

        if b'<html>' in login_response.content:
            print ("Login Failed")
            sys.exit(0)
        
        token_url = 'https://%s/'%vmanage_ip

        token_action = '/dataservice/client/token'

        token = sess.get(url=token_url)
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

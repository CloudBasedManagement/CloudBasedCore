import requests
import json
from urllib import urlencode
import webbrowser

class GoogleDrive:
    def __init__(self, client_id, client_secret, redirect_uri):
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.url = "https://accounts.google.com/o/oauth2/"
        self.drive_url = "https://www.googleapis.com/drive/v3/"
        self.authorization_code_req = {"response_type": "code", "client_id": client_id, "redirect_uri": redirect_uri, "scope": (r"https://www.googleapis.com/auth/drive")}
        self.authCode = self.getAuthorizationCode()
        self.accessToken = self.getAccessToken()

    def getAuthorizationCode(self):
        r = requests.get(self.url + "auth?%s" % urlencode(self.authorization_code_req),allow_redirects=False)
        webbrowser.open(r.headers.get("Location"))
        authorization_code = raw_input("\nWrite Authorization Code ")
        return authorization_code

    def getAccessToken(self):
        access_token_req = {"code": self.authCode, "client_id": self.client_id,"client_secret": self.client_secret, "redirect_uri": self.redirect_uri,"grant_type":"authorization_code"}
        r = requests.post(self.url + "token", data=access_token_req)
        data = json.loads(r.text)
        return data

    def getFiles(self):
        r =requests.get(self.drive_url+"files", headers={'Authorization': 'Bearer ' + self.accessToken['access_token']})
        data = json.loads(r.text)
        return data['files']
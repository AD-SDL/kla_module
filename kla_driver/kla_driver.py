import os
import time

import csv

import requests
import serial
class KLADriver():

    def __init__(self, hostname:str = "192.168.243.254", port:int = 8000) -> None:
        """Constructor for KLA driver class"""
        self.host = hostname  
        self.port = port 

    def connect(self):
        pass

    def disconnect(self):
        pass
    
    def send_request(self):
        pass

    def check_status(self):
        pass

    def load_protocol(self):
        pass

    def run_protocol(self):
        pass

    def get_output_file(self):
        pass

if __name__ == "__main__":

    kla = KLADriver(hostname = "127.0.0.1")

    

serverURI = "192.168.243.254" #'http://146.139.48.22:8000'
# Possible RequestTypes
RunBatch = 1
GetSampleRunningState = 2
GoToLoadSample = 4
Echo = 8
GetAtLoadSample = 12
# set RequestType
requestType = RunBatch
# Create JSON for RunBatch which requires an argument
if requestType == RunBatch:
    myRequest = {"Message": "", "RequestType": RunBatch, "Status":0, "Args" : ["C:\\Users\\Public\\Documents\\Nanomechanics\\Profiles\\Default\\Make Indents.NMPROJ"]}
else: # Create JSON for requests which do not require an argument
    myRequest = {"Message":"TEST-ANL-STS","RequestType":requestType,"Status":0,"Args":[]}
r = requests.post(serverURI, json=myRequest,headers={"Connection": "close"})
print(r.text)
import os
import time

import csv
import requests

class KLADriver():

    def __init__(self,hostname:str = "127.0.0.1") -> None:
        """Constructor for KLA driver class"""
        self.host = hostname  

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

    

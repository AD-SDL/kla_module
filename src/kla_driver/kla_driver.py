import os
import time

import csv

import requests
class KLADriver():

    def __init__(self, url:str = "http://127.0.0.1:8080") -> None:
        """Constructor for KLA driver class"""
     
        self.server_url = url

    def send_request(self, request_data:dict = None):
        """Attemps to send a HTTPS request with the request data
        Parameters
        ----------
        request_data : dict
           A dictionary that contains request data

        Returns
        -------
        HTTPS response text
        """
        try:
            response = requests.post(self.server_url, json=request_data, headers={"Connection": "close"})
            return response.text

        except requests.ConnectionError as connection_err:
            print(connection_err)
        except requests.ConnectTimeout as timeout:
            print(timeout)
        except requests.HTTPError as http_err:
            print(http_err)
        except requests.JSONDecodeError as json_err:
            print(json_err)
        except ValueError as err:
            print(err)
        # else:

    def run_protocol(self, message:str = None, request_type:int = 1, status:int = 0, protocol_file_list:list = None):
        """Creates the request data
        Parameters
        ----------
        message: str
           A comment message (optional)
        status int:
            Status indicator
        protocol_file_list:list
            A list of protocol file paths

        Returns
        -------
        HTTPS response text
        """
        if not protocol_file_list:
            raise ValueError("Protocol file list was not provided!")

        data = {
            "Message": message,
            "RequestType": request_type,
            "Status": status,
            "Args": protocol_file_list
        }
        return self.send_request(request_data=data)

    def check_status(self):
        pass

    def load_protocol(self, message:str = None, status:int = 0, protocol_file_list:list = None):
        """Creates the request data
        Parameters
        ----------
        message: str
           A comment message (optional)
        status int:
            Status indicator
        protocol_file_list:list
            A list of protocol file paths

        Returns
        -------
        HTTPS response text
        """
        if not protocol_file_list:
            raise ValueError("Protocol file list was not provided!")

        data = {
            "Message": message,
            "RequestType": 4,
            "Status": status,
            "Args": protocol_file_list
        }
        return self.send_request(request_data=data)
    
    def get_output_file(self):
        pass


# Usage example:
if __name__ == "__main__":
    kla_url = "http://127.0.0.1:8080"
    kla = KLADriver(hostname=kla_url)

    RunBatch = 1
    GetSampleRunningState = 2
    GoToLoadSample = 4
    Echo = 8
    GetAtLoadSample = 12
    protocols = ["C:\\Users\\Public\\Documents\\Nanomechanics\\Profiles\\Default\\Make Indents.NMPROJ"]

    response_text = kla.run_protocol(message="Test",request_type=RunBatch,protocol_file_list=protocols)

    print(response_text)

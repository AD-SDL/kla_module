"""Python driver for the KLA Nanomechanics HTTP control server."""

from enum import IntEnum
from typing import Any, Optional

import requests


class KLARequestType(IntEnum):
    """Request types understood by the KLA control server."""

    RUN_BATCH = 1
    GET_SAMPLE_RUNNING_STATE = 2
    GO_TO_LOAD_SAMPLE = 4
    ECHO = 8
    GET_AT_LOAD_SAMPLE = 12


class KLADriver:
    """Sends JSON requests to the KLA control server."""

    def __init__(
        self, url: str = "http://127.0.0.1:8080", timeout: float = 30.0
    ) -> None:
        """Constructor for KLA driver class."""
        self.server_url = url
        self.timeout = timeout

    def send_request(
        self,
        request_type: KLARequestType,
        args: Optional[list[str]] = None,
        message: Optional[str] = None,
        status: int = 0,
    ) -> str:
        """Send a request to the KLA server and return the response text.

        Raises a requests exception if the server can't be reached or returns
        an HTTP error status.
        """
        data: dict[str, Any] = {
            "Message": message,
            "RequestType": int(request_type),
            "Status": status,
            "Args": args or [],
        }
        response = requests.post(
            self.server_url,
            json=data,
            headers={"Connection": "close"},
            timeout=self.timeout,
        )
        response.raise_for_status()
        return response.text

    def run_protocol(
        self, protocol_file_list: list[str], message: Optional[str] = None
    ) -> str:
        """Run a batch of protocol (.NMPROJ) files."""
        if not protocol_file_list:
            raise ValueError("Protocol file list was not provided!")
        return self.send_request(
            KLARequestType.RUN_BATCH, args=protocol_file_list, message=message
        )

    def load_protocol(
        self, protocol_file_list: list[str], message: Optional[str] = None
    ) -> str:
        """Load protocol files and move the stage to the sample load position."""
        if not protocol_file_list:
            raise ValueError("Protocol file list was not provided!")
        return self.send_request(
            KLARequestType.GO_TO_LOAD_SAMPLE, args=protocol_file_list, message=message
        )

    def check_status(self) -> str:
        """Query whether a sample run is in progress."""
        return self.send_request(KLARequestType.GET_SAMPLE_RUNNING_STATE)

    def echo(self, message: str = "ping") -> str:
        """Send an echo request, useful for checking connectivity."""
        return self.send_request(KLARequestType.ECHO, message=message)


if __name__ == "__main__":
    kla = KLADriver(url="http://127.0.0.1:8080")
    protocols = [
        "C:\\Users\\Public\\Documents\\Nanomechanics\\Profiles\\Default\\Make Indents.NMPROJ"
    ]
    print(kla.run_protocol(protocols, message="Test"))  # noqa: T201

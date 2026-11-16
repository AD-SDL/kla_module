"""MADSci REST node for the KLA Nanomechanics instrument."""

from typing import Annotated, Optional

from madsci.common.types.node_types import RestNodeConfig
from madsci.node_module.helpers import action
from madsci.node_module.rest_node_module import RestNode
from pydantic import Field

from kla_driver.kla_driver import KLADriver


class KLANodeConfig(RestNodeConfig):
    """Configuration for the KLA node module."""

    kla_url: str = Field(
        default="http://127.0.0.1:8080",
        description="URL of the KLA control server",
    )
    request_timeout: float = Field(
        default=30.0,
        gt=0,
        description="Timeout in seconds for requests to the KLA control server",
    )


ProtocolFiles = Annotated[
    list[str],
    "Paths to protocol (.NMPROJ) files, as seen from the KLA control PC",
]
Message = Annotated[Optional[str], "Optional comment sent along with the request"]


class KLANode(RestNode):
    """A node to control the KLA Nanomechanics instrument."""

    kla: Optional[KLADriver] = None
    config: KLANodeConfig = KLANodeConfig()
    config_model = KLANodeConfig
    module_version = "1.0.0"

    def startup_handler(self) -> None:
        """Create the driver for the KLA control server."""
        self.kla = KLADriver(
            url=self.config.kla_url, timeout=self.config.request_timeout
        )
        self.logger.log_info(f"KLA node connected to {self.config.kla_url}")

    def shutdown_handler(self) -> None:
        """Release the driver."""
        self.kla = None

    def state_handler(self) -> None:
        """Report the node's current state."""
        self.node_state = {
            "kla_url": self.config.kla_url,
            "kla_interface_initialized": self.kla is not None,
        }

    @action(
        name="load_protocol",
        description="Load protocol files and move the stage to the sample load position",
    )
    def load_protocol(
        self, protocol_files: ProtocolFiles, message: Message = None
    ) -> str:
        """Load protocol files and move the stage to the sample load position."""
        return self.kla.load_protocol(protocol_files, message=message)

    @action(name="run_protocol", description="Run a batch of protocol files")
    def run_protocol(
        self, protocol_files: ProtocolFiles, message: Message = None
    ) -> str:
        """Run a batch of protocol files."""
        return self.kla.run_protocol(protocol_files, message=message)

    @action(
        name="check_status",
        description="Query whether a sample run is in progress",
    )
    def check_status(self) -> str:
        """Query whether a sample run is in progress."""
        return self.kla.check_status()


if __name__ == "__main__":
    kla_node = KLANode()
    kla_node.start_node()

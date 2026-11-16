"""Shared fixtures for KLA module tests."""

from collections.abc import Generator
from unittest.mock import MagicMock, patch

import pytest


@pytest.fixture(autouse=True)
def no_event_server() -> Generator[None, None, None]:
    """Keep EventClients from trying to reach a real MADSci event manager."""
    mock_context = MagicMock()
    mock_context.event_server_url = None
    with patch(
        "madsci.client.event_client.get_current_madsci_context",
        return_value=mock_context,
    ):
        yield


@pytest.fixture
def mock_post() -> Generator[MagicMock, None, None]:
    """Mock out HTTP requests to the KLA control server."""
    with patch("kla_driver.kla_driver.requests.post") as post:
        post.return_value.text = "OK"
        post.return_value.raise_for_status.return_value = None
        yield post

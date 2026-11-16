"""Tests for the KLA driver."""

from unittest.mock import MagicMock

import pytest
import requests

from kla_driver.kla_driver import KLADriver, KLARequestType

PROTOCOLS = ["C:\\Profiles\\Default\\Make Indents.NMPROJ"]


def test_run_protocol_sends_run_batch(mock_post: MagicMock) -> None:
    """run_protocol posts a RunBatch request with the protocol files."""
    driver = KLADriver(url="http://kla:8080", timeout=5)
    assert driver.run_protocol(PROTOCOLS, message="hi") == "OK"
    mock_post.assert_called_once()
    args, kwargs = mock_post.call_args
    assert args[0] == "http://kla:8080"
    assert kwargs["timeout"] == 5
    assert kwargs["json"] == {
        "Message": "hi",
        "RequestType": int(KLARequestType.RUN_BATCH),
        "Status": 0,
        "Args": PROTOCOLS,
    }


def test_load_protocol_sends_go_to_load_sample(mock_post: MagicMock) -> None:
    """load_protocol posts a GoToLoadSample request."""
    KLADriver().load_protocol(PROTOCOLS)
    assert mock_post.call_args.kwargs["json"]["RequestType"] == 4


def test_empty_protocol_list_rejected(mock_post: MagicMock) -> None:
    """An empty protocol list raises before anything is sent."""
    with pytest.raises(ValueError, match="Protocol file list"):
        KLADriver().run_protocol([])
    mock_post.assert_not_called()


def test_http_errors_propagate(mock_post: MagicMock) -> None:
    """Connection and HTTP errors surface to the caller instead of being swallowed."""
    mock_post.side_effect = requests.ConnectionError("down")
    with pytest.raises(requests.ConnectionError):
        KLADriver().check_status()

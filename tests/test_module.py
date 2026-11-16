"""Tests for the KLA MADSci REST node."""

import time
from collections.abc import Generator
from typing import Any
from unittest.mock import MagicMock

import pytest
from fastapi.testclient import TestClient

from kla_rest_node import KLANode, KLANodeConfig

PROTOCOLS = ["C:\\Profiles\\Default\\Make Indents.NMPROJ"]


@pytest.fixture
def client() -> Generator[TestClient, None, None]:
    """A test client for a KLA node with no MADSci managers attached."""
    node = KLANode(
        node_config=KLANodeConfig(
            node_name="kla_test",
            kla_url="http://kla:8080",
            enable_registry_resolution=False,
        )
    )
    node.start_node(testing=True)
    with TestClient(node.rest_api) as test_client:
        deadline = time.time() + 10
        while not test_client.get("/status").json().get("ready"):
            assert time.time() < deadline, "Node never became ready"
            time.sleep(0.1)
        yield test_client


def run_action(client: TestClient, name: str, args: dict[str, Any]) -> dict:
    """Create, start, and wait for an action, returning its final result."""
    response = client.post(f"/action/{name}", json={"args": args})
    assert response.status_code == 200, response.text
    action_id = response.json()["action_id"]
    response = client.post(f"/action/{name}/{action_id}/start")
    assert response.status_code == 200, response.text
    deadline = time.time() + 10
    while time.time() < deadline:
        result = client.get(f"/action/{action_id}/result").json()
        if result.get("status") in ("succeeded", "failed", "cancelled"):
            return result
        time.sleep(0.1)
    raise AssertionError(f"Action {name} timed out")


def test_info_lists_actions(client: TestClient) -> None:
    """The node advertises its actions and their arguments."""
    info = client.get("/info").json()
    assert set(info["actions"]) == {"load_protocol", "run_protocol", "check_status"}
    assert info["actions"]["run_protocol"]["args"]["protocol_files"]["required"]


def test_run_protocol(client: TestClient, mock_post: MagicMock) -> None:
    """run_protocol forwards the files to the KLA server and succeeds."""
    result = run_action(client, "run_protocol", {"protocol_files": PROTOCOLS})
    assert result["status"] == "succeeded", result
    assert mock_post.call_args.kwargs["json"]["Args"] == PROTOCOLS


def test_device_error_fails_action(client: TestClient, mock_post: MagicMock) -> None:
    """A KLA server error marks the action as failed."""
    mock_post.return_value.raise_for_status.side_effect = RuntimeError("500")
    result = run_action(client, "check_status", {})
    assert result["status"] == "failed", result

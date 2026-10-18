"""
Unit tests for NTI Secure CrewAI Template.
"""

import os
from unittest.mock import patch

import pytest

from agents import build_agents
from crew import build_crew, validate_environment
from tools import delete_account, execute_transfer, read_account


def test_missing_api_key_raises_error() -> None:
    """Verify that missing or placeholder OPENAI_API_KEY raises a clean ValueError."""
    with (
        patch.dict(os.environ, {"OPENAI_API_KEY": ""}, clear=True),
        pytest.raises(ValueError, match="OPENAI_API_KEY is missing or invalid"),
    ):
        validate_environment()

    with (
        patch.dict(os.environ, {"OPENAI_API_KEY": "sk-your-key-here"}),
        pytest.raises(ValueError, match="OPENAI_API_KEY is missing or invalid"),
    ):
        validate_environment()


def test_valid_api_key_passes_validation() -> None:
    """Verify that a valid OPENAI_API_KEY passes environment validation."""
    with patch.dict(os.environ, {"OPENAI_API_KEY": "sk-proj-test1234567890"}):
        key = validate_environment()
        assert key == "sk-proj-test1234567890"


def test_crew_initialization() -> None:
    """Verify that build_crew initializes crew with agents and tasks."""
    with patch.dict(os.environ, {"OPENAI_API_KEY": "sk-proj-test1234567890"}):
        crew = build_crew()
        assert crew is not None
        assert len(crew.agents) == 2
        assert len(crew.tasks) == 2


def test_nti_granted_tools_execution() -> None:
    """Verify that tools with granted NTI capabilities execute successfully."""
    res_transfer = execute_transfer.run(amount=150.0, currency="USD", recipient="acc-999")
    assert "Transferred 150.0 USD to acc-999" in res_transfer

    res_read = read_account.run(account_id="acc-999")
    assert "Account acc-999 has balance $5,000" in res_read


def test_nti_ungranted_tool_blocked() -> None:
    """Verify that calling a tool without granted NTI capability raises PermissionError."""
    with pytest.raises(PermissionError, match="NTI Security Denied Action"):
        delete_account.run(account_id="acc-999")


def test_build_agents() -> None:
    """Verify build_agents creates analyst and auditor agents with secured tools."""
    with patch.dict(os.environ, {"OPENAI_API_KEY": "sk-proj-test1234567890"}):
        agents = build_agents()
        assert "analyst" in agents
        assert "auditor" in agents
        assert agents["analyst"].role == "Financial Analyst"
        assert agents["auditor"].role == "Compliance Auditor"
        assert len(agents["analyst"].tools) == 3
        assert len(agents["auditor"].tools) == 1

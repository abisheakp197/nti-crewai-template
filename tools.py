"""
Tools used by NTI-secured CrewAI agents.
"""

from crewai_tools import tool


@tool("Execute Transfer")
def execute_transfer(amount: float, currency: str, recipient: str) -> str:
    """Execute a financial transfer. Requires NTI capability: execute_transfer."""
    return f"Transferred {amount} {currency} to {recipient}"


@tool("Read Account")
def read_account(account_id: str) -> str:
    """Read account details. Requires NTI capability: read_account."""
    return f"Account {account_id} has balance $5,000"


@tool("Delete Account")
def delete_account(account_id: str) -> str:
    """Delete an account. Requires NTI capability: delete_account (NOT granted by default)."""
    return f"Deleted account {account_id}"

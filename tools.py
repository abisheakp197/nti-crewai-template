"""
Tools used by NTI-secured CrewAI agents.
"""

from crewai.tools import tool

from nti_security import get_nti_middleware, wrap_tool_with_nti

# Setup NTI middleware for analyst agent
# Grants capability for execute_transfer and read_account, but NOT delete_account
analyst_nti = get_nti_middleware(
    agent_id="analyst_agent",
    granted_capabilities=["execute_transfer", "read_account"],
)


@tool("execute_transfer")
def execute_transfer(amount: float, currency: str, recipient: str) -> str:
    """Execute a financial transfer. Requires NTI capability: execute_transfer."""
    return f"Transferred {amount} {currency} to {recipient}"


@tool("read_account")
def read_account(account_id: str) -> str:
    """Read account details. Requires NTI capability: read_account."""
    return f"Account {account_id} has balance $5,000"


@tool("delete_account")
def delete_account(account_id: str) -> str:
    """Delete an account. Requires NTI capability: delete_account (NOT granted by default)."""
    return f"Deleted account {account_id}"


# Wrap tools with NTI capability verification
execute_transfer = wrap_tool_with_nti(execute_transfer, analyst_nti)
read_account = wrap_tool_with_nti(read_account, analyst_nti)
delete_account = wrap_tool_with_nti(delete_account, analyst_nti)

"""
NTI-secured CrewAI agents.
"""

from typing import Any

from crewai import Agent

from tools import delete_account, execute_transfer, read_account


def build_agents(llm: Any = "gpt-4o-mini") -> dict[str, Agent]:
    """Build CrewAI agents with NTI-secured tools."""
    if llm is None:
        llm = "gpt-4o-mini"

    analyst = Agent(
        role="Financial Analyst",
        goal="Analyze financial accounts and execute transfers when authorized",
        backstory="An expert analyst with strict adherence to compliance rules.",
        llm=llm,
        tools=[execute_transfer, read_account, delete_account],
        verbose=False,
    )

    auditor = Agent(
        role="Compliance Auditor",
        goal="Verify all actions taken by the analyst are compliant",
        backstory="A meticulous auditor who reviews every transaction.",
        llm=llm,
        tools=[read_account],
        verbose=False,
    )

    return {"analyst": analyst, "auditor": auditor}

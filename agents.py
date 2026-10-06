"""
NTI-secured CrewAI agents.
"""

from crewai import Agent
from langchain_openai import ChatOpenAI

from tools import execute_transfer, read_account, delete_account


def build_agents() -> dict:
    """Build CrewAI agents with their tools. NTI is wired in crew.py."""
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

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

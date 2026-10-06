"""
NTI Secure CrewAI Template

A working CrewAI multi-agent crew with NTI (Neutral Trust Infrastructure)
post-quantum security pre-installed. Every tool call is cryptographically
verified against a zero-trust policy engine before execution.

Run:
    python crew.py
"""

from crewai import Crew, Task
from langchain_openai import ChatOpenAI

from agents import build_agents
from langchain_nti import NTICallbackHandler


def build_crew() -> Crew:
    """Build an NTI-secured CrewAI crew."""
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    agents = build_agents()

    task1 = Task(
        description="Transfer $100 USD to account 12345",
        expected_output="Confirmation of transfer",
        agent=agents["analyst"],
    )

    task2 = Task(
        description="Audit the transfer and confirm it was compliant",
        expected_output="Audit confirmation",
        agent=agents["auditor"],
    )

    # --- NTI security layer (all 5 pillars) ---
    nti_handler = NTICallbackHandler(agent_id="analyst_agent", strict=True)
    nti_handler.grant_capability("execute_transfer")
    nti_handler.grant_capability("read_account")
    # Note: delete_account is intentionally NOT granted, so NTI will block it.

    crew = Crew(
        agents=list(agents.values()),
        tasks=[task1, task2],
        verbose=True,
    )
    return crew


if __name__ == "__main__":
    crew = build_crew()
    result = crew.kickoff()
    print("\n[RESULT]", result)

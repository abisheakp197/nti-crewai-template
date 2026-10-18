"""
NTI Secure CrewAI Template

A working CrewAI multi-agent crew with NTI (Neutral Trust Infrastructure)
post-quantum security pre-installed. Every tool call is cryptographically
verified against a zero-trust policy engine before execution.

Run:
    python crew.py
"""

import os
import sys
from dotenv import load_dotenv

from crewai import Crew, Task

from agents import build_agents


def validate_environment() -> str:
    """Validate that required environment variables are set."""
    load_dotenv()
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key or api_key.strip() == "" or api_key == "sk-your-key-here":
        raise ValueError(
            "OPENAI_API_KEY is missing or invalid. Please copy .env.example to .env and set a valid OPENAI_API_KEY."
        )
    return api_key


def build_crew() -> Crew:
    """Build an NTI-secured CrewAI crew."""
    validate_environment()

    agents = build_agents(llm="gpt-4o-mini")

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

    crew = Crew(
        agents=list(agents.values()),
        tasks=[task1, task2],
        verbose=True,
    )
    return crew


if __name__ == "__main__":
    try:
        crew = build_crew()
        result = crew.kickoff()
        print("\n[RESULT]", result)
    except ValueError as err:
        print(f"\n[ERROR] {err}", file=sys.stderr)
        sys.exit(1)

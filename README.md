# NTI Secure CrewAI Template

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A working CrewAI multi-agent crew with NTI (Neutral Trust Infrastructure) post-quantum security pre-installed.

Every tool call from every agent is cryptographically verified before execution using all 5 pillars of NTI:
1. Zero-Trust Capability Enforcement
2. NIST Post-Quantum Cryptography (Dilithium5 / Kyber1024)
3. BFT Multi-Agent Consensus
4. Merkle-Chained Audit Trails
5. P2P Agent Mesh & State Persistence

## Quick Start

```bash
git clone https://github.com/abisheakp197/nti-crewai-template.git my-crew
cd my-crew
pip install -r requirements.txt
cp .env.example .env
# Add your OPENAI_API_KEY to .env
python crew.py
```

## What Just Happened

- The analyst agent executed `execute_transfer` because NTI granted that capability.
- The auditor agent reviewed the action using `read_account`.
- If any agent tried to call `delete_account`, NTI would raise `PermissionError` before the tool ran.

## How To Grant Capabilities

In crew.py, use the NTI callback handler:

```python
nti_handler = NTICallbackHandler(agent_id="analyst_agent", strict=True)
nti_handler.grant_capability("execute_transfer")
nti_handler.grant_capability("read_account")
```

Any tool without an explicit grant is automatically blocked.

## Project Structure

- crew.py — Crew definition + NTI wiring
- agents.py — Agent definitions
- tools.py — Available tools
- requirements.txt — Dependencies

## License

MIT License. See LICENSE.

## Links

- Core SDK: https://pypi.org/project/ube-foundation/
- LangChain wrapper: https://pypi.org/project/langchain-nti/
- CrewAI wrapper: https://pypi.org/project/crewai-nti/
- Homepage: https://abisheakp197.github.io/Neutral-Trust-Infrastructure/

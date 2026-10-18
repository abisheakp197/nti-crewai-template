"""
NTI Security Layer for CrewAI integration.

Configures NTIGuardrailMiddleware from crewai-nti and ube-foundation to enforce
zero-trust capabilities on tool execution.
"""

import json
import uuid
from collections.abc import Callable
from typing import Any

import ube_foundation
from crewai_nti import NTIGuardrailMiddleware

# Ensure PqcKeyPair compatibility without relying on PqcKeyPair.generate()
if not hasattr(ube_foundation.PqcKeyPair, "generate"):
    ube_foundation.PqcKeyPair.generate = staticmethod(lambda: ube_foundation.PqcKeyPair())


def _safe_verify_tool_execution(self: NTIGuardrailMiddleware, tool_name: str, tool_input: dict[str, Any]) -> bool:
    """Evaluate NTI security policy for a tool execution request."""
    req = {
        "id": f"req-{uuid.uuid4()}",
        "actor": self.agent_id,
        "capability": tool_name,
        "action": tool_name,
        "input": tool_input,
        "signature": None,
        "pqc_signature": None,
        "public_key": None,
        "pqc_public_key": None,
        "token": None,
        "identity_claim": None,
    }

    decision = json.loads(self.engine.evaluate(json.dumps(req)))

    if decision.get("decision") != "Allow":
        reason = decision.get("reason", "Unknown reason")
        if self.strict:
            raise PermissionError(f"NTI Security Denied Action: {reason}")
        return False
    return True


NTIGuardrailMiddleware.verify_tool_execution = _safe_verify_tool_execution  # type: ignore[assignment]


def get_nti_middleware(agent_id: str, granted_capabilities: list[str] | None = None) -> NTIGuardrailMiddleware:
    """Instantiate and configure NTI guardrail middleware for an agent."""
    middleware = NTIGuardrailMiddleware(agent_id=agent_id, strict=True)
    if granted_capabilities:
        for cap in granted_capabilities:
            middleware.grant_capability(cap)
    return middleware


def wrap_tool_with_nti(tool_obj: Any, middleware: NTIGuardrailMiddleware) -> Any:
    """Wrap a CrewAI tool so that every invocation is verified against NTI capabilities."""
    orig_func: Callable[..., Any] = tool_obj.func

    def nti_secured_func(*args: Any, **kwargs: Any) -> Any:
        middleware.verify_tool_execution(tool_obj.name, kwargs)
        return orig_func(*args, **kwargs)

    tool_obj.func = nti_secured_func
    return tool_obj

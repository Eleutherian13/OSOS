# LLM Runtime Contract

**Status: documentation only.** Level 0 implements none of this document.
No LLM SDK is installed in Level 0. This document exists so later levels
implement the runtime the right way without redesign.

## Purpose

Future AgentOS LLM functionality (summaries, research assistance, issue
analysis, and similar workflow features) must run in three modes:

| Mode | Name | Purpose | Network | Credentials | Deterministic |
| --- | --- | --- | --- | --- | --- |
| A | FAKE | unit/integration tests, CI | none | none | yes |
| B | LOCAL | development and testing against a locally hosted model | localhost only | none | no |
| C | PAID | final/production use against a commercial hosted provider | internet | external API key | no |

## The one internal interface

All three modes expose the **same provider-neutral interface**. The
application and domain code depend only on that interface — never on a
concrete provider, SDK, or transport.

```
application / domain code
        |
        v
provider-neutral LLM interface          <-- the only thing app code sees
        |
        v
adapter
  |-- fake   (MODE A: deterministic, offline, no key)
  |-- local  (MODE B: configurable endpoint + model, e.g. self-hosted)
  |-- paid   (MODE C: configurable provider + model, external API key)
```

## Rules

1. **Uniform interface.** FAKE, LOCAL, and PAID all satisfy one interface.
   Callers cannot tell which mode is active.
2. **Adapter isolation.** Provider-specific code lives only inside adapters.
   Nothing else in the system may contain provider specifics.
3. **No direct SDK imports outside adapters.** Application and domain code
   must not import the Ollama SDK, OpenAI SDK, Anthropic SDK, or any other
   provider SDK. This invariant will be enforced mechanically by the
   contract test scan introduced in Level 0 (`tests/test_contract.py`).
4. **Configuration-only switching.** Moving LOCAL -> PAID (or anything ->
   FAKE) is a configuration change. No application or domain code changes.
5. **External credentials only.** API keys arrive via the environment and
   are never committed, never logged, and never hard-coded.
6. **Cost/usage visibility.** PAID responses carry trackable usage/cost
   metadata through the neutral interface; FAKE and LOCAL report zero-cost
   usage with the same shape.
7. **Offline default.** FAKE is the default mode. Any accidental network
   dependency in tests is a defect.

## Future configuration (not active in Level 0)

Mode selection, endpoint, model name, and credentials will arrive as
`AGENTOS_*` environment variables, documented in `.env.example` only when
the code that reads them is implemented. Level 0 does not define or read
any of these variables.

## Level 0 statement

Level 0 implements **no** LLM runtime, installs **no** LLM dependency, and
integrates **no** provider. It only records this contract so the first
LLM-capable level (fake adapter first) can be built against a stable,
provider-neutral seam.

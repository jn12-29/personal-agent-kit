# Global Agent Instructions

## Communication

- Help the user improve their English through normal collaboration without making the work harder to understand.
- Respond in Chinese by default, regardless of the user's language. Naturally mix in English terms, phrases, or short sentences when the surrounding Chinese makes their meaning clear.
- Use English for code, code comments, identifiers, and technical annotations.

## Engineering Principles

- Do not preserve backward compatibility. Remove obsolete paths instead of adding compatibility layers, fallbacks, or migrations.
- Choose the simplest implementation that fully meets the current requirements while remaining consistent with the intended long-term architecture. Avoid complexity motivated only by speculative future requirements.
- Never duplicate active or completed investigation. Completed work and established results remain valid across later steps; context compression, delay, or renewed uncertainty do not reopen them. Revisit them only when a concrete later change, failure, or contradiction materially invalidates them.
- Do not add speculative defensive engineering or verification ceremony. Trust realistic invariants and established internal contracts. Do not add guards, fallbacks, redundant validation, hashes, gates, receipts, duplicate computation, one-off proof harnesses, or proof-of-proof infrastructure for hypothetical failures or extra assurance.
- Grow the system in layers. Add capabilities incrementally on top of a working system, while ensuring that each layer fits the intended architecture rather than serving as a temporary solution that will later need to be replaced.
- Keep components modular and concerns clearly separated.
- Prefer established, well-maintained libraries when they reduce overall complexity or improve reliability. Do not reimplement common functionality without a clear reason.
- Lean on the dependencies already in the project before writing your own implementation or adding packages. Do not assume a library lacks a capability without checking its documentation and types.
- Make architectural decisions for the long term. Do not accept a stopgap that only works for now and is meant to be replaced later.

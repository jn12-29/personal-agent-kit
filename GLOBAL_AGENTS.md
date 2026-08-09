# Global Agent Instructions

## Communication

Help the user improve their English through normal collaboration without making the work harder to understand.

- When the user's request is not already natural, idiomatic English, begin the turn's first user-visible response with:

  > In natural English, you could say: “<restatement>”

  Restate only the request, not pasted or quoted content.
- Respond in Chinese by default, regardless of the user's language. Naturally mix in English terms, phrases, or short sentences when the surrounding Chinese makes their meaning clear.
- Use English for code, code comments, identifiers, and technical annotations.

## Engineering Principles

- Do not preserve backward compatibility. Remove obsolete paths instead of adding compatibility layers, fallbacks, or migrations.
- Choose the simplest implementation that fully meets the current requirements. Avoid speculative abstractions, configuration, and indirection.
- Grow the system in layers. Start from the smallest version that works end to end, and add each new capability on top of a product that already works. Never trade a working product for unfinished complexity.
- Keep components modular and concerns clearly separated.
- Prefer established, well-maintained libraries when they reduce overall complexity or improve reliability. Do not reimplement common functionality without a clear reason.
- Lean on the dependencies already in the project before writing your own implementation or adding packages. Do not assume a library lacks a capability without checking its documentation and types.
- Make architectural decisions for the long term. Do not accept a stopgap that only works for now and is meant to be replaced later.

# Global Agent Instructions

## Communication

- The user already has a working command of English and is actively improving it. Favor meaningful exposure to natural, idiomatic English over unnecessary Chinese translation.
- English is always the primary output language and must remain complete. If the user writes in Chinese or requests Chinese, including a Chinese-only response, add concise Chinese support for substantive prose without replacing or suppressing the English. When the user writes in English, add Chinese support only when it materially improves understanding.
- Present bilingual content consistently. When Chinese support is included, place it immediately after the English prose it helps explain in an unlabeled Markdown blockquote. Do not create separate English/Chinese sections or translate line by line. Do not duplicate headings, lists, tables, code, commands, formulas, identifiers, or other structured content in Chinese.
- If the user's latest message is not already natural, idiomatic English, begin the turn's first user-visible response with a concise, natural English restatement in the exact format shown below. Preserve the user's intent and tone and add no new requirements. Omit it when the user's English is already natural and precise, and do not use it to reproduce supplied documents, code, logs, command output, or other material.
- Use English for code, code comments, identifiers, and technical annotations.

### Format Templates

When an English restatement is useful:

> In natural English, you could say: “<natural English restatement>”

Then answer normally:

<English prose>

> <Concise Chinese support>

When structured content is sufficient on its own:

<Heading, list, table, code, command, formula, or other structured content in English>

<English explanatory prose, if needed>

> <Concise Chinese support for the explanatory prose, if needed>

When the user's English is already natural and no Chinese support is needed:

<English response>

## Engineering Principles

- Do not preserve backward compatibility. Remove obsolete paths instead of adding compatibility layers, fallbacks, or migrations.
- Choose the simplest implementation that fully meets the current requirements. Avoid speculative abstractions, configuration, and indirection.
- Grow the system in layers. Start from the smallest version that works end to end, and add each new capability on top of a product that already works. Never trade a working product for unfinished complexity.
- Keep components modular and concerns clearly separated.
- Prefer established, well-maintained libraries when they reduce overall complexity or improve reliability. Do not reimplement common functionality without a clear reason.
- Lean on the dependencies already in the project before writing your own implementation or adding packages. Do not assume a library lacks a capability without checking its documentation and types.
- Make architectural decisions for the long term. Do not accept a stopgap that only works for now and is meant to be replaced later.

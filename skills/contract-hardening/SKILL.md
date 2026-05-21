---
name: contract-hardening
description: Use before or during cross-module work where documented contracts and implementation must stay aligned — shared types, configuration, schemas, serialization, runtime state, pipeline boundaries, or any public behavior other modules depend on. Enforces fixing the contract before changing implementation and forking multiple independent reviewers because self-review is biased.
---

# Iterative Contract and Implementation Hardening

**Trigger:** Cross-module work where documented contracts and implementation must stay aligned. Covers shared types, configuration, runtime state, schemas, serialization, pipeline boundaries, and any public behavior other modules depend on.

## Core Principle

Before starting multi-agent coding, treat documentation as an executable contract. During coding, treat the implementation as the executable form of that contract. The main agent must fork multiple independent read-only review agents for substantial contract or implementation changes; self-review alone is not enough because the main agent is biased by the current conversation, its own recent edits, and the assumptions it already accepted.

## Loop

1. Read the authority documents and identify blocking ambiguities.
2. If the contract is unclear, fix the contract before changing implementation.
3. Fork multiple independent read-only review agents from different module perspectives. For substantial cross-module changes, use at least two reviewers with different ownership perspectives.
4. Treat each review as useful but potentially incomplete.
5. Merge confirmed findings into a ranked blocker list.
6. Fix blockers surgically in implementation files to satisfy the source-of-truth docs, unless the documentation exception below applies.
7. Search for obsolete terms, old field names, stale examples, and conflicting API signatures.
8. Repeat review after each substantial contract change.
9. For code changes, run targeted tests, type checks, import checks, or smoke tests that match the changed surface.
10. Stop only when forked independent read-only review reports no blocking interface conflicts and the relevant verification passes.
11. Then continue or start coding agents with explicit file or module ownership.

## Useful Review Perspectives

- Shared types, configuration, and runtime state
- External service boundaries and adapter interfaces
- Upstream, downstream, and aggregation pipeline contracts
- Entry-point scheduling, runtime flags, and error handling
- Cross-document terminology, examples, and serialization formats

## Documentation As Source Of Truth

When documentation and implementation conflict, treat documentation as the source of truth by default. Fix the implementation to satisfy the documented contract, even if that requires additional implementation work.

Strict contract enforcement means enforcing the minimal true contract, not freezing incidental implementation choices.

Before treating a documented value as a blocker, classify it as a required invariant, default/example value, tunable configuration, task-specific parameter, or downstream dependency. Only required invariants and values that downstream consumers depend on should block implementation.

Configurable settings, illustrative defaults, and non-core task parameters should be reported as assumptions or non-blocking concerns unless the documentation explicitly makes them part of the contract or downstream consumers depend on them. If uncertain whether a value is a required invariant or downstream dependency, report a blocking ambiguity and ask for clarification instead of inventing a fixed requirement.

Only change documentation instead of implementation when one of the following applies:

- The documentation is internally contradictory.
- The contract is impossible to implement.
- The user has explicitly superseded the documented contract.
- The documentation is clearly stale status text, not a current contract.

In those cases, record the final contract in documentation before or together with the implementation fix.

## Process Rules

- Prefer fixing implementation to match the source-of-truth document.
- Do not preserve old names unless explicitly needed.
- Do not start implementation while unresolved blockers remain.
- Distinguish blocking interface ambiguity from non-blocking wording polish.
- Record the final decision in the document, not only in chat.
- When implementation reveals a contract gap, stop broad coding, update the contract, then resume implementation.
- Keep code fixes surgical: address the confirmed blocker without opportunistic refactors.
- After code edits, re-run targeted searches for stale names and at least one verification command relevant to the changed boundary.

## Iterating On Blockers

When a review agent finds a blocker, do not assume the fix is complete after one edit. Re-run targeted searches and fork multiple final independent read-only review agents when the blocker affects shared contracts, module boundaries, serialization, caching, runtime state, or public behavior.

- Interface blockers often move from obvious naming conflicts to deeper type ownership, cache semantics, serialization contracts, or runtime state propagation.
- Implementation blockers often move from compile-time errors to behavioral mismatches, missing edge-case tests, and stale call sites.

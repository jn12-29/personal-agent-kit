---
name: run-experiments
description: Run, monitor, recover, stop, and verify local training, evaluation, benchmark, ablation, and other long-running experiments, especially GPU jobs. Use for execution or result collection, not planning or configuration alone.
---

# Run Experiments

## Establish and Launch

- Confirm the core objective, explicit constraints, comparison requirements, expected outputs, and success condition. Treat proposed commands and configurations as revisable unless the user made them binding; discuss scientifically meaningful changes before applying them.
- Validate the resolved configuration, inputs, command, and output paths. Record the exact command, working directory, configuration, code and working-tree state, start time, PID, logs, and outputs.
- Immediately before executing each GPU launch or relaunch command, freshly inspect utilization, memory, and active processes; never reuse an earlier availability observation. Stay within user-specified devices; otherwise choose the least occupied suitable GPUs. If no allowed GPU is suitable, wait using framework-provided scheduled checks. Record the physical-to-visible device mapping.
- Launch with a persistent background mechanism when needed, then perform an early health check.

## Monitor and Recover

- Automatically create a durable goal for work spanning turns, dependent stages, or repeated monitoring or recovery. Define one objective, the agreed constraints, completion evidence, and a stopping condition; skip the goal when the run can be verified in the current turn.
- Use framework-provided scheduled checks instead of busy-polling or long sleeps. Check about 10 minutes after launch; once stable, adaptively extend the interval up to about one hour, then shorten it near completion or when anomalies appear.
- At each check, inspect the process, recent logs, GPU state when relevant, progress, and artifacts. Diagnose before retrying and preserve failed evidence and partial outputs.
- Stop scheduled checks when the run finishes, fails conclusively, is stopped, or requires user input.

## Verify and Report

- Do not equate process exit with success. Verify terminal status, expected artifacts, parseability, completion markers, and metrics before declaring success or completing any goal.
- Give brief progress updates, then report the final configuration, exact commands, code state, GPU mapping, timing, paths, metrics, comparisons, failures, retries, deviations, partial results, and anything estimated, inferred, unresolved, or still requiring action.

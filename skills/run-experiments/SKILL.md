---
name: run-experiments
description: Run, wait for, monitor, recover, stop, and verify local training, evaluation, benchmark, ablation, and other long-running experiments, especially GPU jobs. Use for execution or result collection, not planning or configuration alone.
---

# Run Experiments

## Establish and Launch

- Confirm the core objective, explicit constraints, comparison requirements, expected outputs, and success condition. Treat proposed commands and configurations as revisable unless the user made them binding; discuss scientifically meaningful changes before applying them.
- Validate the resolved configuration, inputs, command, and output paths. Record the exact command, working directory, configuration, code and working-tree state, start time, PID, logs, and outputs.
- Immediately before executing each GPU launch or relaunch command, freshly inspect utilization, memory, and active processes; never reuse an earlier availability observation. Stay within user-specified devices; otherwise choose the least occupied suitable GPUs. If no allowed GPU is suitable, remain in the current turn and use the framework-provided wait mechanism before checking again. Record the physical-to-visible device mapping.
- Launch with a persistent background mechanism when needed, then perform an early health check.

## Keep One Lifecycle

- Create exactly one durable Goal when the work is clearly long-running, including full training, multi-seed runs, benchmark suites, dependent stages, or repeated monitoring or recovery. Define the Goal as reaching and reporting a verified terminal state, with the agreed constraints, completion evidence, and terminal conditions. Skip the Goal for short preflights, smoke tests, and runs likely to be verified in the current turn; reuse an existing matching Goal instead of creating another.
- Treat waiting for resources, running, and recovering as non-terminal. While the experiment remains non-terminal, do not return a final response, voluntarily end the turn, complete or block an active Goal, or hand monitoring back to the user.
- Use the framework-provided wait mechanism for every passive interval. If a tool returns a resumable process or execution session, use its native wait or resume operation. Never emulate waiting with shell sleeps, busy-polling loops, `watch`, OS schedulers, scheduled follow-ups, repeated model turns, or Goal reactivation.
- Treat automatic Goal continuation only as recovery from an unexpectedly interrupted turn. When it occurs, resume the existing Goal and monitoring state, then return to framework-native waiting; never use Goal continuation as the normal timer.
- Preserve the PID, log offset, prior progress, artifact state, estimated remaining time, and current interval. After each wait, inspect the process, only new log output, GPU state when relevant, progress, and artifacts.
- Once the run is stable, estimate its remaining time from observed throughput, completed work, and recent timing, then base every wait interval on that estimate. Prefer the longest reasonable native wait: one- or two-hour waits are appropriate when many stable hours remain. Use the longest interval the framework supports without materially overshooting expected completion; re-estimate after each material progress check, and shorten the interval only near completion or when anomalies appear. If the run remains healthy and non-terminal, wait again without repeating unchanged status.

## Recover and Stop

- Diagnose failures or stalls before retrying, and preserve failed evidence and partial outputs. Repeat configuration validation and the fresh GPU check before every relaunch.
- Terminate a running experiment only when the user requests it or continuing would violate an explicit safety or resource constraint.
- Pause for user input only when a decision would materially change the run and cannot be resolved from the available context. Do not complete the active Goal while awaiting that decision.

## Verify and Report

- Do not equate process exit with success. Verify terminal status, expected artifacts, parseability, completion markers, and metrics before declaring success or completing any active Goal.
- Finish only after verified completion, conclusive failure with no reasonable recovery path, or an explicitly requested stop.
- Give brief progress updates, then report the final configuration, exact commands, code state, GPU mapping, timing, paths, metrics, comparisons, failures, retries, deviations, partial results, and anything estimated, inferred, unresolved, or still requiring action.

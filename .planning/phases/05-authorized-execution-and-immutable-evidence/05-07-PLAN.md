---
phase: 05-authorized-execution-and-immutable-evidence
plan: 07
type: execute
wave: 4
depends_on:
  - 05-05
files_modified:
  - experiments/specchoice-v1.3.2/validation/guarded_regress.py
  - experiments/specchoice-v1.3.2/tests/test_guarded_regress.py
autonomous: true
requirements:
  - TS-07
  - TS-11
  - TS-12
estimate:
  tokens: 27000
  raw_tokens: 27000
  tasks: 3
  confidence: low
must_haves:
  truths:
    - "Before any harness/test/formal/evidence write, a bounded read-only native calibration runs the fixed sandboxed IPv4 TCP connect to 127.0.0.1:0 three times and admits implementation only when every trial returns errno.EPERM plus the exact intended diagnostic; any other or unstable outcome escalates immediately without admitting regression."
    - "D-05/D-06/D-07: after successful calibration, native admission requires a successfully constructed IPv4 TCP socket whose connect use to fixed loopback address 127.0.0.1 and port 0 is denied as the calibrated errno.EPERM/diagnostic pair; construction-only, successful-connect, refused, timed-out, or otherwise ambiguous outcomes fail closed before regression."
    - "The connection probe cannot address a remote host or a listening endpoint, unit tests use only the injected runner, and no real successful connection is permitted."
    - "The exact /usr/bin/sandbox-exec path, deterministic deny profile, literal ./bin/regress --all argv, offline environment, protected formal/install/cache paths, and no-bare-fallback boundary remain intact."
    - "D-02/D-03/D-08/D-13: the current formal successor root, receipt, report, and optional history are audited read-only; the identical formal invocation performs zero writes and each of two guarded full regressions preserves the exact twelve-leaf inventory and SHA-256 map."
    - "D-01/D-04/D-09/D-10/D-11/D-12/D-14/D-15/D-16: current completed Red evidence and attempt semantics remain unchanged, TS-11/TS-12 remain conditional pending Phase 7, and validation grants no formal, model, metric, publication, or requirement-closing authority."
  artifacts:
    - path: experiments/specchoice-v1.3.2/validation/guarded_regress.py
      provides: "Validation-only native confinement whose network preflight distinguishes the pre-execution-calibrated EPERM connect denial and exact diagnostic from every non-denial outcome."
      contains: "socket.connect"
    - path: experiments/specchoice-v1.3.2/tests/test_guarded_regress.py
      provides: "Injected-runner contracts for construction-before-connect, the fixed loopback/port-zero target, exact denial admission, ambiguity rejection, retained confinement, and evidence immutability."
      contains: "test_network_preflight"
  key_links:
    - from: experiments/specchoice-v1.3.2/validation/guarded_regress.py
      to: /usr/bin/sandbox-exec
      via: "The exact native binary applies the deterministic profile to the connection probe and the fixed regression argv; no alternate or bare path exists."
      pattern: "_SANDBOX_EXEC|_guard_argv"
    - from: experiments/specchoice-v1.3.2/validation/guarded_regress.py
      to: bin/regress
      via: "Only the literal internal argv ./bin/regress --all is admitted after all native preflights pass."
      pattern: "_FIXED_REGRESSION_ARGV"
    - from: experiments/specchoice-v1.3.2/validation/guarded_regress.py
      to: experiments/specchoice-v1.3.2/runs/red-execution-v2/
      via: "Descriptor-held exact inventory and raw SHA-256 snapshots bracket each guarded full regression."
      pattern: "snapshot_v2_evidence"
---

<objective>
Calibrate the execution host's exact native denial representation read-only before implementation, correct the validation-only native guard so admission proves denied connection use rather than denied socket construction, then complete the retained read-only exact-resume audit and two native-confined repository-wide regressions without changing any formal byte or authority per D-01 through D-16.

Purpose: Replace the failed 05-06 validation assertion with a host-pinned, fail-closed connection-use contract while preserving the entire completed Red evidence chain and partial failure history.
Output: Corrected `guarded_regress.py` and `test_guarded_regress.py`, followed only after success by `05-07-SUMMARY.md`; no formal, attempt, evidence, policy, CLI, requirement, Gate A, or Gate B change.
</objective>

<execution_context>
Follow the repository-configured GSD execute-plan and summary contracts. Run every command from the repository root or the exact relative directory stated below. The historical 05-06 plan and cancellation are read-only inputs.
</execution_context>

<context>
@AGENTS.md
@.planning/PROJECT.md
@.planning/REQUIREMENTS.md
@.planning/ROADMAP.md
@.planning/STATE.md
@.planning/phases/05-authorized-execution-and-immutable-evidence/05-CONTEXT.md
@.planning/phases/05-authorized-execution-and-immutable-evidence/05-NATIVE-GUARD-SUCCESSOR-RESEARCH.md
@.planning/phases/05-authorized-execution-and-immutable-evidence/05-VALIDATION.md
@.planning/phases/05-authorized-execution-and-immutable-evidence/05-06-CANCELLATION.md
@.planning/phases/05-authorized-execution-and-immutable-evidence/05-06-FAILED-CLOSED.md
@.planning/phases/05-authorized-execution-and-immutable-evidence/05-05-SUMMARY.md
@experiments/specchoice-v1.3.2/validation/guarded_regress.py
@experiments/specchoice-v1.3.2/tests/test_guarded_regress.py
@experiments/specchoice-v1.3.2/config/execution/red-execution-policy-v2.json
@experiments/specchoice-v1.3.2/src/specchoice_execution/red_v2.py
@experiments/specchoice-v1.3.2/src/specchoice_execution/cli_v2.py
@experiments/specchoice-v1.3.2/tests/test_authorized_execution_v2.py
@experiments/specchoice-v1.3.2/receipts/red-execution-v2.json
@experiments/specchoice-v1.3.2/reports/red-execution/red-execution-v2.md

<interfaces>
- Keep `FORMAL_FILENAMES`, `snapshot_v2_evidence(repo_root)`, `build_sandbox_profile(repo_root, probe_root)`, `preflight_native_guard(...)`, `run_guarded_command(...)`, `main()`, the injected `Runner`, `_SANDBOX_EXEC`, and `_FIXED_REGRESSION_ARGV` as the existing public/internal seams.
- Before either validation source file is edited, run exactly three bounded trials of the fixed `/usr/bin/sandbox-exec` calibration profile `(version 1)`, `(allow default)`, `(deny file-write*)`, `(deny network*)` and Python-standard-library `socket.AF_INET`/`socket.SOCK_STREAM` connect to numeric address `127.0.0.1`, port `0`. The only accepted stable tuple is child return code `77`, empty stderr, and stdout exactly `GUARDED_REGRESS_NETWORK_CONNECT_DENIED errno=1 diagnostic=Operation not permitted\n`, produced only when the caught exception is `errno.EPERM` and its diagnostic equals `os.strerror(errno.EPERM)`. Any different/unstable tuple, timeout, signal, or successful connect is a blocking escalation before implementation, formal/evidence access, summary creation, or regression admission.
- After that calibration passes, the production network child contract is fixed to the same Python standard-library family/type/address/port and exact observed EPERM/diagnostic tuple. Socket construction must complete before `connect` is attempted. The parent admits only dedicated child return code `77` plus the exact deterministic denial line; every other return code/stdout/stderr combination remains `GUARDED_REGRESS_NETWORK_PROBE_NOT_DENIED`.
- The target is loopback-only and port zero has no listening endpoint. Do not start a listener, select a routable or remote address, perform DNS, or accept any successful connection.
- Preserve `(version 1)`, `(allow default)`, `(deny network*)`, every existing protected formal/tool/install/cache path, offline/no-update environment controls, exact evidence enumeration, output hashing, and the fixed native-confined full-regression argv.
- The validation harness remains outside formal execution and the frozen policy closure; `red_v2.py` and `cli_v2.py` neither import nor call it.
</interfaces>
</context>

## Artifacts Produced

- A terminal-only, three-trial native calibration observation before implementation; no calibration file, formal/evidence write, or regression run.
- `experiments/specchoice-v1.3.2/validation/guarded_regress.py` with the corrected connection-use admission contract pinned to the accepted calibration tuple.
- `experiments/specchoice-v1.3.2/tests/test_guarded_regress.py` with exact injected-runner denial, ambiguity, fixed-target, retained-profile, fixed-argv, and evidence-snapshot coverage.
- `.planning/phases/05-authorized-execution-and-immutable-evidence/05-07-SUMMARY.md` only after every focused check, exact formal replay, and both guarded full regressions pass.

## Scope Non-Goals

- No change to formal evidence, attempt history, receipts, reports, current policy, formal executor/CLI/tests, Phase 4 authority, Gate A/Gate B records, requirements, dependencies, routes, firewall, proxy, privileges, or operating-system configuration.
- No provider, model, credential, production retrieval, external network, arbitrary command, package installation, cache update, metric, model-call ledger row, matrix cell, placeholder result, feasibility conclusion, or external publication.
- No `05-06-SUMMARY.md`, no completion claim for 05-06, and no rewrite of `05-06-FAILED-CLOSED.md` or `05-06-CANCELLATION.md`.

<tasks>

<task type="tracer">
  <name>05-07-01: Calibrate the exact native connection-denial representation read-only</name>
  <precondition>`05-06-FAILED-CLOSED.md` hashes to `010075d58b77688284c7ff3c3113cdd3c22aae5d331998d667a9c6eb8f68655c`, `05-06-CANCELLATION.md` binds both partial commits and the observed diagnostic, and neither validation source file nor any formal/evidence byte has been changed for 05-07.</precondition>
  <files>None; this task performs only bounded terminal observation and creates or modifies no file. It must not create a calibration artifact, summary, commit, formal/attempt/evidence leaf, receipt, report, cache, listener, or log.</files>
  <action>
1. Before editing `validation/guarded_regress.py` or `tests/test_guarded_regress.py`, run exactly three trials through exact `/usr/bin/sandbox-exec` with the deterministic calibration profile `(version 1)`, `(allow default)`, `(deny file-write*)`, `(deny network*)`. The global terminating file-write denial makes the calibration strictly read-only rather than relying on intent. Each child uses `/usr/bin/python3`, constructs one `socket.AF_INET`/`socket.SOCK_STREAM` socket, applies a one-second socket timeout, and calls `connect(("127.0.0.1", 0))`; the parent applies a two-second subprocess timeout to each trial. Use the numeric loopback address directly, create no listener, perform no DNS, and never select another address or port.
2. Capture each trial's return code, stdout, and stderr in memory and print the three observed tuples to the terminal. Accept the calibration only when all three tuples are byte-identical: return code `77`, stdout exactly `GUARDED_REGRESS_NETWORK_CONNECT_DENIED errno=1 diagnostic=Operation not permitted\n`, and empty stderr. The child may emit that line and code only after catching an `OSError` whose `errno` equals `errno.EPERM` and whose diagnostic equals `os.strerror(errno.EPERM)`; it must close the socket in every path.
3. Treat a returned `connect`, `ECONNREFUSED`, timeout, unreachable/address error, construction error, signal, altered/missing/extra output, non-empty stderr, different return code, or cross-trial instability as `GUARDED_REGRESS_NATIVE_PREFLIGHT_CALIBRATION_MISMATCH`. Escalate immediately and stop the plan without editing code/tests, reading or invoking formal execution, writing any formal/evidence/planning result, creating `05-07-SUMMARY.md`, or running either focused or repository-wide regression. Do not reinterpret a mismatch, change the address/profile, introduce a listener, or replace the expected tuple.
  </action>
  <verify>
    <automated>PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -c 'import subprocess; profile="(version 1)\n(allow default)\n(deny file-write*)\n(deny network*)\n"; probe="import errno, os, socket, sys\ns=socket.socket(socket.AF_INET, socket.SOCK_STREAM)\ns.settimeout(1.0)\ntry:\n s.connect((\"127.0.0.1\", 0))\nexcept OSError as error:\n diagnostic=error.strerror or os.strerror(error.errno)\n print(f\"GUARDED_REGRESS_NETWORK_CONNECT_DENIED errno={error.errno} diagnostic={diagnostic}\")\n sys.exit(77 if error.errno == errno.EPERM and diagnostic == os.strerror(errno.EPERM) else 78)\nelse:\n print(\"GUARDED_REGRESS_NETWORK_CONNECT_SUCCEEDED\")\n sys.exit(79)\nfinally:\n s.close()"; argv=["/usr/bin/sandbox-exec","-p",profile,"/usr/bin/python3","-c",probe]; runs=[subprocess.run(argv,capture_output=True,text=True,timeout=2,check=False) for _ in range(3)]; observed=[(run.returncode,run.stdout,run.stderr) for run in runs]; expected=(77,"GUARDED_REGRESS_NETWORK_CONNECT_DENIED errno=1 diagnostic=Operation not permitted\n",""); print(observed); raise SystemExit(0 if observed == [expected,expected,expected] else 1)'</automated>
  </verify>
  <done>Three bounded native trials produce the identical measured EPERM/exact-diagnostic tuple on fixed loopback port zero with no listener, external traffic, successful connection, file write, formal/evidence access, or regression admission; otherwise the plan has escalated and stopped without writes.</done>
</task>

<task type="auto" tdd="true">
  <name>05-07-02: Prove the calibrated native connection-use denial path end to end</name>
  <precondition>`05-06-FAILED-CLOSED.md` hashes to `010075d58b77688284c7ff3c3113cdd3c22aae5d331998d667a9c6eb8f68655c`, `05-06-CANCELLATION.md` binds both partial commits and the observed diagnostic, and `05-05-SUMMARY.md` records completed current formal publication and exact resume.</precondition>
  <files>experiments/specchoice-v1.3.2/tests/test_guarded_regress.py, experiments/specchoice-v1.3.2/validation/guarded_regress.py</files>
  <behavior>
    - "The injected runner sees a Python network probe that constructs an AF_INET/SOCK_STREAM socket and then calls connect on exactly 127.0.0.1 port 0; construction-only bytecode cannot satisfy admission."
    - "Only the Task 05-07-01 measured tuple—errno.EPERM, dedicated return code 77, exact `GUARDED_REGRESS_NETWORK_CONNECT_DENIED errno=1 diagnostic=Operation not permitted` stdout, and empty stderr—admits the regression child."
    - "A zero return, an ordinary refused/timed-out/unreachable errno, a signal, missing or altered marker, denial during construction, or any other ambiguity raises GUARDED_REGRESS_NETWORK_PROBE_NOT_DENIED before the regression child."
    - "Unit tests invoke only runner doubles: they open no socket, start no listener, perform no DNS, contact no remote target, and never invoke the real full regression."
    - "All pre-existing unavailable-guard, nonfunctional-profile, protected-write, prohibited-child, evidence add/change/remove, fixed-argv, and unchanged-success contracts remain green."
  </behavior>
  <action>
1. Only after Task 05-07-01 records three identical accepted tuples in the terminal, write the failing tests first. Add `test_network_preflight_requires_connect_to_fixed_loopback_port_zero`, `test_network_preflight_accepts_only_calibrated_eperm_diagnostic`, and `test_network_preflight_rejects_connect_success_and_ambiguous_failure`. Extend the existing runner double to inspect the Python probe argv and return explicit stdout/stderr/return-code combinations; require the command text to create `socket.AF_INET`/`socket.SOCK_STREAM` and call `.connect(("127.0.0.1", 0))`. Preserve the existing tests and prove they never call Python's real socket API or the real regression.
2. Replace only the current network-probe constant and its result check. The child must construct the socket, set the bounded timeout, attempt the fixed loopback/port-zero connect inside `/usr/bin/sandbox-exec`, catch `OSError`, and emit exactly `GUARDED_REGRESS_NETWORK_CONNECT_DENIED errno=1 diagnostic=Operation not permitted` with return code `77` only when the actual exception matches the Task 05-07-01 calibrated `errno.EPERM` and diagnostic. A successful connect, construction denial, any other errno/diagnostic, timeout, signal, non-empty stderr, malformed output, or code/output mismatch must remain the existing stable `GUARDED_REGRESS_NETWORK_PROBE_NOT_DENIED` pre-regression failure. Close the socket deterministically.
3. Keep the native path/profile, write probe, protected paths, offline environment, snapshot logic, output digests, fixed regression argv, CLI arguments, and no-fallback behavior byte-for-byte unless a test assertion must name the new network contract. Do not add a dependency, listener, DNS lookup, remote address, command override, or formal-execution import.
  </action>
  <verify>
    <automated>cd experiments/specchoice-v1.3.2 &amp;&amp; PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src ../../.venv/bin/python -m unittest tests.test_guarded_regress.GuardedRegressTests.test_network_preflight_requires_connect_to_fixed_loopback_port_zero tests.test_guarded_regress.GuardedRegressTests.test_network_preflight_accepts_only_calibrated_eperm_diagnostic tests.test_guarded_regress.GuardedRegressTests.test_network_preflight_rejects_connect_success_and_ambiguous_failure tests.test_guarded_regress.GuardedRegressTests.test_unavailable_guard_fails_before_child tests.test_guarded_regress.GuardedRegressTests.test_bad_or_nonfunctional_profile_fails_before_child tests.test_guarded_regress.GuardedRegressTests.test_prohibited_child_result_is_failure tests.test_guarded_regress.GuardedRegressTests.test_evidence_change_addition_and_removal_fail tests.test_guarded_regress.GuardedRegressTests.test_unchanged_fake_local_command_succeeds_without_network -q &amp;&amp; ../../.venv/bin/ruff check --isolated validation/guarded_regress.py tests/test_guarded_regress.py</automated>
  </verify>
  <done>The real production preflight admits exactly a constructed socket whose fixed loopback connect is denied as EPERM, every non-denial or ambiguous result stops before regression, and all retained harness contracts pass without real unit-test network use.</done>
</task>

<task type="auto">
  <name>05-07-03: Re-run the formal zero-write audit and two native-confined release gates</name>
  <precondition>The corrected real native preflight from Task 05-07-02 still returns the exact tuple measured by Task 05-07-01 on the execution host; unavailable sandbox application or a changed/unrecognized native denial representation is a blocking failure with no bare-regression fallback.</precondition>
  <files>None; this task is read-only over formal, attempt, receipt, report, source, policy, test, dependency, and requirement paths. The executor creates only `05-07-SUMMARY.md` after all checks pass.</files>
  <action>
1. Re-run the bounded real native preflight before any formal command and require the exact three-trial calibration tuple from Task 05-07-01. A successful connection, external/routable target, listener, ordinary endpoint error, timeout, signal, altered output, or host drift stops immediately with no formal/evidence writes and no regression. Only then snapshot the exact current formal root, optional attempt/successor namespaces, receipt, and report before validation. Run the existing read-only successor validator and the identical ten-option production `execute-red` invocation. Require the same canonical receipt, exact inventory/bytes/SHA-256/write-observable metadata, and zero writes per D-01/D-02/D-03/D-05/D-08/D-13/D-14/D-16; stop without repair, deletion, cleanup, migration, regeneration, or summary normalization on any mismatch.
2. Run the complete current guarded-harness, predecessor/successor execution, data, treatment, canonical, and filesystem unittest modules plus Ruff and `git diff --check`. Confirm D-04/D-07/D-09/D-10/D-11/D-12/D-15 and TS-07/TS-11/TS-12 remain unchanged: current status stays completed Red, the real-call ledger and matrix remain empty/zero, conditional requirements remain pending Phase 7, and no metric, model/provider/credential/retrieval surface, broader authority, or Gate A/Gate B change appears.
3. From the repository root, invoke `validation/guarded_regress.py --repo-root .` exactly twice. Each invocation must independently pass the harmless, pinned connection-use, and protected-write preflights, launch only literal `./bin/regress --all` through the exact native profile, and prove the exact ten formal leaves plus receipt/report repository-relative inventory and SHA-256 unchanged before and after. The second successful invocation is the deterministic zero-write release proof.
4. If either guard application, expected EPERM classification, prohibited-operation denial, regression, install/cache protection, formal replay, or evidence comparison fails, stop and preserve the diagnostic; do not run a bare command or create a completion summary. After both passes, record only commands, return status, guard/profile identity, output digests, and before/after manifest equality in `05-07-SUMMARY.md`; that summary remains non-authoritative validation metadata.
  </action>
  <verify>
    <automated>cd experiments/specchoice-v1.3.2 &amp;&amp; PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src ../../.venv/bin/python -m specchoice_execution.cli_v2 execute-red --repo-root . --policy config/execution/red-execution-policy-v2.json --authority phase4/branch-authority-v6.json --packet reports/h3/h3-red-review-v6/review-packet.json --readiness receipts/h3-branch-readiness-v6.json --decision reviews/h3-branch-decision-v6.json --attempt-root runs/red-attempts-v2 --formal-root runs/red-execution-v2 --receipt receipts/red-execution-v2.json --report reports/red-execution/red-execution-v2.md &amp;&amp; PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src ../../.venv/bin/python -m unittest tests.test_data_admission tests.test_data_splits tests.test_data_relevance tests.test_data_h2 tests.test_treatments_frame tests.test_treatments_prompts tests.test_treatments_retrieval tests.test_treatments_h3 tests.test_authorized_execution tests.test_authorized_execution_v2 tests.test_guarded_regress tests.test_canonical tests.test_filesystem_boundary -q &amp;&amp; ../../.venv/bin/ruff check --isolated src/specchoice_execution validation/guarded_regress.py tests/test_authorized_execution.py tests/test_authorized_execution_v2.py tests/test_guarded_regress.py &amp;&amp; git diff --check &amp;&amp; cd ../.. &amp;&amp; PYTHONDONTWRITEBYTECODE=1 .venv/bin/python experiments/specchoice-v1.3.2/validation/guarded_regress.py --repo-root . &amp;&amp; PYTHONDONTWRITEBYTECODE=1 .venv/bin/python experiments/specchoice-v1.3.2/validation/guarded_regress.py --repo-root .</automated>
  </verify>
  <done>The current formal Red chain exact-resumes with zero writes, all focused checks pass, and two consecutive fixed native-confined full regressions each preserve the exact twelve-file evidence inventory and SHA-256 map without a remote connection, install/cache/formal write, bare fallback, or authority change.</done>
</task>

</tasks>

## Plan-Set Multi-Source Coverage Audit

| Source | ID | Feature / constraint | Plan | Status |
|---|---|---|---|---|
| GOAL | — | Complete immutable authorized-branch evidence without unauthorized calls, hidden repair, asymmetric retries, or favorable subsets. | 05-04, 05-05, 05-07 | COVERED |
| REQ | TS-07 | Preserve and re-audit separate immutable raw/parsed/diagnostic/span custody. | 05-07-03 | COVERED |
| REQ | TS-11 | Preserve the Red zero-cell/no-G-Y-execution boundary and pending-Phase-7 state. | 05-07-03 | COVERED |
| REQ | TS-12 | Preserve the empty real-call ledger and prove no hidden call during guarded validation. | 05-07-01, 05-07-02, 05-07-03 | COVERED |
| RESEARCH | — | Preserve partial 05-06 history outside `*-PLAN.md` discovery with no fabricated summary. | 05-06 cancellation/archive | COVERED |
| RESEARCH | — | Exercise connection use after socket construction; construction alone is not the admission criterion. | 05-07-01, 05-07-02 | COVERED |
| RESEARCH | — | Measure the host-specific native denial representation before implementation and fail closed rather than guessing it. | 05-07-01 | COVERED |
| RESEARCH | — | Distinguish exact native denial from ordinary endpoint failure and fail closed on ambiguity. | 05-07-01, 05-07-02 | COVERED |
| RESEARCH | — | Use only standard library, current repository primitives, and the existing native guard; add no package. | 05-07-01, 05-07-02 | COVERED |
| RESEARCH | — | Retain fixed argv/profile, offline/install protections, exact evidence snapshots, and two guarded full regressions. | 05-07-02, 05-07-03 | COVERED |
| RESEARCH | — | Keep validation outside formal closure and require no new Gate A or Gate B. | 05-07-01, 05-07-02, 05-07-03 | COVERED |
| CONTEXT | D-01 | Preserve the exact mutually bound completed contract. | 05-07-03 | COVERED |
| CONTEXT | D-02 | Prove byte-identical zero-write resume without overwrite/regeneration. | 05-07-03 | COVERED |
| CONTEXT | D-03 | Preserve separate failed custody and all-or-nothing formal publication. | 05-07-03 | COVERED |
| CONTEXT | D-04 | Keep completion permission limited to downstream Red-evidence evaluation. | 05-07-03 | COVERED |
| CONTEXT | D-05 | Preserve the three-layer zero-call proof. | 05-07-01, 05-07-02, 05-07-03 | COVERED |
| CONTEXT | D-06 | Retain formal all-socket denial while measuring and correctly testing native connection-use denial. | 05-07-01, 05-07-02 | COVERED |
| CONTEXT | D-07 | Keep the real-call ledger empty and blocked operations separate. | 05-07-03 | COVERED |
| CONTEXT | D-08 | Re-audit exact v6 and current execution closure roots. | 05-07-03 | COVERED |
| CONTEXT | D-09 | Preserve the canonical exact Red zero-cell matrix. | 05-07-03 | COVERED |
| CONTEXT | D-10 | Preserve TS-11/TS-12 conditional pending-Phase-7 state. | 05-07-03 | COVERED |
| CONTEXT | D-11 | Preserve formula/partition zeros and absence of unregistered artifacts. | 05-07-03 | COVERED |
| CONTEXT | D-12 | Preserve canonical JSON authority, deterministic Markdown, and no metrics/success claim. | 05-07-03 | COVERED |
| CONTEXT | D-13 | Treat any frozen formal-byte drift as requiring another separately authorized successor. | 05-07-03 | COVERED |
| CONTEXT | D-14 | Preserve complete immutable failed-attempt semantics. | 05-07-03 | COVERED |
| CONTEXT | D-15 | Keep validation non-authorizing and current v6 unable to authorize changed formal bytes. | 05-07-01, 05-07-02, 05-07-03 | COVERED |
| CONTEXT | D-16 | Preserve immutable ordered retry history and empty ledgers. | 05-07-03 | COVERED |

<threat_model>
## Trust Boundaries

| Boundary | Description |
|---|---|
| calibration child -> implementation admission | Three bounded read-only trials must expose the exact stable EPERM/diagnostic tuple before code, evidence, or regression work begins; any drift escalates without writes. |
| network-probe child -> regression admission decision | A generic nonzero result is untrusted; only the pre-execution-calibrated EPERM return-code/stdout/stderr contract proves native denial. |
| probe target -> host/network | The child may address only loopback `127.0.0.1:0`, with no listener, DNS, remote route, or accepted connection. |
| repository regression -> network/install surfaces | The broad suite is admitted only through the exact native profile with offline controls and protected writes. |
| repository regression -> formal evidence | Each run is invalid if any formal leaf, receipt, or report changes, appears, disappears, becomes unsafe, or moves. |
| cancelled plan -> GSD discovery | Historical 05-06 bytes must remain auditable without being redispatched or falsely summarized. |
| validation result -> formal authority | Passing release validation cannot authorize models, metrics, publication, requirement closure, or changed formal bytes. |

## STRIDE Threat Register — ASVS L1

| Threat ID | Category | Component | Severity | Disposition | Mitigation Plan |
|---|---|---|---|---|---|
| T-05-07-01 | Elevation of Privilege | native-denial calibration | critical | mitigate | Before implementation, require three bounded identical trials of the exact fixed sandbox/profile/connect command; accept only errno.EPERM, return code 77, exact intended stdout diagnostic, and empty stderr, otherwise escalate with zero formal/evidence writes and no regression. |
| T-05-07-02 | Information Disclosure | connection target | high | mitigate | Hard-code loopback `127.0.0.1:0`, create no listener, perform no DNS, reject any connect success, and use injected runners in unit tests. |
| T-05-07-03 | Elevation of Privilege | regression subprocess | critical | mitigate | Pin production admission to the calibrated tuple and preserve exact `/usr/bin/sandbox-exec`, deterministic profile, literal internal argv, single `--repo-root` interface, and no shell/override/bare fallback. |
| T-05-07-04 | Tampering | formal evidence and install/cache roots | critical | mitigate | Retain terminating write denials, offline controls, descriptor-held exact inventory/hash snapshots, and fail on any before/after delta around both full runs. |
| T-05-07-05 | Repudiation | partial 05-06 lifecycle | high | mitigate | Preserve byte-identical `05-06-FAILED-CLOSED.md`, bind both commits and the observed diagnostic in cancellation, and never create `05-06-SUMMARY.md`. |
| T-05-07-06 | Repudiation / Elevation of Privilege | validation authority | high | mitigate | Keep the harness outside formal closure and record only non-authoritative validation results after all passes; no Gate or requirement state changes. |
| T-05-SC | Tampering | validation toolchain | high | mitigate | Use only pinned `.venv`, standard library, installed repository primitives, and the exact native guard; install, download, upgrade, route, proxy, firewall, privilege, and OS changes remain prohibited. |
</threat_model>

<verification>
- Confirm the archive remains byte-identical, no `05-06-SUMMARY.md` exists, and `phase-plan-index 05` discovers 05-07 rather than 05-06.
- Before any implementation or formal/evidence access, run Task 05-07-01's exact three-trial bounded calibration and require the identical EPERM/return-code/stdout/stderr tuple; any mismatch stops with no writes and no regression.
- Run the exact focused test selectors in Task 05-07-02, then the full current focused suite, Ruff, and `git diff --check` from Task 05-07-03.
- Re-run the identical formal command and require the same canonical receipt with zero writes.
- Invoke only the harness twice for the repository-wide regression; each invocation must pass exact native connection/write admission and exact evidence before/after equality.
- Confirm no formal, evidence, policy, CLI, requirement, dependency, Gate A, or Gate B byte changed.
</verification>

<success_criteria>
- The read-only native calibration runs first, observes the same exact EPERM/diagnostic tuple three times, and otherwise escalates before any code, formal/evidence, summary, or regression write.
- The corrected native preflight proves actual connect denial after successful construction against the calibrated tuple and rejects every generic or ambiguous connection failure.
- The connection target is fixed loopback/port-zero, cannot be a real remote or listening endpoint, and no successful connection is accepted.
- The fixed native profile, argv, offline controls, protected paths, evidence snapshots, and no-bare-fallback contract remain effective.
- The identical formal command performs zero writes and both guarded full regressions pass with exact twelve-leaf inventory/hash equality.
- Completed Red evidence, all D-01 through D-16 invariants, and TS-07/TS-11/TS-12 status remain unchanged; validation grants no additional authority.
- 05-06 remains failed-closed historical evidence without a summary, and 05-07 is the sole discoverable incomplete successor.
</success_criteria>

<output>
Create `.planning/phases/05-authorized-execution-and-immutable-evidence/05-07-SUMMARY.md` when done. Never create `05-06-SUMMARY.md`.
</output>

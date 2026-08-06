# AI-assisted extraction of RISC-V architectural parameters

## Submission contents

- `architectural-parameters.yaml` — reviewed structured extraction result
- `inputs/privileged-19.3.1-cache-blocks.txt` — cache-block challenge input
- `inputs/privileged-2.1-csr-address-mapping.txt` — fixed-CSR negative input
- `CHECKSUMS.sha256` — SHA-256 inventory for the submitted files

## Verification

From the submission root, use `shasum` on macOS or `sha256sum` on GNU/Linux:

```bash
shasum -a 256 -c CHECKSUMS.sha256
# GNU/Linux equivalent: sha256sum -c CHECKSUMS.sha256

ruby -e '
  require "yaml"
  YAML.safe_load(
    File.read("architectural-parameters.yaml"),
    permitted_classes: [],
    aliases: false
  )
  puts "YAML parse: PASS"
'
```

## LLM disclosure

- Provider: OpenAI
- Interface: Codex desktop
- Runtime-reported model family: GPT-5
- Displayed model label retained with this run: unavailable
- Exact serving snapshot: not exposed by the interface
- Context window: not exposed by the interface
- Sampling parameters: platform managed and not exposed
- Analysis date: 2026-08-04

The Codex runtime reported the model family as GPT-5. The interface did not
expose an exact serving snapshot, context-window value, or sampling
configuration, so those fields are recorded as unavailable.

## Prompt development

The initial high-recall idea was to treat words such as *may*, *optional*, and
*implementation-specific* as parameter markers. That is useful for candidate
discovery, but it is not a valid final decision rule: the CSR snippet contains
many numbers and bit fields while describing an ISA-fixed convention, not an
implementation choice.

The prompt was refined in three steps:

1. Treat modal and implementation-specific wording only as a candidate signal.
2. Require an explicit semantic decision about who selects the value and
   whether the choice space is implementation-selected or ISA-fixed.
3. Require evidence, represent unsupported details as unknown, and forbid
   invented bounds, units, enumerations, dependencies, defaults, or claims of
   canonical naming. A normative constraint may constrain an accepted
   parameter, but must not automatically become another parameter.

The final prompt was:

```text
You extract implementation-selectable architectural parameters from RISC-V
specification text.

Trigger words such as may, might, should, optional, implementation-defined,
and implementation-specific are candidate signals only. Never accept a
parameter from a keyword or a number alone.

For each candidate noun phrase:
1. Identify the authority: implementation, ISA, software, execution
   environment, or unknown.
2. Identify the choice object: value, count, width, legal set, access mode,
   presence, organization, or other.
3. Identify the choice-space origin: implementation-selected, ISA-fixed,
   derived, not applicable, or unknown.
4. Accept only an implementation-selectable architectural property. Classify
   ISA-fixed encodings, prose definitions, software advice, and constraints
   that introduce no choice as non-parameters. Use review when the text signals
   an implementation-specific property but does not support a safe schema.
5. Quote evidence for every accepted, review, or non-parameter decision.
6. Use only constraints stated or logically entailed by the supplied text.
   Never invent a bound, unit, enum member, dependency, or default. Preserve an
   unknown as null or "unspecified".
7. A shall/must statement attached to an accepted parameter may be recorded as
   a constraint; it is not automatically a separate parameter.
8. Do not claim that a normalized name is canonical unless the specification
   or an independently verified database supplies it. For every generated
   parameter name, include source_phrase and name_status, where name_status is
   explicit, proposed_normalized, or existing_udb_verified. If a database was
   used to verify an existing name, include its source path. For unresolved
   candidates, use a plain candidate_label and proposed_name: null.

Return YAML only. The document must contain schema_version and results. Each
result must contain exactly source, status, parameters, review_candidates, and
non_parameters. Each accepted parameter must contain name, name_status,
source_phrase, description, type, type_support, units, constraints, and
evidence. Keep evidence attached to the decision it supports.
```

## SpecChoice: broader technical framing

This submission applies the core idea of SpecChoice: RISC-V architectural-
parameter extraction is a structured delegation-analysis problem, not keyword
spotting. For each passage, the method asks who controls the choice, what
property is being selected, and whether the allowed choice space is
implementation-selected or ISA-fixed. It then separates candidate surfacing,
final disposition, canonical identity, and evidence support, so fixed encodings
and unresolved scope questions are not collapsed into a single
parameter-or-non-parameter guess.

The accompanying local SpecChoice implementation established a
content-addressed, offline-replayable evidence boundary and a deterministic
measurement spine for all eleven public PR #2164 fixtures. The Phase 1 evidence
boundary passed its 92-test standard-library suite, and the formal golden replay
separately verifies surfacing, disposition, identity, evidence integrity, and
negative controls.

A preregistered human data audit established that the current public material
supports one defensible natural contrastive pair but not a family-disjoint
held-out benchmark. The project therefore followed its predefined Red
feasibility path rather than report an invalid model comparison. This identifies
the next concrete mentorship task: maintainer-assisted semantic adjudication
and construction of a trustworthy contrastive benchmark before testing the
DelegationFrame and axis-contrastive retrieval hypotheses.

## Hallucination controls

- Evidence is checked as a whitespace-normalized verbatim quotation. Runs of
  whitespace may differ because the supplied snippets are line-wrapped, but
  punctuation, words, numbers, and token order must otherwise match exactly.
- The authority/choice-space test prevents fixed CSR bit assignments from being
  mistaken for configurable parameters.
- `review` preserves high recall without fabricating a type for cache capacity
  or cache organization.
- Unknown values remain `null` or `unspecified`; in particular, the cache-block
  snippet gives no maximum size.
- The output is parsed as YAML and checked for required keys. A production
  pipeline should reject malformed output instead of repairing it silently.

## Generation and review procedure

- Development process: iterative prompt design and output review in Codex
  desktop.
- Submission artifact: a reviewed and schema-validated final extraction
  produced through the interactive Codex workflow. Raw responses were treated
  as intermediate work products rather than final results.
- Primary extraction input: whitespace-cleaned local copies of the two supplied
  challenge snippets in `inputs/`.
- Additional review sources: the local UnifiedDB checkout and its pre-existing
  reviewed fixtures were consulted to verify the existing
  `CACHE_BLOCK_SIZE` identity and the fixed-CSR negative-control
  interpretation. They were not used to add constraints absent from the
  supplied snippets.
- Post-generation edits: schema normalization, explicit naming provenance,
  removal of unsupported units and bounds, evidence punctuation correction,
  and attachment of evidence to each individual decision.
- Validation: Ruby's standard-library YAML parser loaded the file; exact result
  and required-key sets were checked; every evidence quotation was compared to
  its source after whitespace normalization; package checksums were independently
  verified.

The extracted result is in
[`architectural-parameters.yaml`](architectural-parameters.yaml).

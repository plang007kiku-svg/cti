# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repository is

This is a **data repository**, not a software project. It holds the Cloud Security Alliance's
CAVEaT (Cloud Adversarial Vectors, Exploits, and Threats) cloud threat-intelligence corpus as
**STIX 2.1 JSON objects**. There is no build, lint, test, or CI pipeline, and nothing to run —
work here means adding, editing, or validating JSON data files.

CAVEaT's distinguishing approach (see `README.md`): instead of generic mitigations, each
`course-of-action` carries **provider-specific, actionable remediation** (exact console paths,
CLI commands, API calls) for AWS / Azure / GCP. Threats are identified "evidence-based" — i.e.
where cloud providers invest in dedicated security services.

The authoring/validation **tooling lives in a separate repo**, not here:
[WG-CAVEaT](https://github.com/CloudSecurityAlliance-WG/WG-CAVEaT). This repo is just the data.

## Data model

All data lives under `caveat/`, one directory per STIX object type:

- `caveat/attack-pattern/` — **threats** (a cloud attack technique). Uses MITRE ATT&CK-style
  vocabulary: `kill_chain_phases`, `x_mitre_platforms` (e.g. `["AWS"]`, `["Azure"]`, `["AMD EPYC"]`),
  `x_mitre_detection`, and `external_references` to CVEs / vendor bulletins / research.
- `caveat/course-of-action/` — **mitigations** (a specific cloud security control or service).
  Carries the custom `x_mitre_implementation` object with `Console_Method` / `CLI_Method` /
  `API_Method`, each a `{ description, steps[] }` block. `steps` embed fenced code (```bash, ```json)
  as plain strings.
- `caveat/relationship/` — **edges** linking the above. Always `relationship_type: "mitigates"`
  with `source_ref` = a `course-of-action--…` and `target_ref` = an `attack-pattern--…`.

Together these form a knowledge graph: course-of-action **mitigates** attack-pattern.

### Custom STIX extensions

Beyond standard STIX 2.1 fields, objects use MITRE-style `x_mitre_*` custom properties
(`x_mitre_version`, `x_mitre_domains`, `x_mitre_platforms`, `x_mitre_contributors`,
`x_mitre_detection`, `x_mitre_is_subtechnique`, `x_mitre_deprecated`) and the CAVEaT-specific
`x_mitre_implementation` (the provider-specific remediation steps).

## File conventions and known inconsistencies

- **Filenames have no extension** and are the STIX `id` with the `--` separator collapsed to a
  single `-`. Example: file `attack-pattern-0193c168-4fec-0000-9549-cfc21de144e5` holds object
  `"id": "attack-pattern--0193c168-4fec-0000-9549-cfc21de144e5"`.
- **Two storage shapes exist** — be ready for both when reading:
  1. A bare STIX object (`{ "type": "attack-pattern", ... }`), or
  2. A STIX **bundle** (`{ "type": "bundle", "objects": [ ... ] }`) wrapping one or more objects.
- **The filename ID does not always match the internal object `id`.** For the structured
  `0193c168-…`-style IDs they match; for several random-UUID and bundle-wrapped files they differ
  (e.g. file `course-of-action-d47e3896-…` contains object `course-of-action--2c8e58b3-…`).
  **Do not assume you can locate an object by its STIX ID via the filename** — grep the contents:
  `grep -rl 'attack-pattern--f9dbfbb7' caveat/`.

When adding a new object, prefer matching the surrounding files: keep one logical object per file,
name the file after its STIX `id`, and keep `created`/`modified` as ISO-8601 Z timestamps.

## Validating data

There is no validator in-repo. To sanity-check edits:

```bash
# JSON is well-formed
find caveat -type f -exec python3 -c "import json,sys; json.load(open(sys.argv[1]))" {} \;

# Every relationship's source_ref/target_ref resolves to an object that exists in the repo
# (collect all ids — including those inside bundles — then check each ref appears)
```

The MITRE / OASIS STIX tooling in the WG-CAVEaT repo is the canonical validator.

## Contributing (PR workflow)

Per `README.md`, contributions go through fork → branch → pull request against
`CloudSecurityAlliance/cti` `main`. Do not commit directly to `main`. New entries are often
drafted with the CAVEaT chatbot (links in `README.md`) and then committed as STIX files here.

License: **CC0 1.0** (public domain dedication).

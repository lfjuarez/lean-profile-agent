---
id: case-detection-coverage
title: "Case study: detection coverage assessment against MITRE ATT&CK and ATLAS"
questions:
  - How do you measure detection coverage against MITRE ATT&CK?
  - What did the detection coverage assessment deliver?
  - Do you cover MITRE ATLAS and AI application security?
---

## Context

Representative engagement for a regional bank's SOC. The SOC believed its 312 Splunk Enterprise Security rules covered "most" of ATT&CK; nobody could say which techniques, how well, or what a ransomware operator would get away with. Figures are synthetic; the method and the deliverables are the real ones. The assessment covered ATT&CK Enterprise v20 (259 techniques) scored by detection quality, and MITRE ATLAS for the bank's two customer-facing LLM applications.

## The problem

Coverage was a belief, not a measurement. Rules had piled up over six years from three vendors and two SIEM migrations; 41 depended on data no longer collected. The two customer-facing LLM applications had no security telemetry at all.

## Approach

1. Exported every enabled correlation search and EDR rule with its SPL and metadata.
2. Mapped each rule to ATT&CK and ATLAS with an AI-assisted pipeline; every mapping reviewed by hand.
3. Tested each rule against the data actually collected; scored each technique none, low, medium or high.
4. Prioritized gaps by attack-path position, sector threat relevance and effort to close.

## Results

- ATT&CK techniques covered: 48% before, 58% after the first wave.
- ATLAS (AI and LLM) coverage: 15% before, 35% once prompt and tool-call telemetry reached the SIEM.
- 41 rules retired or repaired that could never have fired.
- Coverage by tactic ranged from 11% (Resource Development) to 82% (Execution); the weakest areas were Exfiltration (20%), Collection (29%) and Reconnaissance (33%).

## Top gaps and the detection built for each

- T1486 Data Encrypted for Impact (critical): burst of renames to unknown extensions per host (EDR / Sysmon event 11).
- T1021 Remote Services (critical): first-seen admin logons between servers (Windows event 4624, logon types 3 and 10).
- AML.T0051 LLM Prompt Injection (critical): injection patterns and guardrail verdicts per session, from prompt logs sent through HEC.
- T1110 Brute Force (serious): many failures then success, per source and user, on the Authentication data model.

## Delivered

Scored heat maps for ATT&CK and ATLAS; ATT&CK Navigator layer file; rule inventory with mapping, status and owner; SPL for every proposed detection; a six-week roadmap and a walkthrough with SOC leadership.

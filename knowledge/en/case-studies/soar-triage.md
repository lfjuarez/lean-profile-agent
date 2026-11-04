---
id: case-soar-triage
title: "Case study: phishing and malware triage automation with Splunk SOAR"
questions:
  - How did you automate alert triage with Splunk SOAR?
  - What results did SOAR automation achieve after 90 days?
  - How do you keep analysts in control of automated containment?
---

## Context

Representative engagement drawn from SOAR work in the energy sector. A six-person SOC received about 1,900 phishing and malware alerts a month and triaged each one by hand across six consoles. Figures are synthetic; the playbook design, the approval model and the metrics are the real method.

## The problem

Mean time to triage was 42 minutes and the queue backed up every Monday. Analysts repeated the same lookups (hash reputation, sender history, host owner, user privileges) for every alert, and the containment actions lived in four different consoles with four sets of credentials. Nobody could report how many alerts were true positives.

## Approach

1. Measured first: two weeks of alerts classified by hand to get the real true-positive rate (11%) and the lookups analysts actually performed.
2. Built the integrations as reusable SOAR assets (EDR, email gateway, Active Directory, firewall, ticketing, sandbox) with least-privilege service accounts and tested actions.
3. Wrote the playbooks in stages: enrichment only for four weeks (analysts kept deciding), then automatic closure of low-risk false positives, then automatic containment for high-confidence verdicts on non-critical assets.
4. Every automatic action writes its evidence back to the Enterprise Security notable and the ticket, so audit never depends on SOAR alone.

## Playbook structure

Three triggers (Enterprise Security notable with risk score 60 or more, user report through a report-phish button, EDR detection) are normalized into one container schema (hash, URL, sender, host, user). One enrichment stage (VirusTotal, URL sandbox, Active Directory user and host context, asset criticality, prior cases). A verdict matrix of confidence by asset criticality with an analyst gate for medium confidence. Containment (isolate host, block sender and URL, reset credentials and revoke sessions). Ticket and close (ServiceNow incident with evidence, notable updated, metrics to Splunk).

## Verdict matrix in production

- High confidence (two independent sources agree): non-critical asset contained automatically with notification; critical asset waits at the analyst gate with a 15-minute timeout that escalates.
- Medium confidence: analyst gate with the collected evidence; for critical assets the on-call analyst is paged.
- Low or known benign: closed with evidence; for critical assets, a weekly sample review.

## Results after 90 days

- Mean time to triage: 42 minutes before, 6 minutes after.
- 78% of alerts enriched and closed or contained without an analyst touching a console.
- 14 playbooks in production, 6 integrations, 31 tested actions.
- 0 containment actions reverted as wrong in 90 days; two held at the analyst gate.

## Delivered

Playbooks and custom functions in version control; integration assets and runbooks; verdict matrix agreed with the CISO; SOC metrics dashboard in Splunk (volume, triage time, automation rate, gate decisions); two training sessions for analysts.

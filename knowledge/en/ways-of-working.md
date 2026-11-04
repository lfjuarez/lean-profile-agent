---
id: ways-of-working
title: How I work and lead
questions:
  - How do you lead a technical team?
  - How do you mentor junior engineers or transfer knowledge?
  - How do you prioritize work?
  - How do you work with clients and stakeholders?
  - How do you manage risk when changing production systems?
  - Tell me about a project you are proud of.
---

## Leading technical teams

As Technical Leader Splunk at a consulting firm (July 2020 – March 2025), Leandro led a technical team of 2 to 4 engineers delivering scalable, clustered Splunk environments for banking, finance, energy and insurance clients.

## Mentoring and knowledge transfer

He closes every engagement with a hand-off: documentation plus a session or workshop with the client's team, so the team understands and owns what was built. In that consulting role he designed and delivered knowledge-transfer programs with his own material, split by level (introductory and advanced). As a Splunk Certified Instructor he designs the progression from basic to advanced with practical exercises and assessments so students can work on their own. In the SOAR engagement he delivered two training sessions for analysts.

## Prioritizing work

He prioritizes with explicit criteria and writes them down. In the detection coverage assessment, gaps were ranked by position in the attack path, relevance of the threat to the sector and effort to close. His health checks deliver findings ordered by priority, each with evidence, impact and recommendation, followed by a roadmap. Coverage work ended with a six-week roadmap.

## Deciding with data

He measures before deciding. Examples from the case studies: two weeks of alerts classified by hand to learn the real true-positive rate before automating; a platform sized from 30 days of measured ingestion and search concurrency; SmartStore adopted only after measuring that 94% of searches hit the last 30 days.

## Managing risk and change

He changes production in stages with a way back. SOAR playbooks went live in stages (enrichment only for four weeks, then automatic closure of low-risk false positives, then automatic containment for high-confidence verdicts on non-critical assets) with an analyst approval gate for medium confidence. A SIEM migration ran in four waves with old and new platforms in parallel and event counts compared before each cut-over. Disaster recovery was proven with a timed site-loss drill. In regulated environments he works through formal change requests (RFC).

## Working with clients and stakeholders

Clear written reports, defined deliverables and no surprises, with fixed check-ins during remote work. He agrees decision rules with leadership (for example, the SOAR verdict matrix was agreed with the CISO) and presents results in walkthroughs with SOC leadership. A first conversation starts by scoping the work with concrete questions about platform version, Cloud or on-premise, daily volume and what is not working.

## The project I am most proud of

The AI-agent pipelines that migrated more than 2,000 detection rules between SIEM platforms. Each rule went through automatic quality control, metadata enrichment and mapping to MITRE ATT&CK, with an automatic assessment of coverage and obsolescence; rules that did not meet the standard were quarantined automatically instead of being migrated as they were. It combines the three things he does: SIEM engineering at scale, detection engineering and applied AI.

## Highlights

- AI-agent pipelines that migrated and validated more than 2,000 detection rules between SIEM platforms, with MITRE ATT&CK mapping.
- PresupuestAR, a SaaS he designed, built and runs in production on Google Cloud Run.
- Authorization by Splunk to teach the Power User Fast Start track in Spanish.

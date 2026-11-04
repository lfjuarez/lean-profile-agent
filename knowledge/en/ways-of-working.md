---
id: ways-of-working
title: How I work and lead
questions:
  - How do you lead a technical team?
  - How do you manage tasks, projects and deliverables?
  - How do you mentor junior engineers or transfer knowledge?
  - How do you prioritize work?
  - How do you work with clients and stakeholders?
  - How do you manage risk when changing production systems?
  - Tell me about a project you are proud of.
---

## Leading technical teams

As SIEM Architect at CyberStone (July 2020 – March 2025) I led a technical team of 2 to 4 engineers delivering scalable, clustered Splunk environments for 15 clients in banking, consumer finance, energy, gas distribution, travel assistance and media. Before that, at the Argentine Federal Police, I led the projects and sub-projects assigned to me: I gathered requirements with business owners and key users, documented the specifications and reviewed every deliverable before calling it done. I lead through clear deliverables and review of the work, not through hour counting: everyone knows what they deliver, when, and by which acceptance criteria.

## Managing tasks, projects and deliverables

I come from a PMO: at MetroGAS I monitored the SAP implementation programme with PMI methodology and good practices, built the programme dashboards and status reports with Python, Splunk and Power BI from Jira, SAP Solution Manager, Excel and MS Project data, defined KPIs and escalated status, issues and risks to the PMO director and to business and product owners on daily, weekly and monthly cycles. I scheduled and led regular and emergency meetings, recorded decisions and communicated them to teams and stakeholders. I apply that discipline to every technical project: scope and deliverables in writing from the start, tasks with an owner and a visible status, risks and issues escalated early, and decisions recorded. With my team I work in Scrum sprints: the work in Jira, documentation in Confluence or Google Docs, code and reviews in GitHub or GitLab, and Notion or Trello when the client already uses them. I adapt the cadence to the phase: a short daily sync when needed or a weekly meeting with my team, every two weeks with other teams, and more meetings and follow-up when a goal requires aligning many people. With clients I make sure they are very well informed at every stage: what the team is doing, where we stand, what is missing and what we need from them. In regulated environments every production change goes through a formal change request (RFC).

## Typical deliverables

Every engagement ends with concrete, documented deliverables: a health-check report with findings ordered by priority (each with evidence, impact and recommendation) and a roadmap; architecture documentation and runbooks, including a tested failover runbook; a MITRE ATT&CK and ATLAS coverage map with its ATT&CK Navigator layer and the detections built for each gap; SOAR playbooks with a verdict matrix agreed with the CISO; and a hand-off session with the client's team. Figures in the published case studies are synthetic; the method and the deliverables are the real ones.

## Mentoring and knowledge transfer

I close every engagement with a hand-off: documentation plus a session or workshop with the client's team, so the team understands and owns what was built. At CyberStone I designed and delivered knowledge-transfer programs with my own material, split by level (introductory and advanced). As a Splunk Certified Instructor I design the progression from basic to advanced with practical exercises and assessments so students can work on their own; across four cohorts of the Power User Fast Start track every student completed the course. In the SOAR engagement I delivered two training sessions for analysts.

## Prioritizing work

I prioritize with explicit criteria and write them down. In the detection coverage assessment, gaps were ranked by position in the attack path, relevance of the threat to the sector and effort to close. My health checks deliver findings ordered by priority, each with evidence, impact and recommendation, followed by a roadmap. The coverage work ended with a six-week roadmap.

## Deciding with data

I measure before deciding. Examples from the case studies: two weeks of alerts classified by hand to learn the real true-positive rate before automating; a platform sized from 30 days of measured ingestion and search concurrency; SmartStore adopted only after measuring that 94% of searches hit the last 30 days. In the AI-agent rule migration, every rule went through an automated test battery with coverage tracking before it counted as migrated.

## Managing risk and change

I change production in stages with a way back. SOAR playbooks went live in stages (enrichment only for four weeks, then automatic closure of low-risk false positives, then automatic containment for high-confidence verdicts on non-critical assets) with an analyst approval gate for medium confidence. A SIEM migration ran in four waves with old and new platforms in parallel and event counts compared before each cut-over. Disaster recovery was proven with a timed site-loss drill. In regulated environments I work through formal change requests (RFC) and leave evidence for PCI DSS, ISO 27001 and BCRA audits.

## Working with clients and stakeholders

Clear written reports, defined deliverables and no surprises, with fixed check-ins during remote work. I agree decision rules with leadership (for example, the SOAR verdict matrix was agreed with the CISO) and present results in walkthroughs with SOC leadership. A first conversation starts by scoping the work with concrete questions about platform version, Cloud or on-premise, daily volume and what is not working. Then I reply with how I would approach it, a scope and a quote.

## The project I am most proud of

The AI-agent pipelines that migrated more than 2,000 detection rules between SIEM platforms. Each rule went through automatic quality control, metadata enrichment and mapping to MITRE ATT&CK, with an automatic assessment of coverage and obsolescence; rules that did not meet the standard were quarantined automatically instead of being migrated as they were. It combines the three things I do: SIEM engineering at scale, detection engineering and applied AI.

## Highlights

- AI-agent pipelines that migrated and validated more than 2,000 detection rules between SIEM platforms, with MITRE ATT&CK mapping.
- Splunk projects for 15 clients in five years, the largest at around 500 GB per day, averaging more than 50 correlation searches and playbooks per client.
- Four cohorts of Splunk's official Power User Fast Start track delivered in Spanish and English, with every student completing the course.
- PresupuestAR, a SaaS I designed, built and run on Google Cloud Run, now in beta.

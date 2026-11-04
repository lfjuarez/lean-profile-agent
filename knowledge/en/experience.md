---
id: experience
title: Work experience
questions:
  - What is your current role?
  - Tell me about your Splunk consulting experience.
  - Have you worked in banking or energy?
  - What experience do you have with AI agents in production?
  - Have you built a product of your own?
  - Where do you work now?
  - What did you do at CyberStone?
---

## Senior Cloud Cybersecurity Engineer, Mercado Libre (April 2025 – present)

Full time, hybrid, Buenos Aires. I drive the architecture of Observability Security (ObSec): building AI ecosystems for cybersecurity and unifying telemetry across a massive Security Data Lake.

- Migration of multiple legacy SIEMs (more than 200 data sources) into a unified, SOCless platform on Elasticsearch, optimizing the lifecycle of petabytes of events (hot, warm, cold and frozen tiers) on AWS for scalability with cost under control.
- Design, maintenance and on-demand scaling of the ELK infrastructure, provisioned with Terraform (infrastructure as code) and managed through the global agent fleet for resilient telemetry collection (syslog, HTTP, REST API).
- Integration of a massive and diverse set of data sources across cloud, identity, network and endpoint, spanning multiple origins, environments and formats, normalized under Elastic Common Schema (ECS) to guarantee interoperability and detection fidelity.
- AI-assisted detection engineering at scale: Elastic's native MCP together with a proprietary Python MCP as a complementary layer for investigations, query validation and reusable skills that migrate and author detections under strict quality standards. Python pipelines based on AI agents that migrated more than 2,000 detection rules between SIEM platforms, with quality control, metadata enrichment and mapping to MITRE ATT&CK; rules that do not meet the standard are quarantined.
- An automated test battery (via MCP) with metadata-driven coverage tracking to guarantee detection quality and MITRE ATT&CK and ATLAS coverage across the whole ruleset.
- Full alert lifecycle, end to end: closing the loop with feedback, continuous improvement, false-positive reduction and tuning of correlation rules and UEBA; integrating detections from multiple teams into the incident-response workflow (TheHive, operated by the response team).
- Operating the SIEM across standard and PCI-scoped environments: segmented, isolated setups for sensitive multi-country banking data under strict data-separation requirements.
- Technical evidence for internal and external audits (PCI DSS, ISO 27001, BCRA, the Argentine central bank) on detection coverage, monitoring, log retention and traceability.

## Splunk Certified Instructor, Splunk (contract, January 2025 – present)

I deliver the official Power User Fast Start track for Splunk Education: public, instructor-led classes that students from any company join through Splunk's training site, in Spanish and English. Four cohorts delivered so far; every student completed the course and many went on to earn the Splunk Core Certified Power User certification. I teach the eight courses required for that certification: working with time (timestamps, time modifiers and UNIX conversions), statistical processing, comparing values with eval and conditional functions, result modification, correlation analysis with stats and transaction, knowledge objects (tags, event types, macros and workflow actions), field extractions with the Field Extractor and regular expressions, and data models for report acceleration and Pivot. I design the progression from basic to advanced with labs so students can apply what they learn on their own.

## SIEM Architect, CyberStone (contract, July 2020 – March 2025)

I led Splunk projects for 15 clients in banking, consumer finance, energy, gas distribution, travel assistance and media: new implementations, migrations from other SIEMs, re-engineering of existing deployments, and ongoing support, maintenance, continuous improvement and optimization of distributed, clustered environments (cloud, on-premise and hybrid), the largest at around 500 GB per day. I led the technical team, two to four engineers.

- Platform lifecycle and architecture: sizing, clustered indexer and search head tiers, upgrades and migrations from other SIEMs; capacity planning, performance tuning and troubleshooting.
- Security operations (SOC and SOCless): Splunk Enterprise Security with MITRE ATT&CK-mapped detections, Splunk SOAR playbooks and Splunk UBA, averaging more than 50 correlation searches and playbooks per client, with measurable reductions in false positives and triage time. Implementation of Splunk SOAR at a leading electricity distributor in Argentina.
- InfoSec data engineering: ingestion, CIM normalization, classification and enrichment of complex sources (including DB Connect); custom add-ons and advanced field extractions with regular expressions to keep data usable and licence spend under control.
- Integration and development: Splunk with external systems, cloud platforms, databases and automation tools; custom apps, dashboards and visualizations, and custom add-ons in Python.
- On-demand support during incidents: threat hunting and forensic analysis on the platform, and scripts and automations to speed up troubleshooting and investigations.
- Strategic consulting: process re-engineering, translating business requirements into Splunk solutions, and evidence for internal and external audits. At the end of each project, knowledge-transfer programs with my own material, by level.

## Project Management Officer, MetroGAS (January 2019 – July 2020)

- Designed and built project dashboards and status reports with Python, Splunk and Power BI from Jira, SAP Solution Manager, Excel and MS Project data, defining KPIs and surfacing insights for the PMO and business owners.
- Monitored the SAP implementation programme: escalated status, issues and risks to the PMO director and to business and product owners on daily, weekly and monthly cycles.
- Applied PMI methodology and good practices across the programme; scheduled and led regular and emergency meetings, recorded decisions and communicated them to project teams and stakeholders.

## Senior Business Analyst, Policía Federal Argentina (February 2011 – January 2019)

- Eight years across development, QA and business analysis on the Argentine Federal Police's internal systems: Interpol liaison, weapons registry, administrative and case-file management, and payroll.
- Developed and tested PHP applications; later led requirements with business owners and key users, documented specifications, reviewed every deliverable and acted as project leader on assigned projects and sub-projects.
- Payroll system: periodic batch loads of HR data into Oracle and development and optimization of PL/SQL stored procedures and triggers.
- Technical support in the design of complex systems in a high-security environment.

## Own product: PresupuestAR, a SaaS in beta (2026 – present)

I designed, built and operate a web SaaS, now in beta and not yet officially launched, for creating and sending professional quotes: Next.js, PostgreSQL (Prisma), Google Cloud Run with continuous deployment, PDF generation, integration with the API of ARCA (the Argentine tax authority), client signature and automatic backups. It is my proof that I build and run software end to end, not only prototypes.

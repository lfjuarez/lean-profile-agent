---
id: projects
title: Projects
questions:
  - What do you do with AI applied to cybersecurity?
  - What is mitre-coverage-kit and what is it for?
  - What is splunk-mcp-readonly?
  - What is PresupuestAR?
  - How is this site built?
  - Do you have open-source projects?
---

## Agentic AI applied to cybersecurity

The problem: migrating and maintaining thousands of detection rules between SIEM platforms by hand is slow, inconsistent and leaves dead rules that never fire. What I built, in my current role: Python pipelines based on AI agents that migrated more than 2,000 detection rules between SIEM platforms. Each rule goes through automatic quality control, metadata enrichment and mapping to MITRE ATT&CK, with an automatic assessment of coverage and obsolescence; rules that do not meet the standard are quarantined instead of being migrated as they are. Quality is guaranteed by an automated test battery (via MCP) and metadata-driven coverage tracking against MITRE ATT&CK and ATLAS. For investigations and query validation I use Elastic's native MCP plus a proprietary Python MCP with reusable skills that migrate and author detections under strict standards. I also contributed to an AI tool that finds MITRE ATT&CK and ATLAS coverage gaps and generates and tests UEBA detection rules, and I build assistants connected to Splunk, Elastic and Jira through the Model Context Protocol (MCP). The goal is always the same: agents that make detection engineering faster and more reliable, with a person reviewing what matters.

## mitre-coverage-kit (open source)

The problem: detection coverage is usually a belief ("we cover credential access") that nobody can measure. mitre-coverage-kit turns it into a measurement. It is a Python command-line tool (`coveragekit`) that reads the rules of one or several SIEMs, from exported files or straight from their APIs (Splunk Enterprise Security, Elastic Security, Wazuh, Microsoft Sentinel or Sigma), scores every MITRE ATT&CK Enterprise technique and every MITRE ATLAS technique from 0 to 3, exports an ATT&CK Navigator layer, renders a heat-map SVG and produces an HTML report with key figures, coverage by tactic and recommendations. It also lists dead rules: the ones that are enabled but can never fire because their data source is missing. It bundles ATT&CK Enterprise v20 and ATLAS v5.6 and can fetch newer releases. MIT licensed, with tests and continuous integration on every push. Code: github.com/lfjuarez/mitre-coverage-kit.

## splunk-mcp-readonly (open source)

The problem: an AI assistant that can explore Splunk is useful; one that can run `| delete` or `| outputlookup` on a typo or a prompt injection is an incident. splunk-mcp-readonly is a standalone, read-only MCP server that lets Claude Desktop, Claude Code or any MCP client query Splunk Enterprise and Splunk Cloud with nothing but a token, without installing anything on the customer's Splunk: it runs on the consultant's, auditor's or analyst's side and only needs the management port. It exposes seven read-only tools (search, SPL validation without running it, indexes, saved searches, server info, health and Enterprise Security notables) behind a guard that refuses any command that could write, delete, export or execute, forces a row cap and a default time range, applies an index allow-list and writes a JSON Lines audit log of every call. Safety is enforced twice: by the server and by a least-privilege Splunk role behind the token. About 800 lines of Python you can review in an hour, 83 offline tests, MIT licensed. Code: github.com/lfjuarez/splunk-mcp-readonly.

## Multi-site Splunk reference architecture (8 TB per day)

A published reference design for a multi-site Splunk Enterprise platform with high availability and disaster recovery, drawn to Splunk Validated Architecture patterns: data sources and collection tier, indexer cluster across two sites with replication and search factors, multi-site search head cluster, dedicated Enterprise Security cluster, cluster manager redundancy, SmartStore on object storage with cross-region replication, management plane, backups and a drilled failover runbook. Sizes are representative. The two-site platform case study on this site shows the same approach applied to a representative client, with synthetic figures and a real method.

## PresupuestAR, my own product

A side project I build for the pleasure of building: a web SaaS, in beta since 2026 and not yet officially launched, for professionals and trades to create and send professional quotes. The client receives a link, views the quote and signs it from the phone. Features: quotes with a custom-designed PDF, delivery by link with notice when the client views and signs it, client signature, client data lookup by tax id (CUIT) through the ARCA API (the Argentine tax authority), business logos and identity, item import from spreadsheets and automatic backups. It has its own mascot, Presu. Stack: Next.js, PostgreSQL with Prisma, Google Cloud Run with continuous deployment, PDF generation, ARCA API integration. It is my proof that I design, build and run software end to end, not only prototypes.

## This site

This CV is itself a project: a chat that answers only from my curated documents, with a citation to the document and section for every answer, plus a read-only MCP server that exposes the same knowledge base. How it works: the base is a set of documents in Spanish and English split into sections; a lexical search (BM25) picks the relevant sections for each question; a language model answers from those sections only and cites them; when no section is relevant, the server declines without calling the model. The answer is streamed and the page marks which sections were read and which were cited. Stack: Python with FastAPI, custom retrieval, a configurable model provider (Gemini on its free tier, or Claude), an MCP server over Streamable HTTP with six read-only tools, per-IP rate limits and a daily cap, tests and continuous integration, deployed on Google Cloud Run under the domain leandrojuarez.info. The code is open at github.com/lfjuarez/lean-profile-agent.

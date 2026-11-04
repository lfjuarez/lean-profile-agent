---
id: projects
title: Projects
questions:
  - What do you do with AI applied to cybersecurity?
  - What is PresupuestAR?
  - Do you have open-source projects?
  - How is this site built?
---

## Agentic AI applied to cybersecurity

In my current role I build Python pipelines based on AI agents that migrated more than 2,000 detection rules between SIEM platforms: each rule goes through automatic quality control, metadata enrichment and mapping to MITRE ATT&CK, with an automatic assessment of coverage and obsolescence; rules that do not meet the standard are quarantined instead of being migrated as they are. I also contributed to an AI tool that finds MITRE ATT&CK and ATLAS coverage gaps and generates and tests UEBA detection rules, and I build assistants connected to Splunk, Elastic and Jira through the Model Context Protocol (MCP). The goal is always the same: agents that make detection engineering faster and more reliable, with a person reviewing what matters.

## mitre-coverage-kit (open source)

A Python command-line tool that turns a SIEM rule inventory into per-technique scores against MITRE ATT&CK and ATLAS, an ATT&CK Navigator layer and a heat-map SVG, and lists the dead rules that can never fire. It bundles ATT&CK Enterprise v20 and ATLAS v5.6. MIT licensed, with tests and continuous integration on every push. Code: github.com/lfjuarez/mitre-coverage-kit.

## splunk-mcp-readonly (open source)

A standalone, read-only MCP server for Splunk that lets Claude or any MCP client query Splunk with nothing but a token: seven read-only tools behind an SPL guard (command blocklist, forced row caps, index allow-list) and a JSON Lines audit log of every call. Made for the cases where you cannot install apps on the customer's Splunk. 83 offline tests, MIT licensed. Code: github.com/lfjuarez/splunk-mcp-readonly.

## PresupuestAR, my own product

A side project I build for the pleasure of building: a web SaaS, in beta since 2026 and not yet officially launched, for creating and sending professional quotes. Next.js, PostgreSQL with Prisma, Google Cloud Run with continuous deployment, PDF generation, integration with the API of ARCA (the Argentine tax authority), client signature and automatic backups, with its own mascot, Presu. It is my proof that I design, build and run software end to end, not only prototypes.

## This site

This CV is itself a project: a chat that answers only from my curated documents, with a citation to the document and section for every answer, plus a read-only MCP server that exposes the same knowledge base. Lexical retrieval over sections, a language model that answers from the retrieved sections only, rate limits and a daily cap, deployed on Google Cloud Run. The code is open at github.com/lfjuarez/lean-profile-agent.

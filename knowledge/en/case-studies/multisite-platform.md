---
id: case-multisite-platform
title: "Case study: two-site Splunk platform with HA and disaster recovery"
questions:
  - Have you designed a multi-site Splunk architecture?
  - How did you test disaster recovery for a bank's SIEM?
  - What design decisions matter in a multi-site Splunk cluster?
---

## Context

Representative engagement: rebuilding a bank's SIEM as a two-site Splunk platform that survives the loss of a data center. A single-site deployment had grown from 3 to 8 TB per day with no replication, a search head that doubled as the Enterprise Security server, and a disaster-recovery plan that had never been tested. Figures are synthetic; design decisions and method are the real ones.

## The problem

Indexers ran at 85% disk with no replication, so any node failure lost data. Enterprise Security competed with ad hoc searches on one search head and skipped 20% of scheduled runs. 12,000 forwarders pointed at hard-coded indexer addresses, so adding capacity meant touching every host. Site-loss recovery was a document, not a drill.

## Approach

1. Sized from measured data: 30 days of ingestion by sourcetype, search concurrency by role, retention required versus configured.
2. Designed to Splunk Validated Architecture patterns: multi-site indexer cluster (replication factor 3, search factor 2), multi-site search head cluster, Enterprise Security on its own cluster, SmartStore with cross-region replication.
3. Forwarders moved to indexer discovery, so capacity changes never touch hosts again.
4. Migrated in four waves by index, old and new in parallel, event counts compared per sourcetype before each cut-over.
5. Wrote the failover runbook and ran it: full Site A shutdown in business hours, timed, with the SOC watching.

## Target topology

Sources (applications and LLM apps, network and security, cloud, identity and SaaS, databases, endpoints) feed a collection layer (HEC virtual IP, syslog, heavy forwarders, intermediate forwarders). Site A (primary) and Site B (DR) each run twelve indexers; a multi-site search head cluster of five members; Enterprise Security on its own cluster with a standby in Site B; cluster manager with standby; SmartStore object store replicated cross-region; deployment server, deployer and monitoring console with configuration and KV store backups.

## Results

- 0 events lost in the site-loss drill; searches continued on Site B copies.
- 22 minutes measured recovery against a 30-minute target, Enterprise Security standby included.
- Scheduled searches skipped: 20% before, 0.3% after Enterprise Security moved to its own cluster.
- 38% lower storage cost per TB with SmartStore and a 30-day cache.

## Design decisions that mattered

- Site affinity on: searches run on local copies, so daily latency does not pay for the second site.
- Site replication (origin 2, total 3) over a stretched single site: survives a site loss without manual bucket fix-up.
- Enterprise Security on its own cluster, never shared with ad hoc search.
- Cluster manager standby in Site B behind one address for peers and forwarders.
- SmartStore only after measuring the searched window: 94% of searches hit the last 30 days, so the cache is sized for that.

## Delivered

Architecture document with sizing model; build and migration runbooks; failover and fail-back runbooks, drilled; monitoring baselines; hand-over workshop.

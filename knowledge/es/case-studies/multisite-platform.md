---
id: case-multisite-platform
title: "Caso de estudio: plataforma Splunk en dos sitios con HA y recuperación ante desastres"
questions:
  - ¿Diseñaste alguna arquitectura Splunk multi-site?
  - ¿Cómo probaste la recuperación ante desastres del SIEM de un banco?
  - ¿Qué decisiones de diseño importan en un cluster Splunk multi-site?
---

## Contexto

Trabajo representativo: reconstruir el SIEM de un banco como una plataforma Splunk en dos sitios que sobrevive a la pérdida de un centro de datos. Un despliegue de un solo sitio había crecido de 3 a 8 TB por día sin replicación, con un search head que a la vez era el servidor de Enterprise Security y un plan de recuperación ante desastres que nunca se había probado. Las cifras son sintéticas; las decisiones de diseño y el método son los reales.

## El problema

Los indexers estaban al 85% de disco sin replicación, así que cualquier falla de nodo perdía datos. Enterprise Security competía con búsquedas ad hoc en un solo search head y se salteaba el 20% de las ejecuciones programadas. 12.000 forwarders apuntaban a direcciones de indexers fijas, así que agregar capacidad implicaba tocar cada host. La recuperación ante la pérdida de un sitio era un documento, no un simulacro.

## Enfoque

1. Dimensionamiento a partir de datos medidos: 30 días de ingesta por sourcetype, concurrencia de búsquedas por rol, retención requerida frente a la configurada.
2. Diseño según los patrones de Splunk Validated Architectures: cluster de indexers multi-site (replication factor 3, search factor 2), cluster de search heads multi-site, Enterprise Security en su propio cluster, SmartStore con réplica entre regiones.
3. Forwarders pasados a indexer discovery, así los cambios de capacidad nunca vuelven a tocar los hosts.
4. Migración en cuatro olas por índice, con la plataforma vieja y la nueva en paralelo, comparando conteos de eventos por sourcetype antes de cada corte.
5. Redacción del runbook de failover y ejecución real: apagado completo del Sitio A en horario laboral, cronometrado, con el SOC observando.

## Topología objetivo

Las fuentes (aplicaciones y apps LLM, red y seguridad, cloud, identidad y SaaS, bases de datos, endpoints) alimentan una capa de colección (VIP de HEC, syslog, heavy forwarders, forwarders intermedios). El Sitio A (primario) y el Sitio B (DR) tienen doce indexers cada uno; un cluster de search heads multi-site de cinco miembros; Enterprise Security en su propio cluster con standby en el Sitio B; cluster manager con standby; almacenamiento de objetos de SmartStore replicado entre regiones; deployment server, deployer y monitoring console con copias de seguridad de configuración y KV store.

## Resultados

- 0 eventos perdidos en el simulacro de pérdida de sitio; las búsquedas continuaron sobre las copias del Sitio B.
- 22 minutos de recuperación medida frente a un objetivo de 30 minutos, standby de Enterprise Security incluido.
- Búsquedas programadas salteadas: 20% antes, 0,3% después de mover Enterprise Security a su propio cluster.
- 38% menos de costo de almacenamiento por TB con SmartStore y una caché de 30 días.

## Decisiones de diseño que importaron

- Afinidad de sitio activada: las búsquedas corren sobre copias locales, así la latencia diaria no paga el costo del segundo sitio.
- Replicación por sitio (origen 2, total 3) en lugar de un solo sitio estirado: sobrevive a la pérdida de un sitio sin arreglo manual de buckets.
- Enterprise Security en su propio cluster, nunca compartido con búsquedas ad hoc.
- Standby del cluster manager en el Sitio B detrás de una sola dirección para peers y forwarders.
- SmartStore solo después de medir la ventana buscada: el 94% de las búsquedas cae en los últimos 30 días, y la caché se dimensiona para eso.

## Entregables

Documento de arquitectura con modelo de dimensionamiento; runbooks de construcción y migración; runbooks de failover y fail-back, ensayados; líneas base de monitoreo; taller de traspaso.

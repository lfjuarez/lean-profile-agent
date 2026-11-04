---
id: projects
title: Proyectos
questions:
  - ¿Qué hacés con IA aplicada a ciberseguridad?
  - ¿Qué es PresupuestAR?
  - ¿Tenés proyectos de código abierto?
  - ¿Cómo está hecho este sitio?
---

## IA agéntica aplicada a ciberseguridad

En mi rol actual construyo pipelines en Python basados en agentes de IA que migraron más de 2.000 reglas de detección entre plataformas SIEM: cada regla pasa por control de calidad automático, enriquecimiento de metadatos y mapeo a MITRE ATT&CK, con una evaluación automática de cobertura y obsolescencia; las reglas que no cumplen el estándar quedan en cuarentena en lugar de migrarse tal cual. También contribuí a una herramienta de IA que detecta huecos de cobertura MITRE ATT&CK y ATLAS y genera y prueba reglas de detección UEBA, y armo asistentes conectados a Splunk, Elastic y Jira mediante el Model Context Protocol (MCP). El objetivo es siempre el mismo: agentes que hagan la ingeniería de detección más rápida y confiable, con una persona revisando lo que importa.

## mitre-coverage-kit (código abierto)

Una herramienta de línea de comandos en Python que convierte un inventario de reglas de SIEM en puntajes por técnica contra MITRE ATT&CK y ATLAS, una capa para ATT&CK Navigator y un mapa de calor en SVG, y lista las reglas muertas que nunca podrían disparar. Incluye ATT&CK Enterprise v20 y ATLAS v5.6. Licencia MIT, con tests e integración continua en cada push. Código: github.com/lfjuarez/mitre-coverage-kit.

## splunk-mcp-readonly (código abierto)

Un servidor MCP de solo lectura para Splunk, independiente, que permite a Claude o a cualquier cliente MCP consultar Splunk con solo un token: siete herramientas de solo lectura detrás de una guarda de SPL (lista de comandos bloqueados, tope forzado de filas, lista de índices permitidos) y un registro de auditoría en JSON Lines de cada llamada. Pensado para cuando no se pueden instalar apps en el Splunk del cliente. 83 tests sin conexión, licencia MIT. Código: github.com/lfjuarez/splunk-mcp-readonly.

## PresupuestAR, mi producto propio

Un proyecto propio que desarrollo por gusto: un SaaS web, en beta desde 2026 y aún sin lanzamiento oficial, para crear y enviar presupuestos profesionales. Next.js, PostgreSQL con Prisma, Google Cloud Run con despliegue continuo, generación de PDF, integración con la API de ARCA (el organismo fiscal argentino), firma del cliente y copias de seguridad automáticas, con su propia mascota, Presu. Es mi prueba de que diseño, construyo y opero productos de software de punta a punta, no solo prototipos.

## Este sitio

Este CV es en sí mismo un proyecto: un chat que responde solo con mis documentos curados, citando documento y sección en cada respuesta, más un servidor MCP de solo lectura que expone la misma base de conocimiento. Búsqueda léxica por secciones, un modelo de lenguaje que responde únicamente con las secciones recuperadas, límites de uso y un tope diario, desplegado en Google Cloud Run. El código está abierto en github.com/lfjuarez/lean-profile-agent.

---
id: experience
title: Experiencia laboral
questions:
  - ¿Cuál es tu rol actual?
  - Contame tu experiencia como consultor Splunk.
  - ¿Trabajaste en banca o energía?
  - ¿Qué experiencia tenés con agentes de IA en producción?
  - ¿Construiste algún producto propio?
  - ¿Dónde trabajás actualmente?
  - ¿Qué hiciste en CyberStone?
---

## Senior Cloud Cybersecurity Engineer, Mercado Libre (abril de 2025 – actualidad)

Jornada completa, híbrido, Buenos Aires. Lidero la arquitectura de Observability Security (ObSec): ecosistemas de IA para ciberseguridad y telemetría unificada en un Security Data Lake masivo.

- Migración de múltiples SIEM legacy (más de 200 fuentes de datos) a una plataforma SOCless unificada sobre Elasticsearch, optimizando el ciclo de vida de petabytes de eventos (niveles hot, warm, cold y frozen) en AWS para escalar con costos bajo control.
- Diseño, mantenimiento y escalado bajo demanda de la infraestructura ELK, provisionada con Terraform (infraestructura como código) y administrada con la flota global de agentes para una recolección resiliente de telemetría (syslog, HTTP, REST API).
- Integración de un conjunto masivo de fuentes de cloud, identidad, red y endpoint, de múltiples orígenes, entornos y formatos, normalizadas bajo Elastic Common Schema (ECS) para garantizar interoperabilidad y fidelidad de detección.
- Ingeniería de detección asistida por IA a escala: el MCP nativo de Elastic más un MCP propio en Python como capa complementaria para investigaciones, validación de consultas y skills reutilizables que migran y escriben detecciones bajo estándares estrictos. Pipelines en Python basados en agentes que migraron más de 2.000 reglas de detección entre plataformas SIEM, con control de calidad, enriquecimiento de metadatos y mapeo a MITRE ATT&CK; las reglas que no cumplen el estándar quedan en cuarentena.
- Batería de tests automática (vía MCP) con seguimiento de cobertura basado en metadatos, para garantizar la calidad de las detecciones y la cobertura MITRE ATT&CK y ATLAS de todo el conjunto de reglas.
- Ciclo de vida completo de las alertas: cierre del circuito con feedback, mejora continua, reducción de falsos positivos y tuning de correlaciones y UEBA; integración de las detecciones de varios equipos en el flujo de respuesta a incidentes (TheHive, operado por el equipo de respuesta).
- Operación del SIEM en entornos estándar y con alcance PCI: entornos segmentados y aislados para datos bancarios sensibles de varios países, con requisitos estrictos de separación de datos.
- Evidencia técnica para auditorías internas y externas (PCI DSS, ISO 27001, BCRA) sobre cobertura de detección, monitoreo, retención de logs y trazabilidad.

## Instructor Certificado de Splunk, Splunk (contrato, enero de 2025 – actualidad)

Dicto el track oficial Power User Fast Start para Splunk Education: clases públicas con instructor, a las que se suman alumnos de cualquier empresa a través del sitio de formación de Splunk, en español e inglés. Cuatro cohortes dictadas hasta ahora; todos los alumnos completaron el curso y muchos obtuvieron después la certificación Splunk Core Certified Power User. Enseño los ocho cursos requeridos para esa certificación: trabajo con tiempo (timestamps, modificadores y conversiones UNIX), procesamiento estadístico, comparación de valores con eval y funciones condicionales, modificación de resultados, análisis de correlación con stats y transaction, knowledge objects (tags, event types, macros y workflow actions), extracción de campos con el Field Extractor y expresiones regulares, y data models para aceleración de reportes y Pivot. Diseño la progresión de básico a avanzado con laboratorios para que el alumno aplique lo aprendido de forma autónoma.

## SIEM Architect, CyberStone (contrato, julio de 2020 – marzo de 2025)

Lideré proyectos Splunk para 15 clientes de banca, consumo, energía, distribución de gas, asistencia al viajero y medios: implementaciones nuevas, migraciones desde otros SIEM, reingeniería de despliegues existentes y soporte, mantenimiento, mejora continua y optimización de entornos distribuidos y en cluster (cloud, on-premise e híbridos), el mayor de unos 500 GB por día. Lideré el equipo técnico, de 2 a 4 ingenieros.

- Ciclo de vida y arquitectura de la plataforma: sizing, clusters de indexers y search heads, upgrades y migraciones desde otros SIEM; capacity planning, tuning de rendimiento y troubleshooting.
- Operaciones de seguridad (SOC y SOCless): Splunk Enterprise Security con detecciones mapeadas a MITRE ATT&CK, playbooks de Splunk SOAR y Splunk UBA, con un promedio de más de 50 correlation searches y playbooks por cliente y reducciones medibles de falsos positivos y de tiempo de triage. Implementación de Splunk SOAR en una distribuidora eléctrica líder de Argentina.
- Ingeniería de datos InfoSec: ingesta, normalización CIM, clasificación y enriquecimiento de fuentes complejas (incluido DB Connect); add-ons propios y extracciones avanzadas de campos con expresiones regulares para mantener los datos usables y el gasto de licencia bajo control.
- Integración y desarrollo: Splunk con sistemas externos, plataformas cloud, bases de datos y herramientas de automatización; apps, dashboards y visualizaciones a medida, y add-ons propios en Python.
- Consultoría estratégica: reingeniería de procesos, traducción de requerimientos de negocio a soluciones Splunk y evidencia para auditorías internas y externas. Al cierre de cada proyecto, programas de transferencia de conocimiento con material propio, por nivel.

## Project Management Officer, MetroGAS (enero de 2019 – julio de 2020)

- Diseñé y construí tableros y reportes de estado con Python, Splunk y Power BI a partir de datos de Jira, SAP Solution Manager, Excel y MS Project, definiendo KPIs y mostrando insights a la PMO y a los responsables de negocio.
- Seguimiento del programa de implementación de SAP: escalado de estado, problemas y riesgos al director de la PMO y a los responsables de negocio y producto en ciclos diarios, semanales y mensuales.
- Aplicación de la metodología y las buenas prácticas del PMI en todo el programa; organización y conducción de reuniones regulares y de emergencia, registro de decisiones y comunicación a los equipos y stakeholders.

## Senior Business Analyst, Policía Federal Argentina (febrero de 2011 – enero de 2019)

- Ocho años entre desarrollo, QA y análisis de negocio en los sistemas internos de la Policía Federal Argentina: enlace con Interpol, registro de armas, gestión administrativa y de expedientes, y liquidación de haberes.
- Desarrollo y prueba de aplicaciones PHP; después, relevamiento de requerimientos con responsables de negocio y usuarios clave, documentación de especificaciones, revisión de cada entregable y liderazgo de los proyectos y subproyectos asignados.
- Sistema de haberes: cargas batch periódicas de datos de recursos humanos en Oracle y desarrollo y optimización de procedimientos almacenados y triggers en PL/SQL.
- Soporte técnico en el diseño de sistemas complejos en un entorno de alta seguridad.

## Producto propio: PresupuestAR, un SaaS en beta (2026 – actualidad)

Diseñé, desarrollé y opero un SaaS web, hoy en beta y aún sin lanzamiento oficial, para crear y enviar presupuestos profesionales: Next.js, PostgreSQL (Prisma), Google Cloud Run con despliegue continuo, generación de PDF, integración con la API de ARCA (el organismo fiscal argentino), firma del cliente y copias de seguridad automáticas. Es mi prueba de que construyo y opero software de punta a punta, no solo prototipos.

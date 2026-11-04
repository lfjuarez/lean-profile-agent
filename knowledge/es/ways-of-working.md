---
id: ways-of-working
title: Cómo trabajo y lidero
questions:
  - ¿Cómo liderás un equipo técnico?
  - ¿Cómo gestionás tareas, proyectos y entregables?
  - ¿Cómo mentoreás a perfiles junior o transferís conocimiento?
  - ¿Cómo priorizás el trabajo?
  - ¿Cómo trabajás con clientes y stakeholders?
  - ¿Cómo manejás el riesgo al cambiar sistemas en producción?
  - Contame un proyecto del que estés orgulloso.
---

## Liderazgo de equipos técnicos

Como SIEM Architect en CyberStone (julio de 2020 – marzo de 2025) lideré un equipo técnico de 2 a 4 ingenieros que entregaba entornos Splunk escalables y en cluster para 15 clientes de banca, consumo, energía, distribución de gas, asistencia al viajero y medios. Antes, en la Policía Federal Argentina, lideré los proyectos y subproyectos que me asignaban: relevaba requerimientos con los responsables de negocio y los usuarios clave, documentaba las especificaciones y revisaba cada entregable antes de darlo por terminado. Mi forma de liderar es por entregables claros y revisión del trabajo, no por control horario: cada persona sabe qué entrega, cuándo y con qué criterio se acepta.

## Gestión de tareas, proyectos y entregables

Vengo de una PMO: en MetroGAS hice el seguimiento del programa de implementación de SAP con la metodología y las buenas prácticas del PMI, construí los tableros y reportes de estado con Python, Splunk y Power BI a partir de Jira, SAP Solution Manager, Excel y MS Project, definí KPIs y escalé estado, problemas y riesgos al director de la PMO y a los responsables de negocio y producto en ciclos diarios, semanales y mensuales. Organizaba y conducía las reuniones regulares y de emergencia, registraba las decisiones y las comunicaba a los equipos y stakeholders. Esa disciplina la aplico en cada proyecto técnico: alcance y entregables por escrito desde el inicio, tareas con responsable y estado visible, riesgos y problemas escalados a tiempo, y decisiones registradas. Con mi equipo trabajo con Scrum, en sprints: el trabajo en Jira, la documentación en Confluence o Google Docs, el código y las revisiones en GitHub o GitLab, y Notion o Trello cuando el cliente ya los usa. La cadencia la adapto a la fase: una sincronización diaria cuando hace falta o una reunión semanal con mi equipo, cada quince días con otros equipos, y más reuniones y seguimiento cuando hay que llegar a un objetivo y alinear a mucha gente. Con los clientes me aseguro de que estén muy informados en cada etapa: qué está haciendo el equipo, cómo venimos, qué falta y qué necesitamos de ellos. En entornos regulados, cada cambio en producción pasa por una solicitud de cambio formal (RFC).

## Entregables típicos

Cada trabajo termina con entregables concretos y documentados: un informe de health check con hallazgos ordenados por prioridad (cada uno con evidencia, impacto y recomendación) y un roadmap; documentación de arquitectura y runbooks, incluido un runbook de failover probado; un mapa de cobertura MITRE ATT&CK y ATLAS con su capa para ATT&CK Navigator y las detecciones construidas para cada hueco; playbooks de SOAR con su matriz de veredicto acordada con el CISO; y una sesión de traspaso con el equipo del cliente. Las cifras de los casos de estudio publicados son sintéticas; el método y los entregables son los reales.

## Mentoría y transferencia de conocimiento

Cierro cada trabajo con un traspaso: documentación más una sesión o taller con el equipo del cliente, para que el equipo entienda y se apropie de lo construido. En CyberStone diseñé y dicté programas de transferencia de conocimiento con material propio, separados por nivel (introductorio y avanzado). Como Splunk Certified Instructor diseño la progresión de básico a avanzado con ejercicios prácticos y evaluaciones para que los alumnos trabajen de forma autónoma; en cuatro cohortes del track Power User Fast Start todos los alumnos completaron el curso. En el trabajo de SOAR dicté dos sesiones de capacitación para analistas.

## Cómo priorizo

Priorizo con criterios explícitos y los dejo por escrito. En la evaluación de cobertura de detección, los huecos se ordenaron por posición en la ruta de ataque, relevancia de la amenaza para el sector y esfuerzo para cerrarlos. Mis health checks entregan hallazgos ordenados por prioridad, cada uno con evidencia, impacto y recomendación, seguidos de un roadmap. El trabajo de cobertura terminó con un roadmap de seis semanas.

## Decidir con datos

Mido antes de decidir. Ejemplos de los casos de estudio: dos semanas de alertas clasificadas a mano para conocer la tasa real de verdaderos positivos antes de automatizar; una plataforma dimensionada con 30 días de ingesta y concurrencia de búsquedas medidas; SmartStore adoptado solo después de medir que el 94% de las búsquedas caía en los últimos 30 días. En la migración de reglas con agentes de IA, cada regla pasó por una batería de tests automática con seguimiento de cobertura antes de darse por migrada.

## Gestión del riesgo y del cambio

Cambio producción por etapas y con vuelta atrás. Los playbooks de SOAR entraron en producción por etapas (solo enriquecimiento durante cuatro semanas, después cierre automático de falsos positivos de bajo riesgo, después contención automática para veredictos de alta confianza en activos no críticos) con una compuerta de aprobación del analista para confianza media. Una migración de SIEM se hizo en cuatro olas con la plataforma vieja y la nueva en paralelo, comparando conteos de eventos antes de cada corte. La recuperación ante desastres se probó con un simulacro cronometrado de pérdida de sitio. En entornos regulados trabajo con solicitudes de cambio formales (RFC) y dejo evidencia para auditorías PCI DSS, ISO 27001 y BCRA.

## Trabajo con clientes y stakeholders

Informes escritos claros, entregables definidos y sin sorpresas, con reuniones de seguimiento fijas en el trabajo remoto. Acuerdo las reglas de decisión con la dirección (por ejemplo, la matriz de veredicto de SOAR se acordó con el CISO) y presento resultados en sesiones con la dirección del SOC. Una primera conversación empieza con preguntas concretas de alcance: versión de la plataforma, Cloud u on-premise, volumen diario y qué no está funcionando. Después respondo con cómo lo encararía, un alcance y una cotización.

## El proyecto del que más me enorgullezco

Los pipelines con agentes de IA que migraron más de 2.000 reglas de detección entre plataformas SIEM. Cada regla pasó por control de calidad automático, enriquecimiento de metadatos y mapeo a MITRE ATT&CK, con una evaluación automática de cobertura y obsolescencia; las reglas que no cumplían el estándar quedaron en cuarentena automática en lugar de migrarse tal cual. Combina las tres cosas que hago: ingeniería de SIEM a gran escala, ingeniería de detección e IA aplicada.

## Logros destacados

- Pipelines con agentes de IA que migraron y validaron más de 2.000 reglas de detección entre plataformas SIEM, con mapeo a MITRE ATT&CK.
- Proyectos Splunk para 15 clientes en cinco años, el mayor de unos 500 GB por día, con más de 50 correlation searches y playbooks por cliente en promedio.
- Cuatro cohortes del track oficial Power User Fast Start de Splunk dictadas en español e inglés, con todos los alumnos completando el curso.
- PresupuestAR, un SaaS que diseñé, desarrollé y opero en Google Cloud Run, hoy en beta.

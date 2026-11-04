---
id: ways-of-working
title: Cómo trabajo y lidero
questions:
  - ¿Cómo liderás un equipo técnico?
  - ¿Cómo mentoreás a perfiles junior o transferís conocimiento?
  - ¿Cómo priorizás el trabajo?
  - ¿Cómo trabajás con clientes y stakeholders?
  - ¿Cómo manejás el riesgo al cambiar sistemas en producción?
  - Contame un proyecto del que estés orgulloso.
---

## Liderazgo de equipos técnicos

Como Technical Leader Splunk en una consultora (julio de 2020 – marzo de 2025), Leandro lideró un equipo técnico de 2 a 4 ingenieros que entregaba entornos Splunk escalables y en cluster para clientes de banca, finanzas, energía y seguros.

## Mentoría y transferencia de conocimiento

Cierra cada trabajo con un traspaso: documentación más una sesión o taller con el equipo del cliente, para que el equipo entienda y se apropie de lo construido. En ese rol de consultoría diseñó y dictó programas de transferencia de conocimiento con material propio, separados por nivel (introductorio y avanzado). Como Splunk Certified Instructor diseña la progresión de básico a avanzado con ejercicios prácticos y evaluaciones para que los alumnos trabajen de forma autónoma. En el trabajo de SOAR dictó dos sesiones de capacitación para analistas.

## Cómo prioriza

Prioriza con criterios explícitos y los deja por escrito. En la evaluación de cobertura de detección, los huecos se ordenaron por posición en la ruta de ataque, relevancia de la amenaza para el sector y esfuerzo para cerrarlos. Sus health checks entregan hallazgos ordenados por prioridad, cada uno con evidencia, impacto y recomendación, seguidos de un roadmap. El trabajo de cobertura terminó con un roadmap de seis semanas.

## Decidir con datos

Mide antes de decidir. Ejemplos de los casos de estudio: dos semanas de alertas clasificadas a mano para conocer la tasa real de verdaderos positivos antes de automatizar; una plataforma dimensionada con 30 días de ingesta y concurrencia de búsquedas medidas; SmartStore adoptado solo después de medir que el 94% de las búsquedas caía en los últimos 30 días.

## Gestión del riesgo y del cambio

Cambia producción por etapas y con vuelta atrás. Los playbooks de SOAR entraron en producción por etapas (solo enriquecimiento durante cuatro semanas, después cierre automático de falsos positivos de bajo riesgo, después contención automática para veredictos de alta confianza en activos no críticos) con una compuerta de aprobación del analista para confianza media. Una migración de SIEM se hizo en cuatro olas con la plataforma vieja y la nueva en paralelo, comparando conteos de eventos antes de cada corte. La recuperación ante desastres se probó con un simulacro cronometrado de pérdida de sitio. En entornos regulados trabaja con solicitudes de cambio formales (RFC).

## Trabajo con clientes y stakeholders

Informes escritos claros, entregables definidos y sin sorpresas, con reuniones de seguimiento fijas en el trabajo remoto. Acuerda las reglas de decisión con la dirección (por ejemplo, la matriz de veredicto de SOAR se acordó con el CISO) y presenta resultados en sesiones con la dirección del SOC. Una primera conversación empieza con preguntas concretas de alcance: versión de la plataforma, Cloud u on-premise, volumen diario y qué no está funcionando.

## El proyecto del que más me enorgullezco

Los pipelines con agentes de IA que migraron más de 2.000 reglas de detección entre plataformas SIEM. Cada regla pasó por control de calidad automático, enriquecimiento de metadatos y mapeo a MITRE ATT&CK, con una evaluación automática de cobertura y obsolescencia; las reglas que no cumplían el estándar quedaron en cuarentena automática en lugar de migrarse tal cual. Combina las tres cosas que hace: ingeniería de SIEM a gran escala, ingeniería de detección e IA aplicada.

## Logros destacados

- Pipelines con agentes de IA que migraron y validaron más de 2.000 reglas de detección entre plataformas SIEM, con mapeo a MITRE ATT&CK.
- PresupuestAR, un SaaS que diseñó, desarrolló y opera en producción en Google Cloud Run.
- Habilitación de Splunk para dictar el track Power User Fast Start en español.

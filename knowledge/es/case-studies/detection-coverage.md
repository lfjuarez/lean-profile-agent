---
id: case-detection-coverage
title: "Caso de estudio: evaluación de cobertura de detección contra MITRE ATT&CK y ATLAS"
questions:
  - ¿Cómo medís la cobertura de detección contra MITRE ATT&CK?
  - ¿Qué entregó la evaluación de cobertura de detección?
  - ¿Cubrís MITRE ATLAS y la seguridad de aplicaciones de IA?
---

## Contexto

Trabajo representativo para el SOC de un banco regional. El SOC creía que sus 312 reglas de Splunk Enterprise Security cubrían "la mayor parte" de ATT&CK; nadie podía decir qué técnicas, con qué calidad, ni qué lograría un operador de ransomware sin ser detectado. Las cifras son sintéticas; el método y los entregables son los reales. La evaluación abarcó ATT&CK Enterprise v20 (259 técnicas) puntuadas por calidad de detección, y MITRE ATLAS para las dos aplicaciones LLM del banco orientadas a clientes.

## El problema

La cobertura era una creencia, no una medición. Las reglas se habían acumulado durante seis años de tres proveedores y dos migraciones de SIEM; 41 dependían de datos que ya no se recolectaban. Las dos aplicaciones LLM orientadas a clientes no tenían telemetría de seguridad.

## Enfoque

1. Exportación de cada correlation search y regla de EDR habilitada con su SPL y metadatos.
2. Mapeo de cada regla a ATT&CK y ATLAS con un pipeline asistido por IA; cada mapeo revisado a mano.
3. Prueba de cada regla contra los datos realmente recolectados; cada técnica puntuada como ninguna, baja, media o alta.
4. Priorización de los huecos por posición en la ruta de ataque, relevancia de amenazas del sector y esfuerzo para cerrarlos.

## Resultados

- Técnicas de ATT&CK cubiertas: 48% antes, 58% después de la primera ola.
- Cobertura de ATLAS (IA y LLM): 15% antes, 35% una vez que la telemetría de prompts y de llamadas a herramientas llegó al SIEM.
- 41 reglas retiradas o reparadas que nunca podrían haber disparado.
- La cobertura por táctica fue de 11% (Resource Development) a 82% (Execution); las áreas más débiles fueron Exfiltration (20%), Collection (29%) y Reconnaissance (33%).

## Principales huecos y la detección construida para cada uno

- T1486 Data Encrypted for Impact (crítico): ráfaga de renombrados a extensiones desconocidas por host (EDR / evento 11 de Sysmon).
- T1021 Remote Services (crítico): primeros inicios de sesión de administrador entre servidores (evento 4624 de Windows, tipos de logon 3 y 10).
- AML.T0051 LLM Prompt Injection (crítico): patrones de inyección y veredictos del guardrail por sesión, desde logs de prompts enviados por HEC.
- T1110 Brute Force (serio): muchos fallos seguidos de un éxito, por origen y usuario, sobre el data model Authentication.

## Entregables

Mapas de calor puntuados para ATT&CK y ATLAS; archivo de capa para ATT&CK Navigator; inventario de reglas con mapeo, estado y responsable; SPL de cada detección propuesta; roadmap de seis semanas y una presentación con la dirección del SOC.

---
id: case-soar-triage
title: "Caso de estudio: automatización del triage de phishing y malware con Splunk SOAR"
questions:
  - ¿Cómo automatizaste el triage de alertas con Splunk SOAR?
  - ¿Qué resultados logró la automatización con SOAR a los 90 días?
  - ¿Cómo mantenés a los analistas en control de la contención automática?
---

## Contexto

Trabajo representativo, basado en el trabajo con SOAR en el sector energético. Un SOC de seis personas recibía unas 1.900 alertas de phishing y malware por mes y hacía el triage de cada una a mano en seis consolas. Las cifras son sintéticas; el diseño del playbook, el modelo de aprobación y las métricas son el método real.

## El problema

El tiempo medio de triage era de 42 minutos y la cola se acumulaba cada lunes. Los analistas repetían las mismas consultas (reputación del hash, historial del remitente, dueño del host, privilegios del usuario) para cada alerta, y las acciones de contención vivían en cuatro consolas distintas con cuatro juegos de credenciales. Nadie podía informar cuántas alertas eran verdaderos positivos.

## Enfoque

1. Medir primero: dos semanas de alertas clasificadas a mano para obtener la tasa real de verdaderos positivos (11%) y las consultas que los analistas hacían de verdad.
2. Construcción de las integraciones como assets reutilizables de SOAR (EDR, gateway de correo, Active Directory, firewall, tickets, sandbox) con cuentas de servicio de mínimo privilegio y acciones probadas.
3. Escritura de los playbooks por etapas: solo enriquecimiento durante cuatro semanas (los analistas seguían decidiendo), después cierre automático de falsos positivos de bajo riesgo, después contención automática para veredictos de alta confianza en activos no críticos.
4. Cada acción automática escribe su evidencia en el notable de Enterprise Security y en el ticket, así la auditoría nunca depende solo de SOAR.

## Estructura del playbook

Tres disparadores (notable de Enterprise Security con risk score de 60 o más, reporte del usuario mediante un botón de reportar phishing, detección del EDR) se normalizan en un único esquema de contenedor (hash, URL, remitente, host, usuario). Una etapa de enriquecimiento (VirusTotal, sandbox de URL, contexto de usuario y host en Active Directory, criticidad del activo, casos previos). Una matriz de veredicto de confianza por criticidad del activo con compuerta del analista para confianza media. Contención (aislar host, bloquear remitente y URL, restablecer credenciales y revocar sesiones). Ticket y cierre (incidente en ServiceNow con evidencia, notable actualizado, métricas a Splunk).

## Matriz de veredicto en producción

- Confianza alta (dos fuentes independientes coinciden): activo no crítico contenido automáticamente con notificación; activo crítico espera en la compuerta del analista con un tiempo de espera de 15 minutos que escala.
- Confianza media: compuerta del analista con la evidencia recolectada; para activos críticos se llama al analista de guardia.
- Baja o benigno conocido: cierre con evidencia; para activos críticos, revisión semanal de una muestra.

## Resultados a los 90 días

- Tiempo medio de triage: 42 minutos antes, 6 minutos después.
- 78% de las alertas enriquecidas y cerradas o contenidas sin que un analista toque una consola.
- 14 playbooks en producción, 6 integraciones, 31 acciones probadas.
- 0 acciones de contención revertidas por erróneas en 90 días; dos retenidas en la compuerta del analista.

## Entregables

Playbooks y funciones propias en control de versiones; assets de integración y runbooks; matriz de veredicto acordada con el CISO; dashboard de métricas del SOC en Splunk (volumen, tiempo de triage, tasa de automatización, decisiones de la compuerta); dos sesiones de capacitación para analistas.

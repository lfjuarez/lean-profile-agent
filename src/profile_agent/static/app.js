(() => {
  "use strict";

  const I18N = {
    en: {
      "nav.skip": "Skip to the question box", "nav.profile": "Profile", "nav.ask": "Ask", "nav.exp": "Experience", "nav.edu": "Education", "nav.skills": "Skills", "nav.projects": "Projects", "nav.mcp": "MCP",
      "topics.more": "More topics", "topics.less": "Fewer topics", "fab.ask": "Ask",
      "more.exp": "Show the 2 earlier roles", "less.exp": "Show fewer roles", "more.edu": "Show 3 more degrees", "less.edu": "Show fewer degrees",
      "more.skills": "Show 4 more areas", "less.skills": "Show fewer areas", "more.proj": "Show 3 more projects", "less.proj": "Show fewer projects",
      "hero.alt": "Portrait of Leandro F. Juárez",
      "hero.role": "Cybersecurity engineer and SIEM architect",
      "hero.roleSub": "Detection engineering · AI for security operations · Elastic and Splunk · Consulting and training",
      "hero.statement": "I help security teams get real value from their SIEM: platforms that scale, detections that fire on real threats, and people who know how to use them.",
      "certs.instructor": "Splunk Certified Instructor", "certs.note": "· Power User Fast Start, authorized by Splunk",
      "creds.master": "Master's in Data Science", "creds.cloud": "Cloud: AWS, Azure and Google Cloud",
      "hero.cv": "View my CV", "hero.cvAlt": "CV en español", "proj.detail": "Details and links",
      "contact.email": "Email", "contact.copy": "Copy", "contact.copied": "Copied", "contact.where": "Based in", "contact.whereV": "Buenos Aires, Argentina · remote",
      "aud.title": "Pick your role so the answers fit you",
      "aud.tech": "Technical", "aud.biz": "Sales", "aud.people": "HR and People",
      "aud.techText": "Ask about SIEM architectures, MITRE ATT&CK detections, SOAR or AI applied to security. Every answer cites the exact section of my documents, and you can connect this same CV to your Claude or ChatGPT through MCP.",
      "aud.bizText": "If you are evaluating a consultant for a SIEM, detection or Splunk training project, ask about services, rates, availability and case studies. Answers come from my documents and the CV downloads in one click.",
      "aud.peopleText": "If you are screening candidates or preparing an interview, ask about my track record, how I work, team leadership and project references. I answer in the first person, with the source next to it.",
      "aud.note": "I answer in the first person, but the one replying is an AI assistant that uses only my documents and cites the source. If something is not documented, it says so.",
      "ask.label": "Ask me about my professional experience", "ask.placeholder": "Type your question…", "ask.send": "Ask",
      "answer.empty": "Answers come only from my documented experience, with sources. Each one marks, further down, the roles, studies, skills and topics it read and the ones it cites.",
      "exp.title": "Professional experience", "exp.sub": "You can ask about any role. After each answer, the ones I read and the ones I cited are marked.",
      "exp.ask": "Ask about this role",
      "exp.meli.when": "Apr 2025 – present",
      "exp.meli.b1": "I drive the architecture of Observability Security: AI ecosystems for cybersecurity and unified telemetry in a Security Data Lake.",
      "exp.meli.b2": "Migration of several legacy SIEMs into a SOCless platform on Elasticsearch over AWS, with the lifecycle of petabytes of events; infrastructure with Terraform and 200+ sources normalized in ECS.",
      "exp.meli.b3": "AI-assisted detection engineering through MCP: 2,000+ rules migrated with quality control and measured MITRE ATT&CK and ATLAS coverage; evidence for PCI DSS, ISO 27001 and BCRA audits.",
      "exp.meli.ask": "Tell me about your current role at Mercado Libre.",
      "exp.splunk.when": "Jan 2025 – present",
      "exp.splunk.b1": "I deliver the official Power User Fast Start track for Splunk Education, in Spanish and English, to students from any company.",
      "exp.splunk.b2": "Four cohorts delivered: every student completed the course and many earned the Splunk Core Certified Power User certification.",
      "exp.splunk.ask": "Tell me about your work as a Splunk Certified Instructor.",
      "exp.cyber.when": "Jul 2020 – Mar 2025",
      "exp.cyber.b1": "Splunk projects for 15 clients in banking, consumer finance, energy, gas, travel assistance and media, the largest at 500 GB per day; I led a technical team of 2 to 4 engineers.",
      "exp.cyber.b2": "Enterprise Security with MITRE ATT&CK detections, SOAR playbooks and UBA: 50+ correlation searches and playbooks per client, with fewer false positives and less triage time.",
      "exp.cyber.b3": "Migrations from other SIEMs, multi-site clusters, CIM normalization, custom integrations and audit evidence.",
      "exp.cyber.ask": "Tell me about your time as SIEM Architect at CyberStone.",
      "exp.metrogas.when": "Jan 2019 – Jul 2020",
      "exp.metrogas.b1": "Dashboards and reports with Python, Splunk and Power BI from Jira, SAP Solution Manager and MS Project for the SAP implementation programme.",
      "exp.metrogas.b2": "Status, issue and risk tracking with PMI methodology, on daily, weekly and monthly cycles.",
      "exp.metrogas.ask": "What did you do at MetroGAS?",
      "exp.pfa.when": "Feb 2011 – Jan 2019",
      "exp.pfa.b1": "Eight years across development, QA and business analysis on critical systems: Interpol liaison, weapons registry, case files and payroll.",
      "exp.pfa.b2": "PHP applications, Oracle and PL/SQL; requirements with key users and leadership of assigned projects in a high-security environment.",
      "exp.pfa.ask": "What did you do at the Argentine Federal Police?",
      "exp.presu.when": "2026 – present", "exp.presu.org": "· my own product",
      "exp.presu.b1": "A SaaS in beta, not yet officially launched, for creating and sending professional quotes: Next.js, PostgreSQL, Google Cloud Run, PDF, client signature and the ARCA API.",
      "exp.presu.ask": "What is PresupuestAR?",
      "edu.title": "Education",
      "edu.caece.t": "Master's in Data Science and Business Innovation", "edu.caece.n": "Grade average 9.15/10. Thesis: predicting musical success on streaming platforms with NLP and machine learning.",
      "edu.palermo.t": "Bachelor's in Information Technology", "edu.palermo.n": "Final project: a SaaS platform for tele-diagnosis of diabetic retinopathy with machine learning.",
      "edu.esba.t": "Advanced Technician in Systems Analysis",
      "edu.iupfa.t": "Advanced Technician in Telecommunications", "edu.iupfa.n": "Grade average 8.66/10.",
      "edu.cema.t": "Applied Artificial Intelligence", "edu.cema.n": "Model training in Python.",
      "edu.langs": "Languages: native Spanish · English, full professional proficiency.",
      "sk.title": "Skills",
      "sk.1.t": "SIEM platforms", "sk.1.d": "Elastic (Elasticsearch, Kibana, Fleet, ECS) and Splunk (multi-site clusters, Splunk Cloud, SmartStore, Enterprise Security, SOAR, UBA, CIM).",
      "sk.2.t": "Data and normalization", "sk.2.d": "Source onboarding (Universal Forwarder, HEC, syslog, DB Connect, REST), CIM and ECS, hot-warm-cold-frozen lifecycle, data quality.",
      "sk.3.t": "Detection and response", "sk.3.d": "MITRE ATT&CK and ATLAS, detection engineering, UEBA, SOAR playbooks, threat hunting, triage and investigation, false-positive reduction.",
      "sk.4.t": "AI for security", "sk.4.d": "LLM agents, RAG, custom MCP servers, output evaluation and guardrails; Python, TypeScript, SQL.",
      "sk.5.t": "Cloud and infrastructure", "sk.5.d": "AWS, Azure and Google Cloud (Cloud Run), Terraform, Linux and Windows Server, networking.",
      "sk.6.t": "Data science and reporting", "sk.6.d": "Machine learning and NLP, pandas, applied statistics, Power BI, Splunk and Kibana dashboards, ETL.",
      "sk.7.t": "Compliance and audit", "sk.7.d": "PCI DSS, ISO 27001 and BCRA; technical evidence and change management in regulated environments.",
      "sk.8.t": "Leadership and training", "sk.8.d": "Technical teams of 2 to 4 engineers, Scrum and Jira, PMO and PMI methodology, official Splunk instructor in Spanish and English, knowledge transfer.",
      "proj.title": "Projects",
      "proj.aiT": "Agentic AI for cybersecurity",
      "proj.ai": "In my current role: Python pipelines with AI agents that migrated 2,000+ detection rules between SIEMs, with quality control and MITRE ATT&CK mapping; a tool that measures ATT&CK and ATLAS coverage, and assistants connected to Splunk, Elastic and Jira through MCP.",
      "proj.aiAlt": "Detection rules in Elastic Security",
      "proj.cov": "Open source: it turns detection coverage into a measurement. It reads rules from Splunk ES, Elastic Security, Wazuh, Sentinel or Sigma, scores every MITRE ATT&CK and ATLAS technique, lists dead rules and suggests public rules (SigmaHQ) for the gaps. A web app with matrices, a panel per technique, history and export to PDF, Excel and Navigator. Something similar, at massive scale, I implemented at very large companies with SIEMs from different vendors and environments. MIT, with tests and CI.",
      "proj.covAlt": "The mitre-coverage-kit ATT&CK matrix with the coverage traffic light",
      "proj.mcp": "Open source: a standalone, read-only MCP server to query Splunk from Claude or any MCP client with nothing but a token. Seven tools behind an SPL guard (blocked commands, row caps, index allow-list) and an audit log of every call. 83 tests, MIT.",
      "proj.mcpAlt": "The seven read-only tools of splunk-mcp-readonly and its SPL guard",
      "proj.archT": "Multi-site Splunk architecture",
      "proj.arch": "Reference design for a two-site Splunk Enterprise platform with high availability and disaster recovery, drawn to Splunk Validated Architectures: multi-site indexer and search head clusters, a dedicated Enterprise Security cluster, SmartStore with cross-region replication and a drilled failover runbook.",
      "proj.archAlt": "Diagram of the multi-site Splunk reference architecture",
      "proj.presu": "My own product, built for the pleasure of building: a web SaaS in beta, not yet officially launched, for creating and sending professional quotes. Next.js, PostgreSQL, Google Cloud Run and the ARCA API.",
      "proj.presuAlt": "Presu, the PresupuestAR mascot, in a frame of the showreel",
      "proj.siteT": "This CV",
      "proj.site": "Open source: a chat that answers only from my documents and cites every source, plus an MCP server on the same base. It is the sample of how I work with AI.",
      "proj.siteAlt": "Screenshot of this site: the question box and an answer with its sources",
      "facts.title": "In numbers", "facts.it": "years in IT", "facts.clients": "SIEM clients in banking, energy and media",
      "facts.rules": "detection rules migrated with AI agents", "facts.rulesN": "2,000+", "facts.sources": "data sources in one security data lake",
      "err.generic": "Something went wrong. Try again.", "err.rate": "Too many questions in a short time. Wait a minute.",
      "err.daily": "The daily question limit for this demo was reached. Come back tomorrow or write to Leandro.",
      "mcp.title": "Ask it from your own AI too", "mcp.howto": "How to connect it", "mcp.tools": "Six read-only tools:",
      "mcp.intro": "This CV is also a read-only MCP server. Add the URL to Claude, ChatGPT or any MCP client and question it from your own assistant, with the same sources.",
      "mcp.copy": "Copy URL", "mcp.copied": "Copied",
      "mcp.desktop": "Settings, Connectors, Add custom connector, then paste the URL. Or add it to claude_desktop_config.json:",
      "mcp.chatgpt": "Settings, Connectors, Advanced, Developer mode, Create. Paste the URL as the MCP server URL, with no authentication.",
      "how.title": "How it works",
      "how.s1t": "Curated documents", "how.s1": "Twelve documents in Spanish and English. Every section you see marked on this page is one section of them, and nothing else is used.",
      "how.s2t": "Search first, then the model", "how.s2": "Each question selects the relevant sections. The model answers only from them and cites them; with nothing relevant, the server declines without calling it.",
      "how.s3t": "Sources you can see", "how.s3": "Read sections turn dark blue and cited ones light blue. Case study figures are synthetic; method and deliverables are real.",
      "how.s4t": "Limits, honestly", "how.s4": "The wording can still be imperfect, so every answer shows its sources and the CV is one click away. It does not replace a conversation.",
      "foot.synthetic": "Case study figures are synthetic; method and deliverables are real."
    },
    es: {
      "nav.skip": "Ir a la caja de preguntas", "nav.profile": "Perfil", "nav.ask": "Preguntar", "nav.exp": "Experiencia", "nav.edu": "Formación", "nav.skills": "Competencias", "nav.projects": "Proyectos", "nav.mcp": "MCP",
      "topics.more": "Más temas", "topics.less": "Menos temas", "fab.ask": "Preguntar",
      "more.exp": "Ver las 2 etapas anteriores", "less.exp": "Ver menos etapas", "more.edu": "Ver 3 títulos más", "less.edu": "Ver menos títulos",
      "more.skills": "Ver 4 áreas más", "less.skills": "Ver menos áreas", "more.proj": "Ver 3 proyectos más", "less.proj": "Ver menos proyectos",
      "hero.alt": "Retrato de Leandro F. Juárez",
      "hero.role": "Ingeniero de ciberseguridad y arquitecto de SIEM",
      "hero.roleSub": "Ingeniería de detección · IA aplicada a operaciones de seguridad · Elastic y Splunk · Consultoría y formación",
      "hero.statement": "Ayudo a equipos de seguridad a aprovechar al máximo su SIEM: plataformas que escalan, detecciones que disparan con amenazas reales y gente que sabe usarlas.",
      "certs.instructor": "Splunk Certified Instructor", "certs.note": "· Power User Fast Start, habilitado por Splunk",
      "creds.master": "Magíster en Ciencia de Datos", "creds.cloud": "Cloud: AWS, Azure y Google Cloud",
      "hero.cv": "Ver mi CV", "hero.cvAlt": "CV in English", "proj.detail": "Ver detalles y enlaces",
      "contact.email": "Email", "contact.copy": "Copiar", "contact.copied": "Copiado", "contact.where": "Ubicación", "contact.whereV": "Buenos Aires, Argentina · remoto",
      "aud.title": "Elegí tu perfil para que te responda mejor",
      "aud.tech": "Técnico", "aud.biz": "Comercial", "aud.people": "RR. HH. y People",
      "aud.techText": "Preguntá por arquitecturas de SIEM, detecciones MITRE ATT&CK, SOAR o IA aplicada a seguridad. Cada respuesta cita la sección exacta de mis documentos, y podés conectar este mismo CV a tu Claude o ChatGPT por MCP.",
      "aud.bizText": "Si evaluás un consultor para un proyecto de SIEM, detección o formación Splunk, preguntá por servicios, tarifas, disponibilidad y casos de estudio. Las respuestas salen de mis documentos y el CV se descarga en un clic.",
      "aud.peopleText": "Si estás evaluando candidatos o preparando una entrevista, preguntá por trayectoria, forma de trabajar, liderazgo de equipo y referencias de proyectos. Respondo en primera persona, con la fuente al lado.",
      "aud.note": "Respondo en primera persona, pero quien contesta es un asistente de IA que usa solo mis documentos y cita la fuente. Si algo no está documentado, lo dice.",
      "ask.label": "Preguntame sobre mi experiencia profesional", "ask.placeholder": "Escribí tu pregunta…", "ask.send": "Preguntar",
      "answer.empty": "Las respuestas salen solo de mi experiencia documentada, con fuentes. Cada una marca más abajo las etapas, estudios, competencias y temas que leyó y los que cita.",
      "exp.ask": "Preguntar por esta etapa",
      "exp.meli.ask": "Contame sobre tu rol actual en Mercado Libre.",
      "exp.splunk.ask": "Contame sobre tu trabajo como instructor certificado de Splunk.",
      "exp.cyber.ask": "Contame sobre tu etapa como SIEM Architect en CyberStone.",
      "exp.metrogas.ask": "¿Qué hiciste en MetroGAS?",
      "exp.pfa.ask": "¿Qué hiciste en la Policía Federal Argentina?",
      "exp.presu.ask": "¿Qué es PresupuestAR?",
      "facts.title": "En números", "facts.it": "años en IT", "facts.clients": "clientes de SIEM en banca, energía y medios",
      "facts.rules": "reglas de detección migradas con agentes de IA", "facts.rulesN": "2.000+", "facts.sources": "fuentes de datos en un data lake de seguridad",
      "err.generic": "Algo salió mal. Probá de nuevo.", "err.rate": "Demasiadas preguntas en poco tiempo. Esperá un minuto.",
      "err.daily": "Se alcanzó el límite diario de preguntas de esta demo. Volvé mañana o escribile a Leandro.",
      "mcp.title": "Preguntale también desde tu propia IA", "mcp.howto": "Cómo conectarlo", "mcp.tools": "Seis herramientas de solo lectura:",
      "mcp.intro": "Este CV también es un servidor MCP de solo lectura. Sumá la URL a Claude, ChatGPT o cualquier cliente MCP y preguntale desde tu propio asistente, con las mismas fuentes.",
      "mcp.copy": "Copiar URL", "mcp.copied": "Copiado",
      "mcp.desktop": "Configuración, Conectores, Agregar conector personalizado, y pegá la URL. O agregalo a claude_desktop_config.json:",
      "mcp.chatgpt": "Configuración, Conectores, Avanzado, Modo desarrollador, Crear. Pegá la URL como URL del servidor MCP, sin autenticación.",
      "how.title": "Cómo funciona",
      "how.s1t": "Documentos curados", "how.s1": "Doce documentos en español e inglés. Cada sección que ves marcada en esta página es una sección de ellos, y no se usa nada más.",
      "how.s2t": "Primero búsqueda, después el modelo", "how.s2": "Cada pregunta elige las secciones relevantes. El modelo responde solo con ellas y las cita; si no hay nada relevante, el servidor declina sin llamarlo.",
      "how.s3t": "Fuentes a la vista", "how.s3": "Las secciones leídas se pintan azul oscuro y las citadas azul claro. Las cifras de los casos de estudio son sintéticas; el método y los entregables son reales.",
      "how.s4t": "Límites, con honestidad", "how.s4": "La redacción todavía puede ser imperfecta; por eso cada respuesta muestra sus fuentes y el CV está a un clic. No reemplaza una conversación.",
      "foot.synthetic": "Las cifras de los casos de estudio son sintéticas; el método y los entregables son reales."
    }
  };

  const $ = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => Array.from(r.querySelectorAll(s));
  const reduced = matchMedia("(prefers-reduced-motion: reduce)").matches;
  const state = { lang: "es", aud: "tech", history: [], busy: false, topics: [], topic: null };
  const ORIG = new Map(); // Spanish text written in the HTML, for keys the dictionary does not carry
  const t = (k, vars) => {
    let s = (I18N[state.lang] && I18N[state.lang][k]) || I18N.es[k] || k;
    if (vars) for (const [a, b] of Object.entries(vars)) s = s.replace(`{${a}}`, b);
    return s;
  };

  function applyLanguage(lang) {
    state.lang = lang === "en" ? "en" : "es";
    document.documentElement.lang = state.lang;
    try { localStorage.setItem("lang", state.lang); } catch (_) {}
    $$("[data-i18n]").forEach((el) => {
      const k = el.dataset.i18n;
      const v = I18N[state.lang][k];
      if (v !== undefined) el.textContent = v;
      else if (ORIG.has(el)) el.textContent = ORIG.get(el);
    });
    $$("[data-i18n-placeholder]").forEach((el) => {
      const v = I18N[state.lang][el.dataset.i18nPlaceholder];
      el.placeholder = v !== undefined ? v : el.dataset.origPlaceholder || el.placeholder;
    });
    $$("[data-i18n-alt]").forEach((el) => {
      const v = I18N[state.lang][el.dataset.i18nAlt];
      el.alt = v !== undefined ? v : el.dataset.origAlt || el.alt;
    });
    $$(".lang button").forEach((b) => b.setAttribute("aria-pressed", String(b.dataset.lang === state.lang)));
    const activeLink = $(".bar-nav a.active") || $(".bar-nav a");
    if (activeLink) $("#nav-current").textContent = activeLink.textContent;
    const main = state.lang === "es" ? "ES" : "EN", alt = state.lang === "es" ? "EN" : "ES";
    $("#cv-link").href = `/cv?lang=${main.toLowerCase()}`;
    $("#cv-alt").href = `/cv?lang=${alt.toLowerCase()}`;
    $$(".proj-detail").forEach((a) => { a.href = `/projects?lang=${state.lang}#${a.dataset.anchor}`; });
    setAudience(state.aud, false);
    state.history = [];
    $("#answer-full").hidden = true;
    $("#answer-empty").hidden = false;
    resetLights();
    $$("[data-list]").forEach((l) => openList(l, false));
    loadTopics();
    loadChips();
  }

  function setAudience(aud, animate) {
    state.aud = aud;
    $$(".aud-tabs [role=tab]").forEach((b) => b.setAttribute("aria-selected", String(b.dataset.aud === aud)));
    const p = $("#aud-text");
    p.textContent = t(`aud.${aud}Text`);
    if (animate && !reduced) { p.classList.remove("swap"); void p.offsetWidth; p.classList.add("swap"); }
    if (animate) loadChips();
  }

  async function loadChips() {
    const box = $("#chips");
    box.innerHTML = "";
    state.topic = null;
    state.topics.forEach((tp) => tp.btn.setAttribute("aria-pressed", "false"));
    try {
      const r = await fetch(`/api/suggestions?lang=${state.lang}&audience=${state.aud}`);
      (await r.json()).questions.slice(0, 3).forEach((q) => box.appendChild(chip(q)));
    } catch (_) {}
  }

  function chip(text, quiet) {
    const b = document.createElement("button");
    b.type = "button"; b.className = quiet ? "chip chip-quiet" : "chip"; b.textContent = text;
    b.addEventListener("click", () => ask(text));
    return b;
  }

  /* Topics: a quiet row under the suggestions; picking one swaps the suggestions for its questions. */
  async function loadTopics() {
    const row = $("#topic-row"), toggle = $("#topics-toggle");
    row.innerHTML = ""; row.hidden = true;
    toggle.setAttribute("aria-expanded", "false"); toggle.textContent = t("topics.more");
    state.topics = []; state.topic = null;
    let data;
    try { data = await (await fetch(`/api/topics?lang=${state.lang}`)).json(); } catch (_) { return; }
    data.topics.forEach((tp, i) => {
      const b = document.createElement("button");
      b.type = "button"; b.className = "topic"; b.textContent = tp.label; b.setAttribute("aria-pressed", "false");
      b.addEventListener("click", () => setTopic(state.topic === i ? null : i));
      state.topics.push({ btn: b, questions: tp.questions });
      row.appendChild(b);
    });
  }

  function setTopic(i) {
    if (i === null) { loadChips(); return; }
    state.topic = i;
    state.topics.forEach((tp, k) => tp.btn.setAttribute("aria-pressed", String(k === i)));
    const box = $("#chips");
    box.innerHTML = "";
    state.topics[i].questions.slice(0, 5).forEach((q) => box.appendChild(chip(q)));
    if (!reduced) { box.classList.remove("swap"); void box.offsetWidth; box.classList.add("swap"); }
  }

  function setupTopics() {
    const toggle = $("#topics-toggle"), row = $("#topic-row");
    toggle.addEventListener("click", () => {
      const open = row.hidden;
      row.hidden = !open;
      toggle.setAttribute("aria-expanded", String(open));
      toggle.textContent = t(open ? "topics.less" : "topics.more");
      if (!open && state.topic !== null) setTopic(null);
    });
  }

  /* CV blocks carry data-keys="doc#fragment …" and light up with the sections they come from. */
  function lightCv(id, cls, n) {
    $$("[data-keys]").forEach((el) => {
      const hit = el.dataset.keys.split(/\s+/).some((k) => {
        const [doc, frag] = k.split("#");
        return id.startsWith(`${doc}#`) && id.includes(frag);
      });
      if (!hit) return;
      el.classList.add(cls);
      if (cls === "cited") { el.classList.remove("read"); if (!el.dataset.n) el.dataset.n = n; }
      if (el.classList.contains("more")) openList(el.closest("[data-list]"));
    });
  }

  /* Lists show their most relevant entries; the rest unfold on request, or when an answer cites them. */
  function openList(list, open = true) {
    if (!list) return;
    list.classList.toggle("open", open);
    const key = list.dataset.list;
    const btn = $(`.see-more[data-for="${key}"]`);
    if (!btn) return;
    btn.setAttribute("aria-expanded", String(open));
    btn.textContent = t(open ? `less.${key}` : `more.${key}`);
  }

  function setupSeeMore() {
    $$(".see-more").forEach((btn) => btn.addEventListener("click", () => {
      const list = $(`[data-list="${btn.dataset.for}"]`);
      openList(list, !list.classList.contains("open"));
    }));
  }

  function resetLights() {
    $$("[data-keys]").forEach((x) => { x.classList.remove("read", "cited", "hot"); delete x.dataset.n; });
  }

  function escapeHtml(s) { return s.replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c])); }
  function inline(s) {
    return escapeHtml(s)
      .replace(/\*\*(.+?)\*\*/g, "<strong>$1</strong>")
      .replace(/(^|[^*\w])\*([^*\n]+?)\*(?![*\w])/g, "$1<em>$2</em>")
      .replace(/\[(\d{1,2}(?:\s*,\s*\d{1,2})*)\]/g, (_, list) => list.split(",").map((x) => x.trim())
        .map((x) => `<button type="button" class="cite" data-n="${x}" aria-label="Source ${x}">${x}</button>`).join(""));
  }
  function markdown(text) {
    let html = "", list = null, para = [];
    const flush = () => { if (para.length) { html += `<p>${inline(para.join(" "))}</p>`; para = []; } };
    const close = () => { if (list) { html += `</${list}>`; list = null; } };
    for (const raw of text.replace(/\r/g, "").split("\n")) {
      const line = raw.trim();
      const ul = /^[-*•]\s+(.*)$/.exec(line), ol = /^\d+[.)]\s+(.*)$/.exec(line);
      if (ul || ol) {
        flush();
        const kind = ul ? "ul" : "ol";
        if (list !== kind) { close(); html += `<${kind}>`; list = kind; }
        html += `<li>${inline((ul || ol)[1])}</li>`;
      } else if (!line) { flush(); close(); } else { close(); para.push(line); }
    }
    flush(); close();
    return html;
  }

  function setBusy(flag) {
    state.busy = flag;
    $("#send").setAttribute("aria-busy", String(flag));
    $$(".chip, .ask-about").forEach((c) => { c.disabled = flag; });
  }

  async function ask(question) {
    const q = (question || "").trim();
    if (!q || state.busy) return;
    $("#question").value = "";
    const messages = [...state.history, { role: "user", content: q }].slice(-12);
    setBusy(true);
    resetLights();
    const full = $("#answer-full"), body = $("#answer-body"), src = $("#answer-src"), follow = $("#follow");
    const card = $("#answer");
    card.style.minHeight = `${card.offsetHeight}px`;
    $("#answer-empty").hidden = true;
    full.hidden = false;
    full.classList.remove("show"); void full.offsetWidth; full.classList.add("show");
    $("#answer-q").textContent = q;
    body.innerHTML = ""; body.classList.add("streaming");
    src.hidden = true; src.innerHTML = "";
    follow.hidden = true; follow.innerHTML = "";
    card.focus({ preventScroll: true });

    let text = "", sources = [], followups = [], error = null;
    try {
      const res = await fetch("/api/chat", {
        method: "POST", headers: { "content-type": "application/json" },
        body: JSON.stringify({ messages, lang: state.lang, audience: state.aud }),
      });
      if (res.status === 429) throw new Error("err.rate");
      if (res.status === 503) throw new Error("err.daily");
      if (!res.ok) throw new Error("err.generic");
      const reader = res.body.getReader(), dec = new TextDecoder();
      let buf = "";
      for (;;) {
        const { value, done } = await reader.read();
        if (done) break;
        buf += dec.decode(value, { stream: true });
        let i;
        while ((i = buf.indexOf("\n\n")) >= 0) {
          const block = buf.slice(0, i); buf = buf.slice(i + 2);
          let ev = null, data = null;
          for (const line of block.split("\n")) {
            if (line.startsWith("event: ")) ev = line.slice(7);
            else if (line.startsWith("data: ")) data = JSON.parse(line.slice(6));
          }
          if (ev === "retrieved") markRead(data);
          else if (ev === "text") { text += data; body.innerHTML = markdown(text); }
          else if (ev === "sources") sources = data;
          else if (ev === "followups") followups = data;
          else if (ev === "error") error = data.message;
        }
      }
    } catch (e) {
      error = t(e.message && e.message.startsWith("err.") ? e.message : "err.generic");
    } finally {
      body.classList.remove("streaming");
      setBusy(false);
      card.style.minHeight = "";
    }

    if (error) {
      body.innerHTML = `<p class="err">${escapeHtml(error)}</p>`;
      resetLights();
      return;
    }
    state.history = messages.concat([{ role: "assistant", content: text }]).slice(-12);
    markCited(sources);
    renderSources(sources);
    followups.slice(0, 2).forEach((f) => follow.appendChild(chip(f, true)));
    follow.hidden = !followups.length;
    wireCites(body);
  }

  function markRead(ids) {
    if (!ids || !ids.length) return;
    ids.forEach((id, i) => setTimeout(() => lightCv(id, "read"), reduced ? 0 : 45 * i));
  }

  function markCited(sources) {
    sources.forEach((s, i) => setTimeout(() => lightCv(s.id, "cited", s.n), reduced ? 0 : 200 * i + 150));
  }

  function renderSources(sources) {
    const src = $("#answer-src");
    if (!sources.length) return;
    let lastDoc = null;
    sources.forEach((s) => {
      if (s.doc_title !== lastDoc) {
        lastDoc = s.doc_title;
        const d = document.createElement("div");
        d.className = "doc"; d.textContent = s.doc_title;
        src.appendChild(d);
      }
      const row = document.createElement("div");
      row.className = "src"; row.dataset.n = s.n;
      row.innerHTML = `<b>${s.n}</b><span>${escapeHtml(s.section_title)}</span>`;
      row.addEventListener("mouseenter", () => hot(s.n));
      row.addEventListener("mouseleave", () => hot(null));
      src.appendChild(row);
    });
    src.hidden = false;
  }

  function hot(n) {
    $$(".hot").forEach((e) => e.classList.remove("hot"));
    if (n == null) return;
    $$(`.cite[data-n="${n}"], .src[data-n="${n}"], [data-keys][data-n="${n}"]`).forEach((e) => e.classList.add("hot"));
  }

  function wireCites(root) {
    $$(".cite", root).forEach((b) => {
      b.addEventListener("mouseenter", () => hot(b.dataset.n));
      b.addEventListener("mouseleave", () => hot(null));
      b.addEventListener("focus", () => hot(b.dataset.n));
      b.addEventListener("blur", () => hot(null));
      b.addEventListener("click", () => {
        hot(b.dataset.n);
        const target = $(`[data-keys][data-n="${b.dataset.n}"]`);
        if (target) target.scrollIntoView({ behavior: reduced ? "auto" : "smooth", block: "center" });
      });
    });
  }

  function setupNav() {
    // Scroll-spy: the bar marks the section in view; a floating "Ask" appears once the box is scrolled past.
    const links = $$(".bar-nav a[href^='#']");
    const targets = links.map((a) => $(a.getAttribute("href"))).filter(Boolean);
    if ("IntersectionObserver" in window && targets.length) {
      const io = new IntersectionObserver((entries) => {
        entries.forEach((e) => {
          if (!e.isIntersecting) return;
          links.forEach((a) => {
            const on = a.getAttribute("href") === `#${e.target.id}`;
            a.classList.toggle("active", on);
            if (on) $("#nav-current").textContent = a.textContent;
          });
        });
      }, { rootMargin: "-35% 0px -55% 0px", threshold: 0 });
      targets.forEach((el) => io.observe(el));
    }
    // On phones the bar shows the current section as a button that opens the list of sections.
    const bar = $(".bar"), toggle = $("#nav-toggle");
    const closeNav = () => { bar.classList.remove("open"); toggle.setAttribute("aria-expanded", "false"); };
    toggle.addEventListener("click", () => {
      const open = !bar.classList.contains("open");
      bar.classList.toggle("open", open);
      toggle.setAttribute("aria-expanded", String(open));
    });
    links.forEach((a) => a.addEventListener("click", closeNav));
    document.addEventListener("keydown", (e) => { if (e.key === "Escape") closeNav(); });
    document.addEventListener("click", (e) => { if (!bar.contains(e.target)) closeNav(); });
    const fab = $("#ask-fab"), askRow = $(".ask-row");
    if (fab && askRow && "IntersectionObserver" in window) {
      const io2 = new IntersectionObserver((entries) => {
        const e = entries[0];
        fab.hidden = e.isIntersecting || e.boundingClientRect.top > 0;
      }, { threshold: 0 });
      io2.observe(askRow);
      fab.addEventListener("click", () => {
        $("#ask").scrollIntoView({ behavior: reduced ? "auto" : "smooth", block: "start" });
        setTimeout(() => $("#question").focus({ preventScroll: true }), reduced ? 0 : 450);
      });
    }
  }

  function setupProjects() {
    // The whole card opens its project page; links inside keep their own targets.
    $$(".proj").forEach((card) => {
      const detail = $(".proj-detail", card);
      if (!detail) return;
      card.classList.add("clickable");
      card.addEventListener("click", (e) => {
        if (e.target.closest("a")) return;
        location.href = detail.href;
      });
    });
  }

  function setupCv() {
    $$(".ask-about").forEach((btn) => btn.addEventListener("click", () => {
      $("#answer").scrollIntoView({ behavior: reduced ? "auto" : "smooth", block: "start" });
      ask(t(btn.dataset.ask));
    }));
  }

  function setupCopy() {
    $$(".copy, .mini").forEach((btn) => btn.addEventListener("click", async () => {
      try { await navigator.clipboard.writeText($(btn.dataset.copy).textContent); } catch (_) {}
      const label = btn.dataset.i18n;
      btn.textContent = t(label === "contact.copy" ? "contact.copied" : "mcp.copied");
      btn.classList.add("done");
      setTimeout(() => { btn.textContent = t(label); btn.classList.remove("done"); }, 1600);
    }));
  }

  function setupMcp() {
    const url = `${location.origin}/mcp`;
    $("#mcp-url").textContent = url;
    $("#snippet-claude-code").textContent = `claude mcp add --transport http lean-profile ${url}`;
    $("#snippet-claude-desktop").textContent = JSON.stringify(
      { mcpServers: { "lean-profile": { command: "npx", args: ["-y", "mcp-remote", url] } } }, null, 2);
    $$(".tabs [role=tab]").forEach((tab) => tab.addEventListener("click", () => {
      $$(".tabs [role=tab]").forEach((x) => x.setAttribute("aria-selected", String(x === tab)));
      $$(".tabpanel").forEach((p) => { p.hidden = p.dataset.panel !== tab.dataset.tab; });
    }));
  }

  function setupHeat() {
    // A quiet detection-coverage heat map behind the hero: cells that brighten and dim on their own clocks.
    const heat = $("#heat");
    if (!heat) return;
    const frag = document.createDocumentFragment();
    for (let i = 0; i < 162; i++) {
      const cell = document.createElement("i");
      const hot = Math.random() < 0.12;
      cell.style.setProperty("--o", (0.03 + Math.random() * 0.07).toFixed(3));
      cell.style.setProperty("--o2", (hot ? 0.38 + Math.random() * 0.2 : 0.12 + Math.random() * 0.2).toFixed(3));
      cell.style.setProperty("--dur", `${(4 + Math.random() * 6).toFixed(2)}s`);
      cell.style.setProperty("--delay", `-${(Math.random() * 10).toFixed(2)}s`);
      frag.appendChild(cell);
    }
    heat.appendChild(frag);
  }

  function placeContact() {
    // On phones the question box comes first; the contact card follows the answer.
    const reach = $(".reach"), hero = $(".hero"), answer = $("#answer");
    const narrow = matchMedia("(max-width: 760px)");
    const place = () => {
      if (narrow.matches) { if (reach.previousElementSibling !== answer) answer.after(reach); }
      else if (reach.parentElement !== hero) hero.appendChild(reach);
    };
    place();
    narrow.addEventListener("change", place);
  }

  function setupMotion() {
    // Entrances only play on a visible page; a hidden tab (or reduced motion) gets everything at rest.
    if (reduced || document.hidden || !("IntersectionObserver" in window)) return;
    document.documentElement.classList.add("motion");
    $$(".in").forEach((el, i) => el.style.setProperty("--d", `${i * 60}ms`));
    // Safety net: whatever happens to the entrance animations, everything is at rest after 2.5s.
    setTimeout(() => {
      document.documentElement.classList.add("settled");
      $$(".reveal").forEach((el) => { if (el.getBoundingClientRect().top < innerHeight) el.classList.add("seen"); });
    }, 2500);
    const groups = [".cv-head", ".exp-item", ".cv-col", ".projects h2", ".proj", ".mcp-band", ".facts-band h2", ".facts div", ".how h2", ".how-grid > div", ".foot-name"];
    const els = [];
    groups.forEach((sel) => $$(sel).forEach((el, i) => { el.classList.add("reveal"); el.style.setProperty("--d", `${Math.min(i, 5) * 70}ms`); els.push(el); }));
    const io = new IntersectionObserver((entries) => {
      entries.forEach((e) => { if (e.isIntersecting) { e.target.classList.add("seen"); io.unobserve(e.target); } });
    }, { threshold: 0.12, rootMargin: "0px 0px -40px 0px" });
    els.forEach((el) => io.observe(el));
  }

  function init() {
    $$("[data-i18n]").forEach((el) => ORIG.set(el, el.textContent));
    $$("[data-i18n-alt]").forEach((el) => { el.dataset.origAlt = el.alt; });
    $$("[data-i18n-placeholder]").forEach((el) => { el.dataset.origPlaceholder = el.placeholder; });
    const param = new URLSearchParams(location.search).get("lang");
    let saved = null;
    try { saved = localStorage.getItem("lang"); } catch (_) {}
    placeContact();
    setupHeat();
    setupMotion();
    applyLanguage(param || saved || "es");
    const preset = new URLSearchParams(location.search).get("q");
    if (preset) {
      history.replaceState(null, "", `/?lang=${state.lang}`);
      $("#ask").scrollIntoView({ behavior: "auto", block: "start" });
      setTimeout(() => ask(preset), 300);
    }
    $$(".lang button").forEach((b) => b.addEventListener("click", () => { if (b.dataset.lang !== state.lang) applyLanguage(b.dataset.lang); }));
    $$(".aud-tabs [role=tab]").forEach((b) => b.addEventListener("click", () => setAudience(b.dataset.aud, true)));
    $("#ask").addEventListener("submit", (e) => { e.preventDefault(); ask($("#question").value); });
    setupCv();
    setupProjects();
    setupSeeMore();
    setupTopics();
    setupNav();
    setupMcp();
    setupCopy();
  }

  document.addEventListener("DOMContentLoaded", init);
})();

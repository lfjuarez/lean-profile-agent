(() => {
  "use strict";

  const I18N = {
    en: {
      "nav.skip": "Skip to the question box", "nav.map": "Source map", "nav.mcp": "MCP", "nav.how": "How it works",
      "hero.alt": "Portrait of Leandro F. Juárez",
      "hero.statement": "SIEM, SOAR and detection engineering consultant, and Splunk instructor. This CV answers your questions, with sources.",
      "certs.instructor": "Splunk Certified Instructor", "certs.note": "· Power User Fast Start, authorized by Splunk",
      "hero.cv": "Download CV", "hero.cvAlt": "CV en español",
      "contact.email": "Email", "contact.copy": "Copy", "contact.copied": "Copied", "contact.where": "Based in", "contact.whereV": "Buenos Aires, Argentina · remote",
      "ask.label": "Ask about my professional experience", "ask.placeholder": "Type your question…", "ask.send": "Ask",
      "answer.empty": "Answers only from my documented experience, with sources. Each answer lights up, in the map below, the sections it read and the ones it cites.",
      "map.title": "Source map", "map.read": "read for the answer", "map.cited": "cited",
      "map.count": "{n} documented sections", "map.active": "{r} read · {k} cited", "map.sections": "{n} sections",
      "map.case": "Case study", "map.ask": "Tell me about “{t}” ({d})",
      "facts.title": "In numbers", "facts.it": "years in IT", "facts.siem": "years in SIEM and detection",
      "facts.rules": "detection rules migrated with AI agents", "facts.sources": "data sources in one security data lake",
      "err.generic": "Something went wrong. Try again.", "err.rate": "Too many questions in a short time. Wait a minute.",
      "err.daily": "The daily question limit for this demo was reached. Come back tomorrow or write to Leandro.",
      "mcp.title": "Ask it from your own AI too", "mcp.howto": "How to connect it", "mcp.tools": "Six read-only tools:",
      "mcp.intro": "This CV is also a read-only MCP server. Add the URL to Claude, ChatGPT or any MCP client and question it from your own assistant, with the same sources.",
      "mcp.copy": "Copy URL", "mcp.copied": "Copied",
      "mcp.desktop": "Settings, Connectors, Add custom connector, then paste the URL. Or add it to claude_desktop_config.json:",
      "mcp.chatgpt": "Settings, Connectors, Advanced, Developer mode, Create. Paste the URL as the MCP server URL, with no authentication.",
      "how.title": "How it works",
      "how.s1t": "Curated documents", "how.s1": "Eleven documents in Spanish and English. Each tile of the source map is one section of them, and nothing else is used.",
      "how.s2t": "Search first, then the model", "how.s2": "Each question selects the relevant sections. The model answers only from them and cites them; with nothing relevant, the server declines without calling it.",
      "how.s3t": "Sources you can see", "how.s3": "Read sections turn pale green and cited ones dark green. Case study figures are synthetic; method and deliverables are real.",
      "how.s4t": "Limits, honestly", "how.s4": "The wording can still be imperfect, so every answer shows its sources and the CV is one click away. It does not replace a conversation.",
      "foot.synthetic": "Case study figures are synthetic; method and deliverables are real.",
      "honest": "Answers only from my documented experience, with sources."
    },
    es: {
      "nav.skip": "Ir a la caja de preguntas", "nav.map": "Mapa de fuentes", "nav.mcp": "MCP", "nav.how": "Cómo funciona",
      "hero.alt": "Retrato de Leandro F. Juárez",
      "hero.statement": "Consultor de SIEM, SOAR e ingeniería de detección, e instructor de Splunk. Este CV responde tus preguntas, con fuentes.",
      "certs.instructor": "Splunk Certified Instructor", "certs.note": "· Power User Fast Start, habilitado por Splunk",
      "hero.cv": "Descargar CV", "hero.cvAlt": "CV in English",
      "contact.email": "Email", "contact.copy": "Copiar", "contact.copied": "Copiado", "contact.where": "Ubicación", "contact.whereV": "Buenos Aires, Argentina · remoto",
      "ask.label": "Preguntale a mi experiencia profesional", "ask.placeholder": "Escribí tu pregunta…", "ask.send": "Preguntar",
      "answer.empty": "Respuestas solo a partir de mi experiencia documentada, con fuentes. Cada respuesta enciende, en el mapa de abajo, las secciones que leyó y las que cita.",
      "map.title": "Mapa de fuentes", "map.read": "leída para la respuesta", "map.cited": "citada",
      "map.count": "{n} secciones documentadas", "map.active": "{r} leídas · {k} citadas", "map.sections": "{n} secciones",
      "map.case": "Caso de estudio", "map.ask": "Contame sobre «{t}» ({d})",
      "facts.title": "En números", "facts.it": "años en IT", "facts.siem": "años en SIEM y detección",
      "facts.rules": "reglas de detección migradas con agentes de IA", "facts.sources": "fuentes de datos en un data lake de seguridad",
      "err.generic": "Algo salió mal. Probá de nuevo.", "err.rate": "Demasiadas preguntas en poco tiempo. Esperá un minuto.",
      "err.daily": "Se alcanzó el límite diario de preguntas de esta demo. Volvé mañana o escribile a Leandro.",
      "mcp.title": "Preguntale también desde tu propia IA", "mcp.howto": "Cómo conectarlo", "mcp.tools": "Seis herramientas de solo lectura:",
      "mcp.intro": "Este CV también es un servidor MCP de solo lectura. Sumá la URL a Claude, ChatGPT o cualquier cliente MCP y preguntale desde tu propio asistente, con las mismas fuentes.",
      "mcp.copy": "Copiar URL", "mcp.copied": "Copiado",
      "mcp.desktop": "Configuración, Conectores, Agregar conector personalizado, y pegá la URL. O agregalo a claude_desktop_config.json:",
      "mcp.chatgpt": "Configuración, Conectores, Avanzado, Modo desarrollador, Crear. Pegá la URL como URL del servidor MCP, sin autenticación.",
      "how.title": "Cómo funciona",
      "how.s1t": "Documentos curados", "how.s1": "Once documentos en español e inglés. Cada etiqueta del mapa de fuentes es una sección de ellos, y no se usa nada más.",
      "how.s2t": "Primero búsqueda, después el modelo", "how.s2": "Cada pregunta elige las secciones relevantes. El modelo responde solo con ellas y las cita; si no hay nada relevante, el servidor declina sin llamarlo.",
      "how.s3t": "Fuentes a la vista", "how.s3": "Las secciones leídas se pintan verde claro y las citadas verde oscuro. Las cifras de los casos de estudio son sintéticas; el método y los entregables son reales.",
      "how.s4t": "Límites, con honestidad", "how.s4": "La redacción todavía puede ser imperfecta; por eso cada respuesta muestra sus fuentes y el CV está a un clic. No reemplaza una conversación.",
      "foot.synthetic": "Las cifras de los casos de estudio son sintéticas; el método y los entregables son reales.",
      "honest": "Respuestas solo a partir de mi experiencia documentada, con fuentes."
    }
  };

  const $ = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => Array.from(r.querySelectorAll(s));
  const reduced = matchMedia("(prefers-reduced-motion: reduce)").matches;
  const state = { lang: "en", history: [], busy: false, tiles: new Map(), total: 0, firstLoad: true };
  const t = (k, vars) => {
    let s = (I18N[state.lang] && I18N[state.lang][k]) || I18N.en[k] || k;
    if (vars) for (const [a, b] of Object.entries(vars)) s = s.replace(`{${a}}`, b);
    return s;
  };

  function applyLanguage(lang) {
    state.lang = lang === "es" ? "es" : "en";
    document.documentElement.lang = state.lang;
    try { localStorage.setItem("lang", state.lang); } catch (_) {}
    $$("[data-i18n]").forEach((el) => { el.textContent = t(el.dataset.i18n); });
    $$("[data-i18n-placeholder]").forEach((el) => { el.placeholder = t(el.dataset.i18nPlaceholder); });
    $$("[data-i18n-alt]").forEach((el) => { el.alt = t(el.dataset.i18nAlt); });
    $$(".lang button").forEach((b) => b.setAttribute("aria-pressed", String(b.dataset.lang === state.lang)));
    const main = state.lang === "es" ? "ES" : "EN", alt = state.lang === "es" ? "EN" : "ES";
    $("#cv-link").href = `/cv/Leandro_Juarez_CV_${main}.pdf`;
    $("#cv-alt").href = `/cv/Leandro_Juarez_CV_${alt}.pdf`;
    state.history = [];
    $("#answer-full").hidden = true;
    $("#answer-empty").hidden = false;
    loadMap();
    loadChips();
  }

  async function loadChips() {
    const box = $("#chips");
    box.innerHTML = "";
    try {
      const r = await fetch(`/api/suggestions?lang=${state.lang}`);
      (await r.json()).questions.slice(0, 3).forEach((q) => box.appendChild(chip(q)));
    } catch (_) {}
  }

  function chip(text, quiet) {
    const b = document.createElement("button");
    b.type = "button"; b.className = quiet ? "chip chip-quiet" : "chip"; b.textContent = text;
    b.addEventListener("click", () => ask(text));
    return b;
  }

  function makeRow(name, sub, cells, startIndex) {
    const row = document.createElement("div");
    row.className = "row";
    const h = document.createElement("h3");
    h.className = "row-name";
    h.textContent = name;
    const s = document.createElement("span");
    s.textContent = sub;
    h.appendChild(s);
    const tiles = document.createElement("div");
    tiles.className = "tiles";
    cells.forEach((cell, i) => {
      const b = document.createElement("button");
      b.type = "button"; b.className = "tile"; b.setAttribute("role", "listitem");
      b.textContent = cell.title.replace(/\s*\([^)]*\)\s*$/, "");
      b.title = `${cell.group || cell.doc_title} › ${cell.title}`;
      b.dataset.id = cell.id;
      b.style.setProperty("--i", startIndex + i);
      b.addEventListener("click", () => {
        $("#answer").scrollIntoView({ behavior: reduced ? "auto" : "smooth", block: "start" });
        ask(t("map.ask", { t: cell.title, d: cell.group || cell.doc_title }));
      });
      state.tiles.set(cell.id, b);
      tiles.appendChild(b);
    });
    row.append(h, tiles);
    return row;
  }

  async function loadMap() {
    const box = $("#map-rows");
    let data;
    try { data = await (await fetch(`/api/matrix?lang=${state.lang}`)).json(); } catch (_) { return; }
    box.innerHTML = "";
    box.classList.remove("dimmed");
    state.tiles.clear();
    let n = 0;
    const cols = data.columns;
    cols.forEach((col, ci) => {
      const isCases = ci === cols.length - 1;
      if (isCases) {
        const groups = [];
        col.cells.forEach((c) => {
          let g = groups.find((x) => x.name === c.group);
          if (!g) { g = { name: c.group, cells: [] }; groups.push(g); }
          g.cells.push(c);
        });
        groups.forEach((g) => { box.appendChild(makeRow(g.name, t("map.case"), g.cells, n)); n += g.cells.length; });
      } else {
        box.appendChild(makeRow(col.label, t("map.sections", { n: col.cells.length }), col.cells, n));
        n += col.cells.length;
      }
    });
    state.total = n;
    updateCount();
    if (state.firstLoad && !reduced) {
      const io = new IntersectionObserver((entries) => {
        if (entries.some((e) => e.isIntersecting)) {
          box.classList.add("scan");
          setTimeout(() => box.classList.remove("scan"), 2600);
          io.disconnect();
        }
      }, { threshold: 0.2 });
      io.observe(box);
    }
    state.firstLoad = false;
  }

  function updateCount() {
    const active = $("#map-rows").classList.contains("dimmed");
    $("#map-count").textContent = active
      ? t("map.active", { r: $$(".tile.read, .tile.cited").length, k: $$(".tile.cited").length })
      : t("map.count", { n: state.total });
  }

  function resetMap() {
    $("#map-rows").classList.remove("dimmed");
    $$(".tile").forEach((x) => { x.classList.remove("read", "cited", "pop", "hot"); delete x.dataset.n; });
    updateCount();
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
    $$(".chip").forEach((c) => { c.disabled = flag; });
  }

  async function ask(question) {
    const q = (question || "").trim();
    if (!q || state.busy) return;
    $("#question").value = "";
    const messages = [...state.history, { role: "user", content: q }].slice(-12);
    setBusy(true);
    resetMap();
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
        body: JSON.stringify({ messages, lang: state.lang }),
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
      resetMap();
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
    $("#map-rows").classList.add("dimmed");
    ids.forEach((id, i) => {
      const tile = state.tiles.get(id);
      if (tile) setTimeout(() => { tile.classList.add("read"); updateCount(); }, reduced ? 0 : 45 * i);
    });
  }

  function markCited(sources) {
    if (!sources.length) return;
    $("#map-rows").classList.add("dimmed");
    sources.forEach((s, i) => {
      const tile = state.tiles.get(s.id);
      if (!tile) return;
      setTimeout(() => {
        tile.dataset.n = s.n;
        tile.classList.add("cited", "pop");
        updateCount();
      }, reduced ? 0 : 200 * i + 150);
    });
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
    $$(`.tile[data-n="${n}"], .cite[data-n="${n}"], .src[data-n="${n}"]`).forEach((e) => e.classList.add("hot"));
  }

  function wireCites(root) {
    $$(".cite", root).forEach((b) => {
      b.addEventListener("mouseenter", () => hot(b.dataset.n));
      b.addEventListener("mouseleave", () => hot(null));
      b.addEventListener("focus", () => hot(b.dataset.n));
      b.addEventListener("blur", () => hot(null));
      b.addEventListener("click", () => {
        hot(b.dataset.n);
        const tile = $(`.tile[data-n="${b.dataset.n}"]`);
        if (tile) tile.scrollIntoView({ behavior: reduced ? "auto" : "smooth", block: "center" });
      });
    });
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
    $$(".in").forEach((el, i) => el.style.setProperty("--d", `${i * 70}ms`));
    const bar = $(".bar");
    addEventListener("scroll", () => bar.classList.toggle("scrolled", scrollY > 8), { passive: true });
    if (reduced || !("IntersectionObserver" in window)) return;
    const groups = [".mcp-band", ".map-head", ".facts-band h2", ".facts div", ".how h2", ".how-grid > div", ".foot-name"];
    const els = [];
    groups.forEach((sel) => $$(sel).forEach((el, i) => { el.classList.add("reveal"); el.style.setProperty("--d", `${i * 80}ms`); els.push(el); }));
    const io = new IntersectionObserver((entries) => {
      entries.forEach((e) => { if (e.isIntersecting) { e.target.classList.add("seen"); io.unobserve(e.target); } });
    }, { threshold: 0.15, rootMargin: "0px 0px -40px 0px" });
    els.forEach((el) => io.observe(el));
  }

  function init() {
    const param = new URLSearchParams(location.search).get("lang");
    let saved = null;
    try { saved = localStorage.getItem("lang"); } catch (_) {}
    const browser = (navigator.language || "en").toLowerCase().startsWith("es") ? "es" : "en";
    placeContact();
    setupMotion();
    applyLanguage(param || saved || browser);
    $$(".lang button").forEach((b) => b.addEventListener("click", () => { if (b.dataset.lang !== state.lang) applyLanguage(b.dataset.lang); }));
    $("#ask").addEventListener("submit", (e) => { e.preventDefault(); ask($("#question").value); });
    setupMcp();
    setupCopy();
  }

  document.addEventListener("DOMContentLoaded", init);
})();

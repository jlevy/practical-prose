/*
 * Practical Prose — Tip-panels component (Detail + Assessment).
 *
 * Two side-panels update on hover of any `[data-tip-kind]` element
 * (which the bi-card component emits). The functions are lifted from
 * tools/explorations/visual-design/dimension-visualizations.html so any
 * change in the workbench flows straight through the sync script.
 *
 * Public API:
 *
 *   PracticalProseTipPanels.mount(detail, assess, data, biCardApi?, opts?)
 *
 * Arguments:
 *   detail        CSS selector OR Element for the "Evaluation Detail" panel.
 *   assess        CSS selector OR Element for the "Assessment" panel.
 *   data          { groups, dimensions, rubric, doc | docs }
 *                 - `doc`  — single doc (the pprose-render case)
 *                 - `docs` — array of docs (the explorations workbench case
 *                            with multiple bi-cards in one .bi-stack)
 *   biCardApi     Optional return value from PracticalProseBiCard.makeApi().
 *                 When provided, the Assessment panel uses biCardApi.biDim9B
 *                 to mirror the same dim widget that lives in the card.
 *   opts.scope    Optional Element to attach pointerover/pointerleave
 *                 listeners to. Default: `document`. Pass the per-viz
 *                 layout element when more than one tip-panel pair share
 *                 the same page (the workbench does this).
 *
 * Returns `{ onOver, showPlaceholder }` so a caller that wants to manage
 * its own listener attachment can do so; the default behavior wires the
 * listeners onto `opts.scope` automatically.
 *
 * Depends on `window.marked` (the markdown library; vendored as
 * marked.min.js alongside this file).
 */

(() => {
  function _resolve(target) {
    if (!target) return null;
    if (typeof target === "string") return document.querySelector(target);
    return target;
  }

  function mount(detail, assess, data, biCardApi, opts) {
    const detailEl = _resolve(detail);
    const assessEl = _resolve(assess);
    if (!detailEl || !assessEl) {
      console.error("PracticalProseTipPanels.mount: panel(s) not found", detail, assess);
      return null;
    }
    if (!data?.rubric) {
      console.error("PracticalProseTipPanels.mount: data.rubric missing", data);
      return null;
    }

    const rubric = data.rubric;
    const groups = data.groups || [];
    const dims = data.dimensions || [];
    // Accept `docs` (array, workbench multi-doc case) or `doc` (single,
    // pprose-render case).
    const biRealDocs = Array.isArray(data.docs) ? data.docs : data.doc ? [data.doc] : [];

    // ─── Local el helper (same shape as bi-card's; kept here so the
    // tip-panels component can be loaded independently of bi-card). ──
    function el(tag, attrs = {}, ...children) {
      const e = document.createElement(tag);
      Object.entries(attrs).forEach(([k, v]) => {
        if (k === "style" && typeof v === "object") Object.assign(e.style, v);
        else if (k === "class") e.className = v;
        else if (k.startsWith("on") && typeof v === "function") e.addEventListener(k.slice(2), v);
        else e.setAttribute(k, v);
      });
      children.flat().forEach((c) => {
        if (c == null) return;
        e.appendChild(typeof c === "string" ? document.createTextNode(c) : c);
      });
      return e;
    }

    function mountPanel(panel, heading) {
      panel.appendChild(el("div", { class: "tip-panel-heading eyebrow" }, heading));
      const content = el("div", { class: "tip-content" });
      panel.appendChild(content);
      return content;
    }
    const detailContent = mountPanel(detailEl, "Evaluation Detail");
    const assessContent = mountPanel(assessEl, "Assessment");

    function setMarkdown(contentEl, md) {
      contentEl.innerHTML = marked.parse(md, {
        breaks: true,
        gfm: true,
      });
      contentEl.classList.remove("fade-in");
      void contentEl.offsetWidth;
      contentEl.classList.add("fade-in");
    }

    function hideAssess() {
      assessEl.classList.add("is-empty");
    }
    function showAssess() {
      assessEl.classList.remove("is-empty");
    }
    function hideDetail() {
      detailEl.classList.add("is-empty");
    }
    function showDetail() {
      detailEl.classList.remove("is-empty");
    }

    function showPlaceholder() {
      _lastSig = "";
      hideDetail();
      hideAssess();
    }

    function renderDim(key, docId) {
      const r = rubric[key];
      if (!r) return showPlaceholder();

      const rulesMd = r.rules?.length
        ? `\n\n## Rules\n\n${r.rules.map((rule) => `- ${rule}`).join("\n")}`
        : "";

      const detailMd = `# *${r.label}*

*${r.question || ""}*${rulesMd}`;
      showDetail();
      setMarkdown(detailContent, detailMd);

      const doc = docId ? biRealDocs.find((d) => d.id === docId) : null;
      if (!doc) {
        hideAssess();
        return;
      }
      showAssess();

      const score = doc.scores[key];
      const reason = doc.reasons ? doc.reasons[key] : undefined;
      const findings = doc.findings?.[key] || [];

      const escapeHtml = (s) => (s || "").replace(/</g, "&lt;");
      let bodyHtml = "";
      if (typeof score === "number" && findings.length) {
        const items = findings
          .map(
            (f) =>
              `<li><strong>Rule ${f.rule_number ?? "?"} · ${f.verdict || "noted"}</strong> — ${escapeHtml(f.description)}</li>`,
          )
          .join("");
        bodyHtml = `<div class="tip-assessment"><ul>${items}</ul></div>`;
      } else if (reason) {
        bodyHtml = `<div class="tip-assessment"><p>${escapeHtml(reason)}</p></div>`;
      } else {
        bodyHtml = `<div class="tip-assessment"><p class="tip-empty">No assessment recorded for this dimension.</p></div>`;
      }

      assessContent.innerHTML = "";
      const dimMeta = dims.find((dd) => dd.id === key);
      if (dimMeta && biCardApi?.biDim9B) {
        const dimRow = biCardApi.biDim9B(doc, dimMeta, "right");
        const mirror = el(
          "div",
          { class: "bi-ltr bi-tip-dim-mirror" },
          el("div", { class: "bi-col right" }, dimRow),
        );
        assessContent.appendChild(mirror);
      }
      const bodyEl = el("div");
      bodyEl.innerHTML = bodyHtml;
      assessContent.appendChild(bodyEl);
      assessContent.classList.remove("fade-in");
      void assessContent.offsetWidth;
      assessContent.classList.add("fade-in");
    }

    function renderGroup(key) {
      const g = groups.find((g) => g.id === key);
      if (!g) return showPlaceholder();
      const groupDims = dims.filter((d) => d.g === g.id);

      const sense = g.sense ? `${g.sense.charAt(0).toUpperCase() + g.sense.slice(1)}.` : "";

      const dimsMd = groupDims
        .map((d) => {
          const r = rubric[d.id];
          const q = r?.question || "";
          return `**${d.label}**${q ? ` — ${q}` : ""}`;
        })
        .join("\n\n");

      const md = `# ${g.label}

${sense}

${dimsMd}`;
      showDetail();
      setMarkdown(detailContent, md);
      hideAssess();
    }

    // Slide both panels vertically to align with the hovered bi-card.
    function moveToCard(trig) {
      if (!matchMedia("(min-width: 72rem)").matches) return;
      const card = trig.closest(".bi-card");
      const layout = detailEl.parentElement;
      if (!card || !layout) return;
      const layoutRect = layout.getBoundingClientRect();
      const cardRect = card.getBoundingClientRect();
      const top = `${cardRect.top - layoutRect.top}px`;
      detailEl.style.top = top;
      assessEl.style.top = top;
    }

    let _lastSig = "";

    function onOver(e) {
      const trig = e.target.closest("[data-tip-kind]");
      if (!trig) return;
      const kind = trig.dataset.tipKind;
      const key = trig.dataset.tipKey;
      const docId = trig.dataset.tipDoc;
      const sig = `${kind}/${key}/${docId || ""}`;
      if (sig === _lastSig) {
        moveToCard(trig);
        return;
      }
      _lastSig = sig;
      if (kind === "dim" || kind === "score") renderDim(key, docId);
      else if (kind === "group") renderGroup(key);
      moveToCard(trig);
    }

    // Wire hover handlers. Default scope is `document` (single-instance
    // case — pprose render). Workbench passes opts.scope = layoutEl so
    // each per-viz tip-panel pair only listens within its own layout.
    const scope = opts?.scope ? _resolve(opts.scope) : document;
    scope.addEventListener("pointerover", onOver);
    scope.addEventListener("pointerleave", showPlaceholder);

    showPlaceholder();
    return { onOver, showPlaceholder };
  }

  // Extend rather than replace so other components can co-exist in the
  // same namespace if they ever choose to.
  globalThis.PracticalProseTipPanels = globalThis.PracticalProseTipPanels || {};
  const ns = globalThis.PracticalProseTipPanels;
  ns.mount = mount;
})();

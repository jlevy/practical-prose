/*
 * Practical Prose — Tip-panels component (Detail + Assessment).
 *
 * Two side-panels update on hover of any `[data-tip-kind]` element
 * (which the bi-card component emits). The functions inside are lifted
 * verbatim from tools/explorations/visual-design/dimension-visualizations.html
 * so any change in the workbench flows straight through the sync script.
 *
 * Public API:
 *     PracticalProseTipPanels.mount(detailSelector, assessSelector, data, biCardApi?)
 *
 * Arguments:
 *   detailSelector  CSS selector for the "Evaluation Detail" panel.
 *   assessSelector  CSS selector for the "Assessment" panel.
 *   data            same shape as the bi-card data contract:
 *                     { groups, dimensions, rubric, doc }
 *                   (the doc-array form is currently single-doc; future
 *                   compare variants will accept data.docs[]).
 *   biCardApi       optional return value of PracticalProseBiCard.mount().
 *                   When provided, the Assessment panel uses biCardApi.biDim9B
 *                   to mirror the same dim widget that lives in the card.
 *                   Pass it when both components are mounted on the same
 *                   page so the mirror stays in sync.
 *
 * Depends on `window.marked` (the markdown library; vendored as
 * marked.min.js alongside this file).
 */

(() => {
  function mount(detailSelector, assessSelector, data, biCardApi) {
    const detailEl =
      typeof detailSelector === "string"
        ? document.querySelector(detailSelector)
        : detailSelector;
    const assessEl =
      typeof assessSelector === "string"
        ? document.querySelector(assessSelector)
        : assessSelector;
    if (!detailEl || !assessEl) {
      console.error(
        "PracticalProseTipPanels.mount: panel(s) not found",
        detailSelector,
        assessSelector,
      );
      return;
    }
    if (!data || !data.rubric || !data.doc) {
      console.error("PracticalProseTipPanels.mount: malformed data", data);
      return;
    }

    const rubric = data.rubric;
    const groups = data.groups || [];
    const dims = data.dimensions || [];
    // The hover panel was authored for a multi-doc workbench (biRealDocs);
    // here we keep the same array shape but with one entry.
    const biRealDocs = [data.doc];

    // ─── el helper (kept local; same as bi-card's) ──────────────────────
    function el(tag, attrs = {}, ...children) {
      const e = document.createElement(tag);
      Object.entries(attrs).forEach(([k, v]) => {
        if (k === "style" && typeof v === "object") Object.assign(e.style, v);
        else if (k === "class") e.className = v;
        else if (k.startsWith("on") && typeof v === "function")
          e.addEventListener(k.slice(2), v);
        else e.setAttribute(k, v);
      });
      children.flat().forEach((c) => {
        if (c == null) return;
        e.appendChild(typeof c === "string" ? document.createTextNode(c) : c);
      });
      return e;
    }

    // ─── Panel chrome ───────────────────────────────────────────────────
    function mountPanel(panel, heading) {
      panel.appendChild(
        el("div", { class: "tip-panel-heading eyebrow" }, heading),
      );
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

      const rulesMd = r.rules && r.rules.length
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
      const findings = (doc.findings && doc.findings[key]) || [];

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
      if (dimMeta && biCardApi && biCardApi.biDim9B) {
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

      const sense = g.sense
        ? g.sense.charAt(0).toUpperCase() + g.sense.slice(1) + "."
        : "";

      const dimsMd = groupDims
        .map((d) => {
          const r = rubric[d.id];
          const q = r?.question || "";
          return `**${d.label}**${q ? " — " + q : ""}`;
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
    // Only on wide layouts where the panels sit in a flex row next to the
    // stack.
    function moveToCard(trig) {
      if (!matchMedia("(min-width: 72rem)").matches) return;
      const card = trig.closest(".bi-card");
      const layout = detailEl.parentElement;
      if (!card || !layout) return;
      const layoutRect = layout.getBoundingClientRect();
      const cardRect = card.getBoundingClientRect();
      const top = cardRect.top - layoutRect.top + "px";
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

    // Wire hover handlers onto the document so any [data-tip-kind] trigger
    // (today: card; future: comparison page rows) updates the panels.
    document.addEventListener("pointerover", onOver);
    document.addEventListener("pointerleave", showPlaceholder);

    showPlaceholder();
  }

  globalThis.PracticalProseTipPanels = Object.freeze({ mount });
})();

/*
 * Practical Prose — Visual 9B "bi-card" component.
 *
 * Renders the bidirectional-bars eval card (one per document). The JS
 * functions inside the IIFE are lifted verbatim from
 * tools/explorations/visual-design/dimension-visualizations.html so any
 * future change in the workbench flows straight through the sync script.
 *
 * Public API:
 *     PracticalProseBiCard.mount(containerSelector, data)
 *
 * Data contract (object passed to mount):
 *   data.groups       Array of { id, label } — 6 entries (P, E, F, R, G, J)
 *   data.dimensions   Array of { id, label, g } — 20 entries (P1..J3)
 *   data.rubric       Object keyed by dim id: { question, rules: string[], group }
 *   data.doc          { id, name, scores, reasons, findings }
 *     scores:   { [dimId]: number | "NA" | "ERR" }
 *     reasons:  { [dimId]: string }
 *     findings: { [dimId]: [{ rule_number, verdict, description }, ...] }
 *
 * Markup contract: the container becomes a `.bi-stack.bi-ltr` host; the
 * mount appends one `.bi-card` per doc. Group-icon SVGs reference an
 * inline `<svg>` sprite at the top of <body> (#icon-purpose, etc.).
 */

(() => {
  function mount(containerSelector, data) {
    const container =
      typeof containerSelector === "string"
        ? document.querySelector(containerSelector)
        : containerSelector;
    if (!container) {
      console.error("PracticalProseBiCard.mount: container not found", containerSelector);
      return;
    }
    if (!data || !data.groups || !data.dimensions || !data.doc) {
      console.error("PracticalProseBiCard.mount: malformed data payload", data);
      return;
    }

    const groups = data.groups;
    const dims = data.dimensions;

    // Layout per Visual 9B: P/E/F left, R/G/J right (Reasoning pairs
    // row-for-row with Purpose at the top).
    const _byId = (id) => groups.find((g) => g.id === id);
    const biLeftGroups = ["P", "E", "F"].map(_byId).filter(Boolean);
    const biRightGroups = ["R", "G", "J"].map(_byId).filter(Boolean);

    // ─── DOM helper ──────────────────────────────────────────────────────
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

    // ─── Group icon ──────────────────────────────────────────────────────
    // Empty string → <use href="#icon-X"/> references the inlined sprite
    // at the top of <body>. Browsers block cross-file <use> references
    // when loaded via file://, so the sprite must be inlined.
    const ICON_SPRITE = "";
    function groupIcon(g) {
      const span = document.createElement("span");
      span.className = `grp-icon ${g.id.toLowerCase()}`;
      span.setAttribute("aria-hidden", "true");
      const symbol = g.label.toLowerCase();
      span.innerHTML =
        `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">` +
        `<use href="${ICON_SPRITE}#icon-${symbol}"/>` +
        `</svg>`;
      return span;
    }

    // ─── Group-average chip (9B's headerExtra) ───────────────────────────
    function groupAvgChip(g, doc) {
      const scores = dims
        .filter((d) => d.g === g.id)
        .map((d) => doc.scores[d.id])
        .filter((s) => typeof s === "number");
      if (scores.length === 0) return null;
      const avg = scores.reduce((a, b) => a + b, 0) / scores.length;
      return el("span", { class: "bi-group-avg" }, avg.toFixed(1));
    }

    // ─── Color helpers ──────────────────────────────────────────────────
    function _readScoreAlphaStep() {
      const v = getComputedStyle(document.documentElement)
        .getPropertyValue("--score-alpha-step")
        .trim();
      const n = parseFloat(v);
      return Number.isFinite(n) ? n : 0.14;
    }
    function dimColorMix(dimId, alpha) {
      const a = Math.max(0, Math.min(1, alpha));
      return `color-mix(in srgb, var(--dim-${dimId}) ${Math.round(
        a * 100,
      )}%, transparent)`;
    }
    function scoreColor(dimId, score) {
      const step = _readScoreAlphaStep();
      return dimColorMix(dimId, 1 - (5 - score) * step);
    }
    function segmentAlpha(segIdx) {
      const step = _readScoreAlphaStep();
      return 1 - (5 - segIdx) * step;
    }

    // ─── Per-row prep (shared between 9A and 9B variants) ───────────────
    function _biDimPrep(doc, d, side) {
      const s = doc.scores[d.id];
      const classes = ["bi-dim", side];
      if (typeof s !== "number" && s !== "ERR") classes.push("is-na");
      const entry = el("div", {
        class: classes.join(" "),
        style: { color: `var(--dim-${d.id})` },
        "data-tip-kind": "dim",
        "data-tip-key": d.id,
        "data-tip-doc": doc.id,
      });

      const name = el("span", { class: "bi-dim-name" }, d.label);
      const track = el("div", { class: "bi-bar-track" });
      const circle = el("div", { class: "bi-num-circle" });

      if (typeof s === "number") {
        for (let i = 1; i <= s; i++) {
          const seg = el("div", {
            class: "bi-bar-seg",
            "data-seg": String(i),
          });
          seg.style.background = dimColorMix(d.id, segmentAlpha(i));
          if (side === "left") {
            seg.style.right = `${(i - 1) * 20}%`;
          } else {
            seg.style.left = `${(i - 1) * 20}%`;
          }
          track.appendChild(seg);
        }
        circle.style.background = scoreColor(d.id, s);
        circle.textContent = s;
      } else {
        const fill = el("div", { class: "bi-bar-fill" });
        fill.style.width = "100%";
        if (s === "ERR") {
          fill.style.background = "var(--score-err-fill)";
          circle.textContent = "ERR";
          circle.classList.add("err");
        } else {
          fill.style.background = "var(--score-na-fill)";
          circle.textContent = "NA";
          circle.classList.add("na");
        }
        track.appendChild(fill);
      }

      for (let k = 1; k <= 4; k++) {
        const tick = el("div", { class: "bi-tick" });
        tick.style.left = `${side === "left" ? 100 - k * 20 : k * 20}%`;
        track.appendChild(tick);
      }

      return { entry, name, track, circle };
    }

    // ─── 9B per-row DOM ─────────────────────────────────────────────────
    function biDim9B(doc, d, side) {
      const { entry, name, track, circle } = _biDimPrep(doc, d, side);
      const head = el("div", { class: "bi-dim-head" }, name, circle);
      entry.appendChild(head);
      entry.appendChild(track);
      return entry;
    }

    // ─── Card composition ───────────────────────────────────────────────
    function biCard(doc, dimFn, headerExtra) {
      const card = el("div", { class: "bi-card" });
      card.appendChild(
        el("div", { class: "doc-kicker" }, "Practical Prose Evaluation"),
      );
      card.appendChild(el("div", { class: "doc-name" }, doc.name));

      const grid = el("div", { class: "bi-grid" });

      const left = el("div", { class: "bi-col left" });
      biLeftGroups.forEach((g) => {
        const header = el(
          "div",
          {
            class: "bi-group-header",
            style: {
              color: `var(--icon-color, var(--accent-${g.id.toLowerCase()}))`,
            },
            "data-tip-kind": "group",
            "data-tip-key": g.id,
          },
          groupIcon(g),
          el("span", { class: "label" }, g.label),
        );
        if (headerExtra) {
          const extra = headerExtra(g, doc);
          if (extra) header.appendChild(extra);
        }
        left.appendChild(header);
        dims
          .filter((d) => d.g === g.id)
          .forEach((d) => {
            left.appendChild(dimFn(doc, d, "left"));
          });
      });
      grid.appendChild(left);

      const right = el("div", { class: "bi-col right" });
      biRightGroups.forEach((g) => {
        const header = el(
          "div",
          {
            class: "bi-group-header",
            style: {
              color: `var(--icon-color, var(--accent-${g.id.toLowerCase()}))`,
            },
            "data-tip-kind": "group",
            "data-tip-key": g.id,
          },
          el("span", { class: "label" }, g.label),
          groupIcon(g),
        );
        if (headerExtra) {
          const extra = headerExtra(g, doc);
          if (extra) header.appendChild(extra);
        }
        right.appendChild(header);
        dims
          .filter((d) => d.g === g.id)
          .forEach((d) => {
            right.appendChild(dimFn(doc, d, "right"));
          });
      });
      grid.appendChild(right);

      card.appendChild(grid);
      return card;
    }

    // ─── Mount ──────────────────────────────────────────────────────────
    // Clear the container, wrap in the .bi-stack.bi-ltr scaffold the 9B
    // CSS keys off, and append one card per doc (today: one).
    container.innerHTML = "";
    const stack = el("div", { class: "bi-stack bi-ltr" });
    stack.appendChild(biCard(data.doc, biDim9B, groupAvgChip));
    container.appendChild(stack);

    // Expose biDim9B + helpers so the tip-panels component can mirror the
    // "focused dim" widget inside the Assessment panel using the same code
    // path that built the row in the card.
    return {
      biDim9B,
      _biDimPrep,
      el,
      groups,
      dims,
    };
  }

  globalThis.PracticalProseBiCard = Object.freeze({ mount });
})();

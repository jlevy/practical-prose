/*
 * Practical Prose — Visual 9B "bi-card" component.
 *
 * Renders the bidirectional-bars eval card. The functions are lifted
 * verbatim from tools/explorations/visual-design/dimension-visualizations.html
 * so any future change in the workbench flows straight through the sync
 * script.
 *
 * Two public entries:
 *
 *   PracticalProseBiCard.mount(containerSelector, data)
 *       Clear `containerSelector` and append a `.bi-stack.bi-ltr` with
 *       one `.bi-card` for `data.doc`. Returns the same API the
 *       workbench consumes (so the tip-panels component can mirror a
 *       dim row in the Assessment panel).
 *
 *   PracticalProseBiCard.makeApi(data)
 *       Returns the bound helpers (`biCard`, `biDim9B`, `_biDimPrep`,
 *       `groupIcon`, `groupAvgChip`, `dimColorMix`, `scoreColor`,
 *       `segmentAlpha`, `el`, `biLeftGroups`, `biRightGroups`) so
 *       another caller (e.g. the explorations workbench, which renders
 *       Visual 9A as well) can use the same code paths without
 *       duplication.
 *
 * Data contract (passed to mount/makeApi):
 *   data.groups       Array of { id, label } — 6 entries
 *   data.dimensions   Array of { id, label, g } — 20 entries
 *   data.rubric       Object keyed by dim id (used by tip-panels)
 *   data.doc          { id, name, scores, reasons, findings }
 *
 * Group-icon SVGs reference an inline `<svg>` sprite at the top of
 * `<body>` (#icon-purpose, etc.).
 */

(() => {
  function makeApi(data) {
    if (!data || !data.groups || !data.dimensions) {
      throw new Error("PracticalProseBiCard: data must include groups + dimensions");
    }
    const groups = data.groups;
    const dims = data.dimensions;

    // Layout per Visual 9B: P/E/F left, R/G/J right.
    const _byId = (id) => groups.find((g) => g.id === id);
    const biLeftGroups = ["P", "E", "F"].map(_byId).filter(Boolean);
    const biRightGroups = ["R", "G", "J"].map(_byId).filter(Boolean);

    // ─── DOM helper ─────────────────────────────────────────────────
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

    // ─── Group icon ─────────────────────────────────────────────────
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

    function groupAvgChip(g, doc) {
      const scores = dims
        .filter((d) => d.g === g.id)
        .map((d) => doc.scores[d.id])
        .filter((s) => typeof s === "number");
      if (scores.length === 0) return null;
      const avg = scores.reduce((a, b) => a + b, 0) / scores.length;
      return el("span", { class: "bi-group-avg" }, avg.toFixed(1));
    }

    // ─── Color helpers ──────────────────────────────────────────────
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

    // ─── Per-row prep (shared between 9A and 9B variants) ───────────
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

    function biDim9B(doc, d, side) {
      const { entry, name, track, circle } = _biDimPrep(doc, d, side);
      const head = el("div", { class: "bi-dim-head" }, name, circle);
      entry.appendChild(head);
      entry.appendChild(track);
      return entry;
    }

    function biCard(doc, dimFn = biDim9B, headerExtra = null) {
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

    return {
      // Helpers — for callers that want to compose their own DOM (e.g.
      // the workbench mounts Visual 9A using `biCard(doc, biDim, null)`
      // with a locally-defined `biDim` for the 9A row shape).
      el,
      groupIcon,
      groupAvgChip,
      _readScoreAlphaStep,
      dimColorMix,
      scoreColor,
      segmentAlpha,
      _biDimPrep,
      biDim9B,
      biCard,
      // Layout pre-computed from data.groups, for callers that need
      // the column assignments.
      biLeftGroups,
      biRightGroups,
      groups,
      dims,
    };
  }

  function mount(containerSelector, data) {
    const container =
      typeof containerSelector === "string"
        ? document.querySelector(containerSelector)
        : containerSelector;
    if (!container) {
      console.error("PracticalProseBiCard.mount: container not found", containerSelector);
      return null;
    }
    if (!data || !data.doc) {
      console.error("PracticalProseBiCard.mount: data.doc missing", data);
      return null;
    }
    const api = makeApi(data);
    container.innerHTML = "";
    const stack = api.el("div", { class: "bi-stack bi-ltr" });
    stack.appendChild(api.biCard(data.doc, api.biDim9B, api.groupAvgChip));
    container.appendChild(stack);
    return api;
  }

  globalThis.PracticalProseBiCard = Object.freeze({ mount, makeApi });
})();

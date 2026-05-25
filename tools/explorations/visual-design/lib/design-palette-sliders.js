/*
 * Design-tool palette tweaker — per-group H / S / L / Spread sliders.
 *
 * Design-only.  Only the exploration HTML pages use this; production
 * renderers should consume `tools/design-system/` instead.
 *
 * Plain script (not an ES module).  Attaches to globalThis:
 *
 *   window.PracticalProseDesignPaletteSliders = {
 *     mountPaletteSliders,
 *     exportDesignYAML,
 *     applyPalette,
 *   };
 *
 * Reads initial group values from `window.PracticalProseDesignSystem`
 * (loaded via design-system.generated.global.js), so the slider starting
 * positions always match the YAML.
 *
 * On every slider change the module rewrites `--accent-X`, `--surface-X`,
 * and `--dim-Xn` CSS custom properties on <html>.  These overrides win
 * over the static values in design-system.generated.css thanks to CSS
 * cascade (inline style > stylesheet).
 *
 * Markup contract:
 *
 *   <div id="palette-grid"></div>      ← container, sliders injected
 *
 * Pass either the element or `'#palette-grid'`.
 */

(() => {
  // ────────────── Setup ──────────────

  const isDarkMode = () =>
    globalThis.PracticalProseDesignColorControls?.isDarkMode() ||
    document.documentElement.getAttribute("data-theme") === "dark";

  /** Build the runtime per-group palette state from the YAML data. */
  function _initialPalette() {
    const ds = globalThis.PracticalProseDesignSystem;
    if (!ds) {
      throw new Error(
        "palette-sliders.js: window.PracticalProseDesignSystem missing. " +
          "Load design-system.generated.global.js first.",
      );
    }
    const palette = {};
    ds.designSystem.groups.forEach((g) => {
      const dims = ds.designSystem.dimensions.filter((d) => d.group === g.id);
      // Per-dim L offsets relative to the group ink L, in source order.
      // These are what the slider tweaks (everything else flows from H/S/L/spread).
      const _dimOffsetsLight = dims.map((d) =>
        d.color.light ? Math.round(_lOf(d.color.light) - g.ink && _lOf(g.ink.light)) : 0,
      );
      // We re-derive the offset from the resolved colors so we don't need
      // separate per-mode arrays.  L_dim_light - L_group_ink_light is the
      // offset; the same offset applied to L_group_ink_dark gives the dark
      // dim L (close to the YAML's recorded dark, within rounding).
      palette[g.id] = {
        h: g.h,
        s: g.s,
        spread: g.spread,
        lLight: _lOf(g.ink.light),
        lDark: _lOf(g.ink.dark),
        surfaceLLight: _lOf(g.surface.light),
        surfaceLDark: _lOf(g.surface.dark),
        dimOffsets: dims.map((d) => _lOf(d.color.light) - _lOf(g.ink.light)),
        dims: dims.map((d) => d.id),
      };
    });
    return palette;
  }

  /** Parse `hsl(H S% L%)` → just the L value. */
  function _lOf(hslStr) {
    const m = /hsl\(\s*[\d.]+\s+[\d.]+%\s+([\d.]+)%/.exec(hslStr);
    return m ? parseFloat(m[1]) : 0;
  }

  // ────────────── Apply ──────────────

  let palette = null;
  const refreshers = [];

  function applyPalette() {
    if (!palette) palette = _initialPalette();
    const dark = isDarkMode();
    const root = document.documentElement;
    Object.entries(palette).forEach(([gId, st]) => {
      const gL = dark ? st.lDark : st.lLight;
      const surfaceL = dark ? st.surfaceLDark : st.surfaceLLight;
      const cssId = gId.toLowerCase();
      root.style.setProperty(`--accent-${cssId}`, `hsl(${st.h} ${st.s}% ${gL}%)`);
      root.style.setProperty(`--surface-${cssId}`, `hsl(${st.h} ${st.s}% ${surfaceL}%)`);
      const n = st.dims.length;
      const step = n > 1 ? st.spread / (n - 1) : 0;
      st.dims.forEach((dimId, i) => {
        const hueOffset = (i - (n - 1) / 2) * step;
        const dimH = (((st.h + hueOffset) % 360) + 360) % 360;
        const dimL = Math.max(5, Math.min(95, gL + (st.dimOffsets[i] || 0)));
        root.style.setProperty(`--dim-${dimId}`, `hsl(${dimH.toFixed(1)} ${st.s}% ${dimL}%)`);
      });
    });
    refreshers.forEach((r) => {
      r();
    });
  }

  // ────────────── Mount ──────────────

  /**
   * Build the slider grid inside the given container.  Returns a teardown
   * function (call to remove all rows and stop listening to theme changes).
   *
   * @param {HTMLElement|string} container `<div id="palette-grid">` or selector
   */
  function mountPaletteSliders(container) {
    const grid = typeof container === "string" ? document.querySelector(container) : container;
    if (!grid) return () => {};
    if (!palette) palette = _initialPalette();

    const ds = globalThis.PracticalProseDesignSystem.designSystem;
    grid.innerHTML = "";
    refreshers.length = 0;

    ds.groups.forEach((g) => {
      const st = palette[g.id];
      if (!st) return;
      const row = _el("div", { class: "palette-row" });
      row.appendChild(
        _el("span", {
          class: "palette-swatch",
          style: `background: var(--accent-${g.id.toLowerCase()})`,
        }),
      );
      row.appendChild(
        _el(
          "span",
          {
            class: "palette-name",
            style: `color: var(--accent-${g.id.toLowerCase()})`,
          },
          g.label,
        ),
      );
      row.appendChild(_channel(g, st, "h", "Hue", 0, 359));
      row.appendChild(_channel(g, st, "s", "Sat", 0, 100));
      row.appendChild(_channel(g, st, "l", "L", 5, 95));
      row.appendChild(_spread(g, st));
      grid.appendChild(row);
    });

    // Reflect theme flips back into the sliders (L value swaps between
    // light/dark variants when the theme changes).
    const observer = new MutationObserver(applyPalette);
    observer.observe(document.documentElement, {
      attributes: true,
      attributeFilter: ["data-theme"],
    });

    applyPalette();

    return () => {
      observer.disconnect();
      grid.innerHTML = "";
      refreshers.length = 0;
    };
  }

  function _channel(_g, st, key, name, min, max) {
    const wrap = _el("div", { class: "palette-channel" });
    wrap.appendChild(_el("span", { class: "ch-name" }, name));
    const slider = _el("input", {
      type: "range",
      min: String(min),
      max: String(max),
      step: "1",
      class: `ch-${key}`,
    });
    const value = _el("span", { class: "ch-value" });
    function get() {
      if (key === "l") return isDarkMode() ? st.lDark : st.lLight;
      return st[key];
    }
    function set(v) {
      if (key === "l") {
        if (isDarkMode()) st.lDark = v;
        else st.lLight = v;
      } else {
        st[key] = v;
      }
    }
    function refresh() {
      const v = get();
      slider.value = String(v);
      value.textContent = v;
      const L = isDarkMode() ? st.lDark : st.lLight;
      if (key === "s") {
        slider.style.setProperty(
          "--track-gradient",
          `linear-gradient(to right, hsl(${st.h} 0% ${L}%), hsl(${st.h} 100% ${L}%))`,
        );
      } else if (key === "l") {
        slider.style.setProperty(
          "--track-gradient",
          `linear-gradient(to right, hsl(${st.h} ${st.s}% 0%), hsl(${st.h} ${st.s}% 50%), hsl(${st.h} ${st.s}% 100%))`,
        );
      }
      let thumbColor;
      if (key === "h") thumbColor = `hsl(${v} 100% 50%)`;
      else if (key === "s") thumbColor = `hsl(${st.h} ${v}% ${L}%)`;
      else thumbColor = `hsl(${st.h} ${st.s}% ${v}%)`;
      slider.style.setProperty("--thumb-color", thumbColor);
    }
    slider.addEventListener("input", () => {
      set(+slider.value);
      value.textContent = slider.value;
      applyPalette();
    });
    refreshers.push(refresh);
    wrap.appendChild(slider);
    wrap.appendChild(value);
    return wrap;
  }

  function _spread(_g, st) {
    const wrap = _el("div", { class: "palette-channel" });
    wrap.appendChild(_el("span", { class: "ch-name" }, "Spread"));
    const input = _el("input", {
      type: "number",
      min: "0",
      max: "60",
      step: "1",
      value: String(st.spread),
      class: "ch-spread-num",
    });
    input.addEventListener("input", () => {
      st.spread = +input.value || 0;
      applyPalette();
    });
    // No refresher — the input IS the source of truth for spread; resetting
    // input.value while the user is mid-type clobbers keystrokes.
    wrap.appendChild(input);
    return wrap;
  }

  // ────────────── Export YAML snippet ──────────────

  /**
   * Serialize the current slider state to a YAML snippet matching the
   * design-system.yaml shape, leading with a schema comment.  Pastes into
   * design-system.yaml as the new canonical values.
   */
  function exportDesignYAML() {
    if (!palette) palette = _initialPalette();
    const ds = globalThis.PracticalProseDesignSystem.designSystem;
    const lines = [
      "# Snapshot from the palette sliders.",
      "# Paste into tools/design-system/design-system.yaml under `groups:` to",
      "# adopt these values, then re-run generate.py to refresh the artifacts.",
      "",
      "groups:",
    ];
    ds.groups.forEach((g) => {
      const st = palette[g.id];
      lines.push(
        `  - id: ${g.id}\n` +
          `    label: ${g.label}\n` +
          `    h: ${st.h}\n` +
          `    s: ${st.s}\n` +
          `    spread: ${st.spread}\n` +
          `    ink:     { light: ${st.lLight}, dark: ${st.lDark} }\n` +
          `    surface: { light: ${st.surfaceLLight}, dark: ${st.surfaceLDark} }\n` +
          `    icon: ${g.icon}\n` +
          `    sense: ${g.sense}`,
      );
    });
    return lines.join("\n");
  }

  // ────────────── DOM helper ──────────────

  function _el(tag, attrs, text) {
    const e = document.createElement(tag);
    if (attrs) {
      for (const [k, v] of Object.entries(attrs)) {
        if (v == null) continue;
        if (k === "style" && typeof v === "object") {
          Object.assign(e.style, v);
        } else {
          e.setAttribute(k, v);
        }
      }
    }
    if (text != null) e.textContent = text;
    return e;
  }

  // ────────────── Export ──────────────

  globalThis.PracticalProseDesignPaletteSliders = Object.freeze({
    mountPaletteSliders,
    exportDesignYAML,
    applyPalette,
  });
})();

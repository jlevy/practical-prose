/*
 * Design-tool font UI controls — sans + serif chooser.
 *
 * Design-only.  Only the exploration HTML pages use this; production
 * renderers should consume `tools/design-system/` instead.
 *
 * Plain script (not an ES module) so it works from file:// without a
 * local server.  Attaches to globalThis:
 *
 *   window.PracticalProseDesignFontControls = {
 *     mountFontChooser, fontStacks, fontLabels,
 *   };
 *
 * Markup contract — two <select> elements (any ids):
 *
 *   <select id="font-sans-select"></select>
 *   <select id="font-serif-select"></select>
 *
 * Pass `{ sans, serif }` (elements or selectors) to `mountFontChooser`.
 * The selects are populated on first mount; re-mounting won't duplicate
 * options.
 *
 * On change, updates `--font-sans` / `--font-serif` on <html>.  All page
 * styles should read those tokens.
 */

(() => {
  // Source Sans 3 + PT Serif are webfonts; the host page must load the
  // matching @font-face declarations (see dimension-visualizations.html).
  // PT Serif's quote-mark glyphs sit too high — the "LocalPunct" front
  // of the stack overrides ASCII + curly quotes with local Georgia.
  const fontStacks = {
    sans: {
      sourcesans:
        '"Source Sans 3 Variable", -apple-system, BlinkMacSystemFont, "Inter", "Helvetica Neue", Arial, sans-serif',
      ibmplex:
        '"IBM Plex Sans Variable", -apple-system, BlinkMacSystemFont, "Helvetica Neue", Arial, sans-serif',
      hanken:
        '"Hanken Grotesk Variable", -apple-system, BlinkMacSystemFont, "Helvetica Neue", Arial, sans-serif',
      inter: '"Inter Variable", "Inter", -apple-system, BlinkMacSystemFont, sans-serif',
      system: '-apple-system, BlinkMacSystemFont, "Inter", "Helvetica Neue", Arial, sans-serif',
      helvetica: '"Helvetica Neue", Helvetica, Arial, sans-serif',
    },
    serif: {
      notoserif: '"Noto Serif Variable", "Iowan Old Style", "Charter", Georgia, serif',
      sourceserif: '"Source Serif 4 Variable", "Iowan Old Style", "Charter", Georgia, serif',
      ptserif: '"LocalPunct", "PT Serif", "Iowan Old Style", "Charter", Georgia, serif',
      charissil: '"Charis SIL", "Iowan Old Style", "Charter", Georgia, serif',
      gelasio: '"Gelasio", "Iowan Old Style", "Charter", Georgia, serif',
      spectral: '"Spectral", "Iowan Old Style", "Charter", Georgia, serif',
      newsreader: '"Newsreader Variable", "Iowan Old Style", "Charter", Georgia, serif',
      crimsonpro: '"Crimson Pro Variable", "Iowan Old Style", "Charter", Georgia, serif',
      stixtwo: '"STIX Two Text Variable", "Iowan Old Style", "Charter", Georgia, serif',
      vollkorn: '"Vollkorn Variable", "Iowan Old Style", "Charter", Georgia, serif',
      iowan: '"Iowan Old Style", "Charter", "Hoefler Text", Georgia, serif',
      georgia: 'Georgia, "Times New Roman", serif',
      times: '"Times New Roman", Times, serif',
      ui: "ui-serif, Georgia, serif",
    },
  };

  // Source suffix in the label tells the user where each font comes from.
  // "Fontsource" → loaded via @font-face from cdn.jsdelivr.net/fontsource.
  // "system"     → relies on the OS / browser default stack (no webfont
  //                fetched).  Inter and Helvetica Neue may or may not be
  //                installed locally; if not, the rest of the stack handles
  //                the fallback.
  const fontLabels = {
    sans: {
      sourcesans: "Source Sans 3 (default, Fontsource)",
      ibmplex: "IBM Plex Sans (Fontsource)",
      hanken: "Hanken Grotesk (Fontsource)",
      inter: "Inter (Fontsource)",
      system: "System (system)",
      helvetica: "Helvetica Neue (system)",
    },
    serif: {
      notoserif: "Noto Serif (default, Fontsource)",
      sourceserif: "Source Serif 4 (Fontsource)",
      ptserif: "PT Serif (Fontsource)",
      charissil: "Charis SIL (Fontsource)",
      gelasio: "Gelasio (Fontsource)",
      spectral: "Spectral (Fontsource)",
      newsreader: "Newsreader (Fontsource)",
      crimsonpro: "Crimson Pro (Fontsource)",
      stixtwo: "STIX Two Text (Fontsource)",
      vollkorn: "Vollkorn (Fontsource)",
      iowan: "Iowan / Charter (system)",
      georgia: "Georgia (system)",
      times: "Times (system)",
      ui: "System Serif (system)",
    },
  };

  /**
   * Populate and wire two <select> elements that switch `--font-sans` /
   * `--font-serif` on <html>.
   *
   * @param {{ sans: HTMLSelectElement|string, serif: HTMLSelectElement|string }} selects
   */
  function mountFontChooser(selects) {
    const html = document.documentElement;
    ["sans", "serif"].forEach((role) => {
      const sel = _resolve(selects[role]);
      if (!sel) return;
      if (sel.options.length === 0) {
        Object.entries(fontLabels[role]).forEach(([key, label]) => {
          const opt = document.createElement("option");
          opt.value = key;
          opt.textContent = label;
          sel.appendChild(opt);
        });
      }
      sel.addEventListener("change", () => {
        html.style.setProperty(`--font-${role}`, fontStacks[role][sel.value]);
      });
    });
  }

  /**
   * Wire numeric inputs (sliders or `<input type=number>`) to CSS
   * variables on <html>.  Each entry specifies its target var name and
   * an optional unit suffix appended to the value (eg. "px" for size
   * inputs); weight sliders pass no unit so the value is unitless and
   * usable in `font-weight`.
   *
   * @param {Array<{
   *   varName: string,
   *   slider: HTMLInputElement|string,
   *   readout?: HTMLElement|string,
   *   unit?: string,
   * }>} entries
   */
  function mountWeightSliders(entries) {
    const html = document.documentElement;
    entries.forEach(({ varName, slider, readout, unit = "" }) => {
      const sliderEl = _resolve(slider);
      if (!sliderEl) return;
      const readoutEl = readout ? _resolve(readout) : null;
      const apply = () => {
        html.style.setProperty(`--${varName}`, sliderEl.value + unit);
        if (readoutEl) readoutEl.textContent = sliderEl.value;
      };
      sliderEl.addEventListener("input", apply);
      apply();
    });
  }

  function _resolve(elOrSelector) {
    if (!elOrSelector) return null;
    if (typeof elOrSelector === "string") return document.querySelector(elOrSelector);
    return elOrSelector;
  }

  globalThis.PracticalProseDesignFontControls = Object.freeze({
    mountFontChooser,
    mountWeightSliders,
    fontStacks,
    fontLabels,
  });
})();

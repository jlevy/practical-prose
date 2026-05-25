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

(function () {
  "use strict";

  const fontStacks = {
    sans: {
      system:
        '-apple-system, BlinkMacSystemFont, "Inter", "Helvetica Neue", Arial, sans-serif',
      inter: '"Inter", -apple-system, BlinkMacSystemFont, sans-serif',
      helvetica: '"Helvetica Neue", Helvetica, Arial, sans-serif',
      arial: "Arial, Helvetica, sans-serif",
      verdana: "Verdana, Geneva, sans-serif",
      tahoma: "Tahoma, Geneva, sans-serif",
    },
    serif: {
      iowan: '"Iowan Old Style", "Charter", "Hoefler Text", Georgia, serif',
      georgia: 'Georgia, "Times New Roman", serif',
      times: '"Times New Roman", Times, serif',
      garamond: 'Garamond, "Times New Roman", serif',
      palatino: 'Palatino, "Palatino Linotype", "Book Antiqua", serif',
      ui: "ui-serif, Georgia, serif",
    },
  };

  const fontLabels = {
    sans: {
      system: "System (default)",
      inter: "Inter",
      helvetica: "Helvetica Neue",
      arial: "Arial",
      verdana: "Verdana",
      tahoma: "Tahoma",
    },
    serif: {
      iowan: "Iowan / Charter (default)",
      georgia: "Georgia",
      times: "Times",
      garamond: "Garamond",
      palatino: "Palatino",
      ui: "System Serif",
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

  function _resolve(elOrSelector) {
    if (!elOrSelector) return null;
    if (typeof elOrSelector === "string")
      return document.querySelector(elOrSelector);
    return elOrSelector;
  }

  globalThis.PracticalProseDesignFontControls = Object.freeze({
    mountFontChooser,
    fontStacks,
    fontLabels,
  });
})();

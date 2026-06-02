/*
 * Design-tool color UI controls — surface-tone toggle.
 *
 * Workbench-only. `mountThemeToggle` (Auto / Light / Dark) now lives in
 * tools/render-components/theme-toggle/theme-toggle.js (shared with the
 * pprose render pipeline). This file keeps the surface-tone toggle
 * (White / Paper / Gray), which is exploration-only — the production
 * renderer always uses the white surface.
 *
 * Plain script (not an ES module) so it works from file:// without a
 * local server. Extends the shared `globalThis.PracticalProseDesignColorControls`
 * namespace with one extra entry:
 *
 *   PracticalProseDesignColorControls.mountSurfaceToggle(container, opts?)
 *
 * Markup contract:
 *
 *   <div class="surface-toggle">
 *     <button data-surface-set="white">White</button>
 *     <button data-surface-set="paper">Paper</button>
 *     <button data-surface-set="gray">Gray</button>
 *   </div>
 */

(() => {
  /**
   * Orthogonal to the theme toggle. Switches a `data-surface` attribute on
   * <html> that overrides surface-only tokens (bg, card, border). Each
   * surface scheme has its own light AND dark values; flipping surface
   * doesn't change theme.
   *
   * @param {HTMLElement|string} container
   * @param {{ default?: 'white'|'paper'|'gray' }} [opts]
   */
  function mountSurfaceToggle(container, opts) {
    const root = _resolve(container);
    if (!root) return;
    const html = document.documentElement;
    const buttons = root.querySelectorAll("button[data-surface-set]");
    function apply(scheme) {
      if (scheme === "paper") html.removeAttribute("data-surface");
      else html.setAttribute("data-surface", scheme);
      buttons.forEach((b) => {
        b.classList.toggle("active", b.dataset.surfaceSet === scheme);
      });
    }
    buttons.forEach((b) => {
      b.addEventListener("click", () => apply(b.dataset.surfaceSet));
    });
    apply(opts?.default || "white");
  }

  function _resolve(elOrSelector) {
    if (!elOrSelector) return null;
    if (typeof elOrSelector === "string") return document.querySelector(elOrSelector);
    return elOrSelector;
  }

  // Extend the shared theme-toggle namespace with the workbench-only
  // mountSurfaceToggle. Load order doesn't matter — whichever script runs
  // first creates the namespace; the other adds its entry.
  globalThis.PracticalProseDesignColorControls = globalThis.PracticalProseDesignColorControls || {};
  const ns = globalThis.PracticalProseDesignColorControls;
  ns.mountSurfaceToggle = mountSurfaceToggle;
})();

/*
 * Design-tool color UI controls — theme toggle + surface-tone toggle.
 *
 * Design-only.  Only the exploration HTML pages use this; production
 * renderers should consume `tools/design-system/` instead.
 *
 * Plain script (not an ES module) so it works from file:// without a
 * local server.  Attaches to globalThis:
 *
 *   window.PracticalProseDesignColorControls = {
 *     mountThemeToggle, mountSurfaceToggle, isDarkMode,
 *   };
 *
 * Markup contracts:
 *
 *   Theme toggle   →  <div class="theme-toggle">
 *                       <button data-theme-set="auto">Auto</button>
 *                       <button data-theme-set="light">Light</button>
 *                       <button data-theme-set="dark">Dark</button>
 *                     </div>
 *
 *   Surface tone  →  <div class="surface-toggle">
 *                       <button data-surface-set="white">White</button>
 *                       <button data-surface-set="paper">Paper</button>
 *                       <button data-surface-set="gray">Gray</button>
 *                     </div>
 *
 * The DOM contracts match the original viz page so existing markup keeps
 * working unchanged.
 */

(function () {
  "use strict";

  // ────────────── Theme toggle ──────────────

  /**
   * Wire up a three-button theme toggle (Auto / Light / Dark).
   *
   * Sets `data-theme` and `data-theme-mode` on <html>.  In Auto mode the
   * resolved theme flips with the system preference.  CSS keys off
   * `data-theme` for the explicit override and the
   * `prefers-color-scheme: dark` media query for the auto fallback.
   *
   * @param {HTMLElement|string} container root element or selector
   * @param {{ default?: 'auto'|'light'|'dark' }} [opts]
   */
  function mountThemeToggle(container, opts) {
    const root = _resolve(container);
    if (!root) return;
    const html = document.documentElement;
    const mq = matchMedia("(prefers-color-scheme: dark)");
    const buttons = root.querySelectorAll("button[data-theme-set]");
    function apply(mode) {
      if (mode === "auto") {
        html.setAttribute("data-theme", mq.matches ? "dark" : "light");
        html.setAttribute("data-theme-mode", "auto");
      } else {
        html.setAttribute("data-theme", mode);
        html.setAttribute("data-theme-mode", mode);
      }
      const active = html.getAttribute("data-theme-mode");
      buttons.forEach((b) =>
        b.classList.toggle("active", b.dataset.themeSet === active),
      );
    }
    mq.addEventListener("change", () => {
      if (html.getAttribute("data-theme-mode") === "auto") apply("auto");
    });
    buttons.forEach((b) =>
      b.addEventListener("click", () => apply(b.dataset.themeSet)),
    );
    apply((opts && opts.default) || "auto");
  }

  /** Current resolved theme reads `data-theme` on <html>. */
  function isDarkMode() {
    return document.documentElement.getAttribute("data-theme") === "dark";
  }

  // ────────────── Surface-tone toggle ──────────────

  /**
   * Orthogonal to the theme toggle.  Switches a `data-surface` attribute on
   * <html> that overrides surface-only tokens (bg, card, border).  Each
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
      buttons.forEach((b) =>
        b.classList.toggle("active", b.dataset.surfaceSet === scheme),
      );
    }
    buttons.forEach((b) =>
      b.addEventListener("click", () => apply(b.dataset.surfaceSet)),
    );
    apply((opts && opts.default) || "white");
  }

  // ────────────── Helpers ──────────────

  function _resolve(elOrSelector) {
    if (!elOrSelector) return null;
    if (typeof elOrSelector === "string")
      return document.querySelector(elOrSelector);
    return elOrSelector;
  }

  // ────────────── Export ──────────────

  globalThis.PracticalProseDesignColorControls = Object.freeze({
    mountThemeToggle,
    mountSurfaceToggle,
    isDarkMode,
  });
})();

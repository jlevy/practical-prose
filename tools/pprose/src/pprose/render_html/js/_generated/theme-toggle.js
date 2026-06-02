/*
 * Practical Prose — three-button Auto / Light / Dark theme toggle.
 *
 * Lifted from tools/explorations/visual-design/lib/design-color-controls.js
 * (the `mountThemeToggle` half; `mountSurfaceToggle` stays in the
 * workbench's local lib/ since `pprose render` only uses the white
 * surface).
 *
 * Sets `data-theme` and `data-theme-mode` on `<html>`. In Auto mode the
 * resolved theme tracks `prefers-color-scheme`. CSS keys off `data-theme`
 * for the explicit override and `prefers-color-scheme: dark` for the
 * auto fallback.
 *
 * Public API:
 *     PracticalProseDesignColorControls.mountThemeToggle(container, opts?)
 *     PracticalProseDesignColorControls.isDarkMode()
 *
 * Markup contract:
 *     <div class="theme-toggle" role="group" aria-label="Color theme">
 *       <button data-theme-set="auto">Auto</button>
 *       <button data-theme-set="light">Light</button>
 *       <button data-theme-set="dark">Dark</button>
 *     </div>
 */

(() => {
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
      buttons.forEach((b) => {
        b.classList.toggle("active", b.dataset.themeSet === active);
      });
    }
    mq.addEventListener("change", () => {
      if (html.getAttribute("data-theme-mode") === "auto") apply("auto");
    });
    buttons.forEach((b) => {
      b.addEventListener("click", () => apply(b.dataset.themeSet));
    });
    apply(opts?.default || "auto");
  }

  function isDarkMode() {
    return document.documentElement.getAttribute("data-theme") === "dark";
  }

  function _resolve(elOrSelector) {
    if (!elOrSelector) return null;
    if (typeof elOrSelector === "string") return document.querySelector(elOrSelector);
    return elOrSelector;
  }

  // Extend rather than replace, so a same-page workbench can add its own
  // companion entries (e.g. `mountSurfaceToggle`) without load-order
  // sensitivity.
  globalThis.PracticalProseDesignColorControls = globalThis.PracticalProseDesignColorControls || {};
  const ns = globalThis.PracticalProseDesignColorControls;
  ns.mountThemeToggle = mountThemeToggle;
  ns.isDarkMode = isDarkMode;
})();

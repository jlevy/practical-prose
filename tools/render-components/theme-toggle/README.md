---
title: theme-toggle render component
description: Three-button Auto / Light / Dark theme toggle
---
# theme-toggle

A pill-shaped three-button toggle that controls `data-theme` and
`data-theme-mode` on `<html>`. Auto tracks `prefers-color-scheme`; Light
and Dark are explicit overrides.

## Public API

```javascript
PracticalProseDesignColorControls.mountThemeToggle(container, opts?);
PracticalProseDesignColorControls.isDarkMode();
```

`opts.default` is `"auto" | "light" | "dark"`. Defaults to `"auto"`.

## Markup partial

[theme-toggle.html.jinja](theme-toggle.html.jinja) provides the three-button
markup. Include it via `{% include 'theme-toggle.html.jinja' %}` in any
Jinja template that needs the toggle.

## Print behavior

The component carries no print rules. Surfaces that need to hide the toggle
in printed output should include something like:

```css
@media print {
  .theme-toggle { display: none !important; }
}
```

in their own print stylesheet.

## Source

JS is the `mountThemeToggle` half of
[tools/explorations/visual-design/lib/design-color-controls.js](../../explorations/visual-design/lib/design-color-controls.js).
The `mountSurfaceToggle` half stays in the workbench's local `lib/` since
the `pprose render` surface only uses the white surface scheme.

CSS lifted from the explorations file's `<style>` block.

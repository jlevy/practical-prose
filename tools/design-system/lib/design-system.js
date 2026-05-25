/**
 * Typed JS API for the Practical Prose design system.
 *
 * Imports the auto-generated payload, validates it with Zod (defensive — catches
 * a hand-edited generated file), and re-exports it under stable names.  This is
 * the entry point that HTML consumers should import from.
 *
 *   import { designSystem, groupsById, dimensionsById, scoresByLevel }
 *     from "../../design-system/lib/design-system.js";
 *
 * The Zod schema here mirrors `schema.py` (Pydantic).  Keep the two in sync
 * when adding fields.
 *
 * Source of truth: ../design-system.yaml
 * Regenerate the _generated/* files with: uv run --script tools/design-system/generate.py
 */

import { z } from "https://esm.sh/zod@3.23.8";
import {
  designSystem as _designSystem,
  dimensionsById as _dimensionsById,
  groupsById as _groupsById,
  scoresByLevel as _scoresByLevel,
} from "../_generated/design_system.js";

// ────────────── Schema ──────────────

// Modern space-separated HSL, with optional /alpha. No commas, no hex.
const HSL = z
  .string()
  .regex(
    /^hsl\(\s*\d+(?:\.\d+)?\s+\d+(?:\.\d+)?%\s+\d+(?:\.\d+)?%(?:\s*\/\s*\d*(?:\.\d+)?)?\s*\)$/,
  );

const LightDarkHsl = z.object({ light: HSL, dark: HSL }).strict();

const Surfaces = z
  .object({
    bg: LightDarkHsl,
    fg: LightDarkHsl,
    muted: LightDarkHsl,
    card: LightDarkHsl,
    border: LightDarkHsl,
    rule: LightDarkHsl,
  })
  .strict();

const GroupId = z.enum(["P", "E", "F", "R", "G", "J"]);

const Group = z
  .object({
    id: GroupId,
    label: z.string().min(1),
    h: z.number().min(0).max(360),
    s: z.number().min(0).max(100),
    spread: z.number().min(0).max(60),
    // The resolved generated JS expands ink/surface to full HSL strings
    // (the YAML stores L only — resolution happens in the generator).
    ink: LightDarkHsl,
    text: LightDarkHsl,
    surface: LightDarkHsl,
    icon: z.string().regex(/^[a-z0-9_-]+:[a-z0-9_-]+$/),
    sense: z.string().min(1),
  })
  .strict();

const Dimension = z
  .object({
    id: z.string().regex(/^[PEFRGJ]\d+$/),
    label: z.string().min(1),
    short: z.string().min(1).max(10),
    group: GroupId,
    h_offset: z.number().min(-30).max(30),
    color: LightDarkHsl,
  })
  .strict();

const ScoreLevel = z.enum(["0", "1", "2", "3", "4", "5", "NA", "ERR"]);

const Score = z
  .object({
    level: ScoreLevel,
    color: LightDarkHsl,
    weight: z.number().int().min(100).max(900),
    opacity: z.number().min(0).max(1).optional(),
  })
  .strict();

export const DesignSystemSchema = z
  .object({
    version: z.number().int().min(1),
    surfaces: Surfaces,
    groups: z.array(Group),
    dimensions: z.array(Dimension),
    scores: z.array(Score),
  })
  .strict();

// ────────────── Validate-at-load ──────────────

// Defensive: if the generated file has been hand-edited and no longer matches
// the schema, we fail fast at import rather than misrendering at runtime.
DesignSystemSchema.parse(_designSystem);

// ────────────── Exports ──────────────

/** The full resolved design system payload. */
export const designSystem = _designSystem;

/** Lookup tables keyed by id. */
export const groupsById = _groupsById;
export const dimensionsById = _dimensionsById;
export const scoresByLevel = _scoresByLevel;

/**
 * Dimensions grouped by their parent group, in source order.
 * Convenience for consumers that walk the rubric tree-wise.
 */
export const dimensionsByGroup = Object.freeze(
  Object.fromEntries(
    designSystem.groups.map((g) => [g.id, designSystem.dimensions.filter((d) => d.group === g.id)]),
  ),
);

/**
 * Resolve a color triple ({light, dark}) for a given theme mode.
 * @param {{light: string, dark: string}} pair
 * @param {"light"|"dark"} mode
 */
export function pickByMode(pair, mode) {
  return mode === "dark" ? pair.dark : pair.light;
}

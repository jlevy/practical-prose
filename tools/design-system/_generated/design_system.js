/* AUTO-GENERATED from tools/design-system/design-system.yaml — do not edit by hand.
Regenerate with: uv run --script tools/design-system/generate.py */

/** The full resolved Practical Prose design system. */
export const designSystem = Object.freeze({
  "version": 1,
  "surfaces": {
    "bg": {
      "light": "hsl(0 0% 98%)",
      "dark": "hsl(0 0% 8%)"
    },
    "fg": {
      "light": "hsl(30 12% 10%)",
      "dark": "hsl(40 25% 88%)"
    },
    "muted": {
      "light": "hsl(40 0% 28%)",
      "dark": "hsl(40 11% 53%)"
    },
    "card": {
      "light": "hsl(0 0% 100%)",
      "dark": "hsl(0 0% 12%)"
    },
    "border": {
      "light": "hsl(0 0% 88%)",
      "dark": "hsl(0 0% 18%)"
    },
    "rule": {
      "light": "hsl(30 12% 10%)",
      "dark": "hsl(40 25% 88%)"
    }
  },
  "tones": {
    "icon": "hsl(40 0% 28%)",
    "dim_label": "hsl(40 0% 28%)",
    "na": "hsl(220 10% 78%)",
    "na_label": "hsl(40 0% 60%)"
  },
  "groups": [
    {
      "id": "P",
      "label": "Purpose",
      "spread": 22.0,
      "ink": {
        "light": "hsl(214 19% 73%)",
        "dark": "hsl(214 19% 27%)"
      },
      "surface": {
        "light": "hsl(214 19% 92%)",
        "dark": "hsl(214 19% 18%)"
      },
      "icon": "mdi:compass-rose",
      "sense": "orientation toward the reader's task"
    },
    {
      "id": "E",
      "label": "Expression",
      "spread": 30.0,
      "ink": {
        "light": "hsl(134 19% 73%)",
        "dark": "hsl(134 19% 27%)"
      },
      "surface": {
        "light": "hsl(134 19% 92%)",
        "dark": "hsl(134 19% 18%)"
      },
      "icon": "mdi:quill",
      "sense": "language, surface form"
    },
    {
      "id": "F",
      "label": "Form",
      "spread": 30.0,
      "ink": {
        "light": "hsl(58 19% 73%)",
        "dark": "hsl(58 19% 27%)"
      },
      "surface": {
        "light": "hsl(58 19% 92%)",
        "dark": "hsl(58 19% 18%)"
      },
      "icon": "mdi:scroll",
      "sense": "the document as a structured artifact"
    },
    {
      "id": "R",
      "label": "Reasoning",
      "spread": 35.0,
      "ink": {
        "light": "hsl(0 19% 73%)",
        "dark": "hsl(0 19% 27%)"
      },
      "surface": {
        "light": "hsl(0 19% 92%)",
        "dark": "hsl(0 19% 18%)"
      },
      "icon": "mdi:ruler",
      "sense": "inference, measurement, rigor"
    },
    {
      "id": "G",
      "label": "Grounding",
      "spread": 30.0,
      "ink": {
        "light": "hsl(195 17% 73%)",
        "dark": "hsl(195 17% 27%)"
      },
      "surface": {
        "light": "hsl(195 17% 92%)",
        "dark": "hsl(195 17% 16%)"
      },
      "icon": "mdi:anchor",
      "sense": "tied to sources and facts"
    },
    {
      "id": "J",
      "label": "Judgment",
      "spread": 22.0,
      "ink": {
        "light": "hsl(294 19% 73%)",
        "dark": "hsl(294 19% 27%)"
      },
      "surface": {
        "light": "hsl(294 19% 92%)",
        "dark": "hsl(294 19% 18%)"
      },
      "icon": "mdi:scale-balance",
      "sense": "weighing claims, calibration"
    }
  ],
  "dimensions": [
    {
      "id": "P1",
      "label": "Suitability",
      "short": "Suit",
      "group": "P",
      "h_offset": -11.0,
      "color": {
        "light": "hsl(203 19% 40%)",
        "dark": "hsl(203 19% 65%)"
      }
    },
    {
      "id": "P2",
      "label": "Scope",
      "short": "Scope",
      "group": "P",
      "h_offset": -3.7,
      "color": {
        "light": "hsl(210.3 19% 37%)",
        "dark": "hsl(210.3 19% 62%)"
      }
    },
    {
      "id": "P3",
      "label": "Breadth",
      "short": "Brd",
      "group": "P",
      "h_offset": 3.7,
      "color": {
        "light": "hsl(217.7 19% 34%)",
        "dark": "hsl(217.7 19% 59%)"
      }
    },
    {
      "id": "P4",
      "label": "Depth",
      "short": "Dep",
      "group": "P",
      "h_offset": 11.0,
      "color": {
        "light": "hsl(225 19% 31%)",
        "dark": "hsl(225 19% 56%)"
      }
    },
    {
      "id": "E1",
      "label": "Clarity",
      "short": "Clar",
      "group": "E",
      "h_offset": -15.0,
      "color": {
        "light": "hsl(119 19% 35%)",
        "dark": "hsl(119 19% 68%)"
      }
    },
    {
      "id": "E2",
      "label": "Coherence",
      "short": "Coh",
      "group": "E",
      "h_offset": 0.0,
      "color": {
        "light": "hsl(134 19% 32%)",
        "dark": "hsl(134 19% 66%)"
      }
    },
    {
      "id": "E3",
      "label": "Concision",
      "short": "Conc",
      "group": "E",
      "h_offset": 15.0,
      "color": {
        "light": "hsl(149 19% 30%)",
        "dark": "hsl(149 19% 64%)"
      }
    },
    {
      "id": "F1",
      "label": "Organization",
      "short": "Org",
      "group": "F",
      "h_offset": -15.0,
      "color": {
        "light": "hsl(43 19% 38%)",
        "dark": "hsl(43 19% 64%)"
      }
    },
    {
      "id": "F2",
      "label": "Consistency",
      "short": "Cons",
      "group": "F",
      "h_offset": 0.0,
      "color": {
        "light": "hsl(58 19% 35%)",
        "dark": "hsl(58 19% 61%)"
      }
    },
    {
      "id": "F3",
      "label": "Formatting",
      "short": "Fmt",
      "group": "F",
      "h_offset": 15.0,
      "color": {
        "light": "hsl(73 19% 32%)",
        "dark": "hsl(73 19% 58%)"
      }
    },
    {
      "id": "R1",
      "label": "Discipline",
      "short": "Disc",
      "group": "R",
      "h_offset": -17.5,
      "color": {
        "light": "hsl(342.5 19% 40%)",
        "dark": "hsl(342.5 19% 68%)"
      }
    },
    {
      "id": "R2",
      "label": "Soundness",
      "short": "Snd",
      "group": "R",
      "h_offset": -5.8,
      "color": {
        "light": "hsl(354.2 19% 37%)",
        "dark": "hsl(354.2 19% 65%)"
      }
    },
    {
      "id": "R3",
      "label": "Precision",
      "short": "Prec",
      "group": "R",
      "h_offset": 5.8,
      "color": {
        "light": "hsl(5.8 19% 34%)",
        "dark": "hsl(5.8 19% 62%)"
      }
    },
    {
      "id": "R4",
      "label": "Parsimony",
      "short": "Pars",
      "group": "R",
      "h_offset": 17.5,
      "color": {
        "light": "hsl(17.5 19% 31%)",
        "dark": "hsl(17.5 19% 59%)"
      }
    },
    {
      "id": "G1",
      "label": "Verifiability",
      "short": "Ver",
      "group": "G",
      "h_offset": -15.0,
      "color": {
        "light": "hsl(180 17% 32%)",
        "dark": "hsl(180 17% 62%)"
      }
    },
    {
      "id": "G2",
      "label": "Factuality",
      "short": "Fact",
      "group": "G",
      "h_offset": 0.0,
      "color": {
        "light": "hsl(195 17% 29%)",
        "dark": "hsl(195 17% 58%)"
      }
    },
    {
      "id": "G3",
      "label": "Relevance",
      "short": "Rel",
      "group": "G",
      "h_offset": 15.0,
      "color": {
        "light": "hsl(210 17% 26%)",
        "dark": "hsl(210 17% 54%)"
      }
    },
    {
      "id": "J1",
      "label": "Calibration",
      "short": "Cal",
      "group": "J",
      "h_offset": -11.0,
      "color": {
        "light": "hsl(283 19% 42%)",
        "dark": "hsl(283 19% 70%)"
      }
    },
    {
      "id": "J2",
      "label": "Fairness",
      "short": "Fair",
      "group": "J",
      "h_offset": 0.0,
      "color": {
        "light": "hsl(294 19% 39%)",
        "dark": "hsl(294 19% 67%)"
      }
    },
    {
      "id": "J3",
      "label": "Robustness",
      "short": "Rob",
      "group": "J",
      "h_offset": 11.0,
      "color": {
        "light": "hsl(305 19% 36%)",
        "dark": "hsl(305 19% 64%)"
      }
    }
  ],
  "scores": [
    {
      "level": "0",
      "color": {
        "light": "hsl(220 10% 50%)",
        "dark": "hsl(220 10% 60%)"
      },
      "weight": 400,
      "opacity": 0.75
    },
    {
      "level": "1",
      "color": {
        "light": "hsl(0 70% 35%)",
        "dark": "hsl(0 70% 60%)"
      },
      "weight": 800
    },
    {
      "level": "2",
      "color": {
        "light": "hsl(28 80% 30%)",
        "dark": "hsl(28 70% 60%)"
      },
      "weight": 650
    },
    {
      "level": "3",
      "color": {
        "light": "hsl(40 80% 32%)",
        "dark": "hsl(40 70% 60%)"
      },
      "weight": 700
    },
    {
      "level": "4",
      "color": {
        "light": "hsl(140 60% 28%)",
        "dark": "hsl(140 50% 55%)"
      },
      "weight": 750
    },
    {
      "level": "5",
      "color": {
        "light": "hsl(140 60% 20%)",
        "dark": "hsl(140 50% 45%)"
      },
      "weight": 850
    },
    {
      "level": "NA",
      "color": {
        "light": "hsl(220 10% 50%)",
        "dark": "hsl(220 10% 60%)"
      },
      "weight": 400,
      "opacity": 0.65
    },
    {
      "level": "ERR",
      "color": {
        "light": "hsl(0 85% 40%)",
        "dark": "hsl(0 75% 65%)"
      },
      "weight": 700
    }
  ],
  "interactions": {
    "hover": {
      "bg": "hsl(0 0% 50% / 0.15)",
      "bg_strong": "hsl(0 0% 50% / 0.28)",
      "duration": "480ms",
      "easing": "cubic-bezier(0.32, 0.72, 0, 1)"
    }
  },
  "typography": {
    "caps": {
      "tracking": "0.09em"
    },
    "fonts": {
      "sans": {
        "family": "Source Sans 3",
        "stack": "-apple-system, BlinkMacSystemFont, \"Inter\", \"Helvetica Neue\", Arial, sans-serif",
        "source": "fontsource:source-sans-3:vf",
        "size_px": 16.5,
        "weight": 425,
        "weight_medium": 650,
        "weight_bold": 675
      },
      "serif": {
        "family": "Noto Serif",
        "stack": "\"Iowan Old Style\", \"Charter\", Georgia, serif",
        "source": "fontsource:noto-serif:vf",
        "size_px": 14.0,
        "weight": 425,
        "weight_medium": 425,
        "weight_bold": 550
      }
    }
  },
  "scoring": {
    "alpha_step": 0.16
  }
});

/** Convenience accessors keyed by id. */
export const groupsById     = Object.freeze(Object.fromEntries(designSystem.groups.map(g => [g.id, g])));
export const dimensionsById = Object.freeze(Object.fromEntries(designSystem.dimensions.map(d => [d.id, d])));
export const scoresByLevel  = Object.freeze(Object.fromEntries(designSystem.scores.map(s => [s.level, s])));

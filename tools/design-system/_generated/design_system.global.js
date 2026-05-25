/* AUTO-GENERATED from tools/design-system/design-system.yaml — do not edit by hand.
Regenerate with: uv run --script tools/design-system/generate.py */

(function () {
  const designSystem = Object.freeze({
  "version": 1,
  "surfaces": {
    "bg": {
      "light": "hsl(40 38% 93%)",
      "dark": "hsl(40 8% 8%)"
    },
    "fg": {
      "light": "hsl(30 12% 10%)",
      "dark": "hsl(40 25% 88%)"
    },
    "muted": {
      "light": "hsl(40 9% 39%)",
      "dark": "hsl(40 11% 53%)"
    },
    "card": {
      "light": "hsl(40 50% 96%)",
      "dark": "hsl(34 12% 10%)"
    },
    "border": {
      "light": "hsl(40 26% 79%)",
      "dark": "hsl(40 13% 17%)"
    },
    "rule": {
      "light": "hsl(30 12% 10%)",
      "dark": "hsl(40 25% 88%)"
    }
  },
  "groups": [
    {
      "id": "P",
      "label": "Purpose",
      "h": 72.0,
      "s": 51.0,
      "spread": 30.0,
      "ink": {
        "light": "hsl(72 51% 44%)",
        "dark": "hsl(72 51% 68%)"
      },
      "text": {
        "light": "hsl(72 51% 24%)",
        "dark": "hsl(72 51% 81%)"
      },
      "surface": {
        "light": "hsl(72 51% 92%)",
        "dark": "hsl(72 51% 18%)"
      },
      "icon": "mdi:compass-rose",
      "sense": "orientation toward the reader's task"
    },
    {
      "id": "E",
      "label": "Expression",
      "h": 206.0,
      "s": 59.0,
      "spread": 30.0,
      "ink": {
        "light": "hsl(206 59% 51%)",
        "dark": "hsl(206 59% 68%)"
      },
      "text": {
        "light": "hsl(206 59% 31%)",
        "dark": "hsl(206 59% 81%)"
      },
      "surface": {
        "light": "hsl(206 59% 92%)",
        "dark": "hsl(206 59% 18%)"
      },
      "icon": "mdi:quill",
      "sense": "language, surface form"
    },
    {
      "id": "F",
      "label": "Form",
      "h": 30.0,
      "s": 37.0,
      "spread": 30.0,
      "ink": {
        "light": "hsl(30 37% 61%)",
        "dark": "hsl(30 37% 68%)"
      },
      "text": {
        "light": "hsl(30 37% 41%)",
        "dark": "hsl(30 37% 81%)"
      },
      "surface": {
        "light": "hsl(30 37% 92%)",
        "dark": "hsl(30 37% 18%)"
      },
      "icon": "mdi:scroll",
      "sense": "the document as a structured artifact"
    },
    {
      "id": "R",
      "label": "Reasoning",
      "h": 329.0,
      "s": 47.0,
      "spread": 30.0,
      "ink": {
        "light": "hsl(329 47% 53%)",
        "dark": "hsl(329 47% 68%)"
      },
      "text": {
        "light": "hsl(329 47% 33%)",
        "dark": "hsl(329 47% 81%)"
      },
      "surface": {
        "light": "hsl(329 47% 92%)",
        "dark": "hsl(329 47% 18%)"
      },
      "icon": "mdi:ruler",
      "sense": "inference, measurement, rigor"
    },
    {
      "id": "G",
      "label": "Grounding",
      "h": 162.0,
      "s": 55.0,
      "spread": 30.0,
      "ink": {
        "light": "hsl(162 55% 45%)",
        "dark": "hsl(162 55% 62%)"
      },
      "text": {
        "light": "hsl(162 55% 25%)",
        "dark": "hsl(162 55% 75%)"
      },
      "surface": {
        "light": "hsl(162 55% 92%)",
        "dark": "hsl(162 55% 16%)"
      },
      "icon": "mdi:anchor",
      "sense": "tied to sources and facts"
    },
    {
      "id": "J",
      "label": "Judgment",
      "h": 278.0,
      "s": 30.0,
      "spread": 30.0,
      "ink": {
        "light": "hsl(278 30% 55%)",
        "dark": "hsl(278 30% 72%)"
      },
      "text": {
        "light": "hsl(278 30% 35%)",
        "dark": "hsl(278 30% 85%)"
      },
      "surface": {
        "light": "hsl(278 30% 92%)",
        "dark": "hsl(278 30% 18%)"
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
      "h_offset": -4.0,
      "color": {
        "light": "hsl(68 51% 40%)",
        "dark": "hsl(68 51% 65%)"
      }
    },
    {
      "id": "P2",
      "label": "Scope",
      "short": "Scope",
      "group": "P",
      "h_offset": 0.0,
      "color": {
        "light": "hsl(72 51% 37%)",
        "dark": "hsl(72 51% 62%)"
      }
    },
    {
      "id": "P3",
      "label": "Breadth",
      "short": "Brd",
      "group": "P",
      "h_offset": 4.0,
      "color": {
        "light": "hsl(76 51% 34%)",
        "dark": "hsl(76 51% 59%)"
      }
    },
    {
      "id": "P4",
      "label": "Depth",
      "short": "Dep",
      "group": "P",
      "h_offset": 8.0,
      "color": {
        "light": "hsl(80 51% 31%)",
        "dark": "hsl(80 51% 56%)"
      }
    },
    {
      "id": "E1",
      "label": "Clarity",
      "short": "Clar",
      "group": "E",
      "h_offset": -5.0,
      "color": {
        "light": "hsl(201 59% 35%)",
        "dark": "hsl(201 59% 68%)"
      }
    },
    {
      "id": "E2",
      "label": "Coherence",
      "short": "Coh",
      "group": "E",
      "h_offset": -2.0,
      "color": {
        "light": "hsl(204 59% 32%)",
        "dark": "hsl(204 59% 66%)"
      }
    },
    {
      "id": "E3",
      "label": "Concision",
      "short": "Conc",
      "group": "E",
      "h_offset": 1.0,
      "color": {
        "light": "hsl(207 59% 30%)",
        "dark": "hsl(207 59% 64%)"
      }
    },
    {
      "id": "F1",
      "label": "Organization",
      "short": "Org",
      "group": "F",
      "h_offset": -4.0,
      "color": {
        "light": "hsl(26 37% 38%)",
        "dark": "hsl(26 37% 64%)"
      }
    },
    {
      "id": "F2",
      "label": "Consistency",
      "short": "Cons",
      "group": "F",
      "h_offset": 0.0,
      "color": {
        "light": "hsl(30 37% 35%)",
        "dark": "hsl(30 37% 61%)"
      }
    },
    {
      "id": "F3",
      "label": "Formatting",
      "short": "Fmt",
      "group": "F",
      "h_offset": 4.0,
      "color": {
        "light": "hsl(34 37% 32%)",
        "dark": "hsl(34 37% 58%)"
      }
    },
    {
      "id": "R1",
      "label": "Discipline",
      "short": "Disc",
      "group": "R",
      "h_offset": -6.0,
      "color": {
        "light": "hsl(323 47% 40%)",
        "dark": "hsl(323 47% 68%)"
      }
    },
    {
      "id": "R2",
      "label": "Soundness",
      "short": "Snd",
      "group": "R",
      "h_offset": -3.0,
      "color": {
        "light": "hsl(326 47% 37%)",
        "dark": "hsl(326 47% 65%)"
      }
    },
    {
      "id": "R3",
      "label": "Precision",
      "short": "Prec",
      "group": "R",
      "h_offset": 0.0,
      "color": {
        "light": "hsl(329 47% 34%)",
        "dark": "hsl(329 47% 62%)"
      }
    },
    {
      "id": "R4",
      "label": "Parsimony",
      "short": "Pars",
      "group": "R",
      "h_offset": 3.0,
      "color": {
        "light": "hsl(332 47% 31%)",
        "dark": "hsl(332 47% 59%)"
      }
    },
    {
      "id": "G1",
      "label": "Verifiability",
      "short": "Ver",
      "group": "G",
      "h_offset": -4.0,
      "color": {
        "light": "hsl(158 55% 32%)",
        "dark": "hsl(158 55% 62%)"
      }
    },
    {
      "id": "G2",
      "label": "Factuality",
      "short": "Fact",
      "group": "G",
      "h_offset": 0.0,
      "color": {
        "light": "hsl(162 55% 29%)",
        "dark": "hsl(162 55% 58%)"
      }
    },
    {
      "id": "G3",
      "label": "Relevance",
      "short": "Rel",
      "group": "G",
      "h_offset": 4.0,
      "color": {
        "light": "hsl(166 55% 26%)",
        "dark": "hsl(166 55% 54%)"
      }
    },
    {
      "id": "J1",
      "label": "Calibration",
      "short": "Cal",
      "group": "J",
      "h_offset": -6.0,
      "color": {
        "light": "hsl(272 30% 42%)",
        "dark": "hsl(272 30% 70%)"
      }
    },
    {
      "id": "J2",
      "label": "Fairness",
      "short": "Fair",
      "group": "J",
      "h_offset": 0.0,
      "color": {
        "light": "hsl(278 30% 39%)",
        "dark": "hsl(278 30% 67%)"
      }
    },
    {
      "id": "J3",
      "label": "Robustness",
      "short": "Rob",
      "group": "J",
      "h_offset": 6.0,
      "color": {
        "light": "hsl(284 30% 36%)",
        "dark": "hsl(284 30% 64%)"
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
  ]
});
  const groupsById     = Object.freeze(Object.fromEntries(designSystem.groups.map(g => [g.id, g])));
  const dimensionsById = Object.freeze(Object.fromEntries(designSystem.dimensions.map(d => [d.id, d])));
  const scoresByLevel  = Object.freeze(Object.fromEntries(designSystem.scores.map(s => [s.level, s])));
  globalThis.PracticalProseDesignSystem = Object.freeze({ designSystem, groupsById, dimensionsById, scoresByLevel });
})();

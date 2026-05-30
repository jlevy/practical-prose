"""AUTO-GENERATED from tools/design-system/design-system.yaml — do not edit by hand.

Regenerate with::

    uv run python tools/design-system/generate.py
"""

from __future__ import annotations

from typing import Any

DESIGN_SYSTEM: dict[str, Any] = {
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
    "tones": {
        "icon": "hsl(40 0% 28%)",
        "dim_label": "hsl(40 0% 28%)",
        "na": "hsl(220 10% 78%)"
    },
    "groups": [
        {
            "id": "P",
            "label": "Purpose",
            "spread": 45.0,
            "ink": {
                "light": "hsl(72 19% 73%)",
                "dark": "hsl(72 19% 27%)"
            },
            "surface": {
                "light": "hsl(72 19% 92%)",
                "dark": "hsl(72 19% 18%)"
            },
            "icon": "mdi:compass-rose",
            "sense": "orientation toward the reader's task"
        },
        {
            "id": "E",
            "label": "Expression",
            "spread": 30.0,
            "ink": {
                "light": "hsl(206 19% 73%)",
                "dark": "hsl(206 19% 27%)"
            },
            "surface": {
                "light": "hsl(206 19% 92%)",
                "dark": "hsl(206 19% 18%)"
            },
            "icon": "mdi:quill",
            "sense": "language, surface form"
        },
        {
            "id": "F",
            "label": "Form",
            "spread": 20.0,
            "ink": {
                "light": "hsl(35 19% 73%)",
                "dark": "hsl(35 19% 27%)"
            },
            "surface": {
                "light": "hsl(35 19% 92%)",
                "dark": "hsl(35 19% 18%)"
            },
            "icon": "mdi:scroll",
            "sense": "the document as a structured artifact"
        },
        {
            "id": "R",
            "label": "Reasoning",
            "spread": 40.0,
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
            "spread": 40.0,
            "ink": {
                "light": "hsl(162 19% 73%)",
                "dark": "hsl(162 19% 27%)"
            },
            "surface": {
                "light": "hsl(162 19% 92%)",
                "dark": "hsl(162 19% 16%)"
            },
            "icon": "mdi:anchor",
            "sense": "tied to sources and facts"
        },
        {
            "id": "J",
            "label": "Judgment",
            "spread": 45.0,
            "ink": {
                "light": "hsl(265 19% 73%)",
                "dark": "hsl(265 19% 27%)"
            },
            "surface": {
                "light": "hsl(265 19% 92%)",
                "dark": "hsl(265 19% 18%)"
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
                "light": "hsl(68 19% 40%)",
                "dark": "hsl(68 19% 65%)"
            }
        },
        {
            "id": "P2",
            "label": "Scope",
            "short": "Scope",
            "group": "P",
            "h_offset": 0.0,
            "color": {
                "light": "hsl(72 19% 37%)",
                "dark": "hsl(72 19% 62%)"
            }
        },
        {
            "id": "P3",
            "label": "Breadth",
            "short": "Brd",
            "group": "P",
            "h_offset": 4.0,
            "color": {
                "light": "hsl(76 19% 34%)",
                "dark": "hsl(76 19% 59%)"
            }
        },
        {
            "id": "P4",
            "label": "Depth",
            "short": "Dep",
            "group": "P",
            "h_offset": 8.0,
            "color": {
                "light": "hsl(80 19% 31%)",
                "dark": "hsl(80 19% 56%)"
            }
        },
        {
            "id": "E1",
            "label": "Clarity",
            "short": "Clar",
            "group": "E",
            "h_offset": -5.0,
            "color": {
                "light": "hsl(201 19% 35%)",
                "dark": "hsl(201 19% 68%)"
            }
        },
        {
            "id": "E2",
            "label": "Coherence",
            "short": "Coh",
            "group": "E",
            "h_offset": -2.0,
            "color": {
                "light": "hsl(204 19% 32%)",
                "dark": "hsl(204 19% 66%)"
            }
        },
        {
            "id": "E3",
            "label": "Concision",
            "short": "Conc",
            "group": "E",
            "h_offset": 1.0,
            "color": {
                "light": "hsl(207 19% 30%)",
                "dark": "hsl(207 19% 64%)"
            }
        },
        {
            "id": "F1",
            "label": "Organization",
            "short": "Org",
            "group": "F",
            "h_offset": -4.0,
            "color": {
                "light": "hsl(31 19% 38%)",
                "dark": "hsl(31 19% 64%)"
            }
        },
        {
            "id": "F2",
            "label": "Consistency",
            "short": "Cons",
            "group": "F",
            "h_offset": 0.0,
            "color": {
                "light": "hsl(35 19% 35%)",
                "dark": "hsl(35 19% 61%)"
            }
        },
        {
            "id": "F3",
            "label": "Formatting",
            "short": "Fmt",
            "group": "F",
            "h_offset": 4.0,
            "color": {
                "light": "hsl(39 19% 32%)",
                "dark": "hsl(39 19% 58%)"
            }
        },
        {
            "id": "R1",
            "label": "Discipline",
            "short": "Disc",
            "group": "R",
            "h_offset": -6.0,
            "color": {
                "light": "hsl(354 19% 40%)",
                "dark": "hsl(354 19% 68%)"
            }
        },
        {
            "id": "R2",
            "label": "Soundness",
            "short": "Snd",
            "group": "R",
            "h_offset": -3.0,
            "color": {
                "light": "hsl(357 19% 37%)",
                "dark": "hsl(357 19% 65%)"
            }
        },
        {
            "id": "R3",
            "label": "Precision",
            "short": "Prec",
            "group": "R",
            "h_offset": 0.0,
            "color": {
                "light": "hsl(0 19% 34%)",
                "dark": "hsl(0 19% 62%)"
            }
        },
        {
            "id": "R4",
            "label": "Parsimony",
            "short": "Pars",
            "group": "R",
            "h_offset": 3.0,
            "color": {
                "light": "hsl(3 19% 31%)",
                "dark": "hsl(3 19% 59%)"
            }
        },
        {
            "id": "G1",
            "label": "Verifiability",
            "short": "Ver",
            "group": "G",
            "h_offset": -4.0,
            "color": {
                "light": "hsl(158 19% 32%)",
                "dark": "hsl(158 19% 62%)"
            }
        },
        {
            "id": "G2",
            "label": "Factuality",
            "short": "Fact",
            "group": "G",
            "h_offset": 0.0,
            "color": {
                "light": "hsl(162 19% 29%)",
                "dark": "hsl(162 19% 58%)"
            }
        },
        {
            "id": "G3",
            "label": "Relevance",
            "short": "Rel",
            "group": "G",
            "h_offset": 4.0,
            "color": {
                "light": "hsl(166 19% 26%)",
                "dark": "hsl(166 19% 54%)"
            }
        },
        {
            "id": "J1",
            "label": "Calibration",
            "short": "Cal",
            "group": "J",
            "h_offset": -6.0,
            "color": {
                "light": "hsl(259 19% 42%)",
                "dark": "hsl(259 19% 70%)"
            }
        },
        {
            "id": "J2",
            "label": "Fairness",
            "short": "Fair",
            "group": "J",
            "h_offset": 0.0,
            "color": {
                "light": "hsl(265 19% 39%)",
                "dark": "hsl(265 19% 67%)"
            }
        },
        {
            "id": "J3",
            "label": "Robustness",
            "short": "Rob",
            "group": "J",
            "h_offset": 6.0,
            "color": {
                "light": "hsl(271 19% 36%)",
                "dark": "hsl(271 19% 64%)"
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
            "duration": "280ms",
            "easing": "cubic-bezier(0.2, 0, 0, 1)"
        }
    },
    "typography": {
        "caps": {
            "tracking": "0.09em",
            "weight": 600,
            "weight_strong": 800
        },
        "numeric": {
            "weight": 600
        }
    },
    "scoring": {
        "alpha_step": 0.14
    }
}

# Convenience accessors keyed by id.
GROUPS_BY_ID = {g["id"]: g for g in DESIGN_SYSTEM["groups"]}
DIMENSIONS_BY_ID = {d["id"]: d for d in DESIGN_SYSTEM["dimensions"]}
SCORES_BY_LEVEL = {s["level"]: s for s in DESIGN_SYSTEM["scores"]}

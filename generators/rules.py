"""Prompt builder for the ANKLE Studio — reference-driven image-making (remix / edit /
expand / reimagine), NOT recipe vessels. The user's prompt drives; we add only light
quality + reference-handling guidance. Separate from the EP food rules on purpose.
"""

import re

QUALITY = ("Shot as one single real photograph: consistent light, grain, focus and white balance "
           "across the entire frame — nothing pasted-on, cut-out, over-sharpened, HDR-crunchy or "
           "artificially smooth. Natural photographic detail, high quality 4k. No text, watermark, "
           "border, frame or UI. Do not stretch, squish or distort proportions.")


def clean_prompt(t):
    """Strip MidJourney / blend-image artifacts from a pasted prompt: image URLs
    (s.mj.run), --flags (--v 7.0, --ar, --stylize…), literal \\n, <...> wrappers, and
    random hash codes — leaving the clean creative text."""
    t = t or ""
    t = re.sub(r"<[^>]*>", " ", t)                                  # <https://...> wrappers
    t = re.sub(r"https?://\S+", " ", t)                            # any URL
    t = re.sub(r"--\w+(?:\s+[^\s-][\w:.%]*)?", " ", t)             # MJ flags + their values
    t = t.replace("\\n", " ").replace("\n", " ")                   # literal + real newlines
    t = re.sub(r"\b(?=\w*[A-Za-z])(?=\w*\d)[A-Za-z0-9]{9,}\b", " ", t)  # hash-like ids (letters+digits, 9+)
    t = re.sub(r"\s{2,}", " ", t).strip(" ,.-")
    return t


def instr(prompt, nrefs=0, mode="remix", has_base=False, base_id=""):
    out = _compose_instr(prompt, nrefs, mode, has_base)
    if base_id == "gallery-white":   # Gallery White base ALWAYS carries the Gagosian look
        out += (" Institutional Gagosian-style sculpture documentation photography: soft, diffuse, even "
                "light from high above; the sculpture grounded by a soft-edged natural shadow pool directly "
                "beneath it with gentle falloff — no hard, double or floating shadows; faint reflected light "
                "from the white walls onto its lower surfaces; neutral white balance, medium-format clarity "
                "with subtle natural grain, like a real gallery installation photograph.")
    return out


def _compose_instr(prompt, nrefs=0, mode="remix", has_base=False):
    """Compose the generation instruction.
    prompt   = Alex's creative direction (drives everything)
    nrefs    = number of EXTRA reference images (beyond the base scene)
    mode     = 'remix' | 'edit' | 'free' (how the references are used)
    has_base = a base SCENE is supplied as image 1 (e.g. the empty gallery) — the work is
               created INTO it, matching its space/lighting (like the EP vessel base).
    """
    p = clean_prompt(prompt)   # strip any MJ blend artifacts the user pasted
    base = ("Image 1 is the EXACT empty scene photograph. Re-shoot Image 1's room — same walls, floor, "
            "camera position and light setup — with the work described physically standing in it: real "
            "contact shadows, ambient occlusion, subtle colour bounce, correct perspective and scale. "
            "Do not replace or restyle the room: ") if has_base else ""
    if not nrefs:
        return f"{base}{p}. {QUALITY}" if base else f"{p} {QUALITY}"
    nth = "2" if has_base else "1"
    if mode == "edit":
        ref = f"Use image {nth} as the source — keep its overall composition and subject; apply this: "
    elif mode == "free":
        ref = f"The other reference image(s) are loose inspiration for style, color and mood only — do not copy them. "
    elif mode == "sculpt2026":
        ref = ("Study the world of the prior sculptures shown — their materials, construction logic, scale, "
               "humour and gallery presentation — and create a NEW sculpture that belongs to that same body of "
               "work, assembled and transformed from the references. It stands directly on the floor (no plinth, "
               "pedestal or podium); Gagosian-style soft diffuse documentation. ")
    elif mode == "aleqth":
        ref = ("Build this in my voice and world: a hyper-slick contemporary gallery sculpture assembled from the "
               "references, with neo-pop charge and uncanny recombination, standing on the floor (no plinth), shot "
               "as institutional soft-diffuse Gagosian-style documentation. ")
    elif mode == "dada":
        # /dada — read the references through the L0-L3 semantic charter, then resynthesise.
        ref = ("Read the reference image(s) through a four-layer semantic lens before creating — "
               "L0 World: the environment, context and material conditions; "
               "L1 Subject: what actually appears and acts; "
               "L2 Charge: the force, mood, tension and reading it carries; "
               "L3 Meta: its frame, gesture and underlying thesis. "
               "Do not copy the references — transpose that semantic reading into a new work that honours their charge: ")
    else:  # remix
        ref = f"Use the other reference image(s) as the visual basis — sample, develop and reimagine their forms, materials, color and detail. "
    return f"{base}{ref}{p}. {QUALITY}"


if __name__ == "__main__":
    print(instr("turn this shirt graphic into a streetwear poster", nrefs=1, mode="remix"))

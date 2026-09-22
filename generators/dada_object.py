#!/usr/bin/env python3
"""The .dada object — DADA's NATIVE OUTPUT, made real.

The system "speaks in DADA": a question resolves into ONE canonical file — the **Rectangle + 3 Squares**.
  • L0 = the base canvas (the rectangle / the world / the literal), full-bleed, dimmed.
  • L1 = top square   (context / friction)
  • L2 = middle square (charge / the meme / the vibe)
  • L3 = bottom square (synthesis / the predictive trajectory)
The four images ARE the answer. Placement is the reasoning.

It is a PNG with the full semantic payload (query, L0-L3 text, image sources, didactic tags, narrative,
provenance, timestamp) embedded in an iTXt chunk → self-describing, portable, and MIRROR-ABLE: any DADA
node can read the embedded payload and reseed from it (the decentralized semantic mirror-network), and an
agent can DECODE it ("what does this mean?") because the meaning travels inside the file.

Headless by design: render()/write_dada() take a plain payload dict, so DADA can sit over ANY source
(surf / x / now / Getty / Bloomberg / a museum archive) — only the upstream adapter changes.
"""
import json, subprocess, tempfile, time
from pathlib import Path
from PIL import Image, ImageDraw, ImageEnhance
from PIL.PngImagePlugin import PngInfo
import portrait

ASSETS = Path(__file__).parent / "dashboard" / "assets" / "dada"
DADA_KEY = "ankl.dada"            # iTXt chunk key carrying the JSON payload


def _fetch(url, timeout=18):
    if not url: return None
    try:
        tf = tempfile.NamedTemporaryFile(suffix=".img", delete=False)
        subprocess.run(["curl", "-sL", "-m", str(timeout), "-o", tf.name, url], timeout=timeout + 5, capture_output=True)
        return Image.open(tf.name).convert("RGB")
    except Exception:
        return None

def _cover(im, w, h):
    iw, ih = im.size; s = max(w / iw, h / ih)
    im = im.resize((max(1, round(iw * s)), max(1, round(ih * s))), Image.LANCZOS)
    x = (im.width - w) // 2; y = (im.height - h) // 2
    return im.crop((x, y, x + w, y + h))


# === CANONICAL DADA FORMAT (per /Users/alex/Desktop/dada-protocol/dada.format.md) ===
# 768×987, NO frame/borders, L0 full-bleed cover; 3 slots 93×82 at left 337, tops 191/326/477;
# render order L0→L1→L2→L3 (back to front); "/dada" wordmark stamped bottom-right.
CANVAS_W, CANVAS_H = 768, 987
SLOT_W, SLOT_H = 93, 82
SLOTS = [(337, 191), (337, 326), (337, 477)]   # L1 subject, L2 charge, L3 meta

def render(payload):
    imgs = payload.get("images") or {}
    canvas = Image.new("RGB", (CANVAS_W, CANVAS_H), (20, 20, 22))
    l0 = _fetch((imgs.get("L0") or {}).get("url"))
    if l0:
        canvas.paste(_cover(l0, CANVAS_W, CANVAS_H), (0, 0))   # host, full-bleed cover, full brightness
    for i, k in enumerate(("L1", "L2", "L3")):                 # nodes, back-to-front, NO frame
        im = _fetch((imgs.get(k) or {}).get("url"))
        if im:
            canvas.paste(_cover(im, SLOT_W, SLOT_H), SLOTS[i])
    ImageDraw.Draw(canvas).text((CANVAS_W - 56, CANVAS_H - 26), "/dada", fill=(255, 255, 255))
    return canvas


import re as _re
def _font(size):
    from PIL import ImageFont
    for p in ("/System/Library/Fonts/Supplemental/Arial.ttf", "/Library/Fonts/Arial.ttf",
              "/System/Library/Fonts/Helvetica.ttc", "/System/Library/Fonts/Supplemental/Arial Bold.ttf"):
        try: return ImageFont.truetype(p, size)
        except Exception: pass
    return ImageFont.load_default()

_STOPW = {"the", "and", "for", "with", "this", "that", "from", "its", "are", "was", "into", "over", "a", "an", "of", "to", "in", "on"}
def _layer_word(payload, k):
    """Distill a layer to ONE salient word (for the text-DADA hashtag)."""
    L = (payload.get("layers") or {}).get(k, "") or ""
    for w in _re.findall(r"[A-Za-z][A-Za-z'-]{2,}", L):
        if w.lower() not in _STOPW:
            return w.lower()
    dd = payload.get("didactic") or []
    return (dd[0] if dd else "untitled")

def render_text(payload):
    """TEXT-DADA: no images, no labels, no watermark — just the layers as hashtag WORDS in Arial,
    centered as a clean typographic stack. L0 world hashtag(s), L1 subject (largest), L2 charge, L3 meta."""
    W, H = CANVAS_W, CANVAS_H
    canvas = Image.new("RGB", (W, H), (245, 244, 241))
    d = ImageDraw.Draw(canvas); ink = (17, 17, 17)
    lines = [("#" + _layer_word(payload, "L0"), 56), ("#" + _layer_word(payload, "L1"), 108),
             ("#" + _layer_word(payload, "L2"), 54), ("#" + _layer_word(payload, "L3"), 54)]
    gap = 46
    total = sum(sz for _, sz in lines) + gap * (len(lines) - 1)
    y = (H - total) // 2
    for txt, sz in lines:
        f = _font(sz)
        try: w = d.textlength(txt, font=f)
        except Exception: w = len(txt) * sz * 0.5
        d.text(((W - w) / 2, y), txt, font=f, fill=ink)
        y += sz + gap
    return canvas


def write_dada(payload, out_path, text=False, **kw):
    img = render_text(payload) if text else render(payload, **kw)
    meta = PngInfo(); meta.add_itxt(DADA_KEY, json.dumps(payload))
    img.save(str(out_path), "PNG", pnginfo=meta)
    return str(out_path)


def read_dada(path):
    """Read the embedded semantic payload back out of a .dada PNG (the mirror-network entry point)."""
    try:
        im = Image.open(path)
        txt = (getattr(im, "text", {}) or {}).get(DADA_KEY) or im.info.get(DADA_KEY)
        return json.loads(txt) if txt else None
    except Exception:
        return None


def build(slug, text=False):
    """Render the latest pass of a portrait into a .dada file (PNG + embedded payload). Returns its url.
    text=True → the typographic TEXT-DADA (hashtag words in Arial, no images)."""
    doc = portrait.get(slug)
    if not doc or not doc.get("passes"): return {"ok": False, "error": "no portrait — build one first"}
    p = doc["passes"][-1]
    payload = {"type": "ankl.dada/1", "query": doc.get("query"), "ts": int(time.time()),
               "source": p.get("source"), "layers": p.get("layers"), "images": p.get("images"),
               "didactic": [c.get("term") for c in (p.get("charges") or [])][:12],
               "narrative": p.get("narrative"), "provenance": ["aleqth/portrait"]}
    ASSETS.mkdir(parents=True, exist_ok=True)
    name = f"{slug}.dada.txt.png" if text else f"{slug}.dada.png"
    write_dada(payload, ASSETS / name, text=text)
    return {"ok": True, "url": f"assets/dada/{name}", "query": payload["query"], "text": text}


def decode(payload):
    """Agent Decoder: read the embedded assemblage → explain what it MEANS (the 'what does this mean?' loop)."""
    if not payload: return {"ok": False, "error": "no .dada payload found in file"}
    L = payload.get("layers") or {}
    reading = portrait._grok(
        prompt=(f'A DADA object answers: "{payload.get("query")}".\n'
                f'L0 (world): {L.get("L0","")}\nL1 (context): {L.get("L1","")}\n'
                f'L2 (charge): {L.get("L2","")}\nL3 (synthesis): {L.get("L3","")}\n'
                f'Didactic tags: {", ".join(payload.get("didactic") or [])}'),
        system=("You are the DADA decoder. Read this visual semantic assemblage (the 4 stacked layers) and "
                "explain in 3-4 plain sentences what it MEANS — why these symbols, what cultural reading or "
                "prediction the placement encodes. You are translating an image-language back into words."))
    return {"ok": True, "query": payload.get("query"), "layers": L,
            "didactic": payload.get("didactic") or [], "reading": reading or payload.get("narrative") or ""}


def mirror(payload):
    """Mirror-network: ingest another node's .dada payload, seed a NEW portrait from its charge (L0 seed)."""
    if not payload: return {"ok": False, "error": "no payload"}
    seed = (payload.get("query") or "") + " " + " ".join(payload.get("didactic") or [])
    res = portrait.build(seed.strip()[:120] or "mirror", source="surf")
    res["mirrored_from"] = payload.get("query")
    return res

#!/usr/bin/env python3
"""Aleqth Prompt Mutation Machine — Python port of prompt_machine.html.

Generates creative-direction sentences in Alex's voice by mutating his SEED PROMPT
BANK against the lexicon + synonym map (V2 "alex" preset, hybrid of structured /
mutate / chaos). Used by the overnight runner so prompts read like Alex wrote them.

  python3 prompt_machine.py 5          # print 5 mutated prompts
"""
import random, re, json
from pathlib import Path
HERE = Path(__file__).parent

# Alex's seed prompt bank (his voice corpus) — kept in sync with prompt_machine.html if present.
_SEED_FALLBACK = (
 "Skin skull with distorted limbs from a mannequin attached to it and the ribs and the body of what "
 "seems to be Ronald McDonald in a gallery front-facing camera angle soft diffuse lighting the Gagosian style | "
 "anatomy of a human head lightning flying out red scissors goosebumps style paper texture shot by wes anderson 1998 | "
 "hyper slick character with rubber features and unique color patterns hanging on a wall | "
 "long haired figure with head turned backwards and arms on opposite sides wearing black biker jacket with erected "
 "collar shot in a white void on film full body picture with legs showing side angle shot | "
 "destruction of a marble head sculpture with giant mouth and modern hair on it with red scissors goosebumps style | "
 "hands of a figure sculpture going to one side while standing the character is rendered in spongebob style but is a "
 "dolphin gagosian style photography in studio soft diffuse lighting | "
 "evolving pop character that resembles donald duck but with red fur and green polkadots doing a hand stand while on a drum | "
 "maniacal headache figure wearing jewelry with red eyes and long hair and vampiric energy sculpture in gallery environment | "
 "red smooth ferrari headed shark with looney toon style face mouth and eyes dog with legs of a mechanical whisk and a pencil | "
 "square shaped suitcase muscular-shaped robot body with really intense build that kind of resembles more so a wall than a "
 "body, very ornate and well-designed patterns, studded in parts, very technological | "
 "there's some rodeo sound equipment attached to the back of a dentist skull mannequin metallic and it's hung on the wall, "
 "and there's a pink cat-like pink panther style action figure hanging on to the attachment between the two objects | "
 "pulse radar zombie with neo pop imagery jeff koons rhizomatic dna with balloon hands and giant chin and fairly odd "
 "parents eyes bizzaro clandestine manifesto style warrior with anthropomorphic gestures laconian influences post jung "
 "majerus vision via sigmar polke | "
 "inflatable toy lizard doing a yoga pose bending backwards | "
 "long whispy hands and fingers falling from a piano like a waterfall in white void studio gagosian style | "
 "michel majerus style hybrid conceptual platform as a human pseudo figure pop culture jeff koons sculpture by an artist "
 "affiliated with richard prince | "
 "real down bad ugly amazing superhero with distinct look standing in white void studio | "
 "silver long armed human with long neck shoulder abstract poses and angry face skin in white void studio with flannel "
 "blanket over face | "
 "jeff koons balloon dog but its a dog mask | "
 "michel majerus style hybrid picasso with richard prince influence sculpture by an artist affiliated with supreme and demna | "
 "german shepherd doing a yoga pose where their stomach is facing up and their four paws are on the ground white background | "
 "egon schiele inspired expressive sculpture of a purple rubber figure | "
 "standing bathtub with long legs and head of a giraffe popping up from top | "
 "space character with laser from eyes onto the ground below them of the gallery studio gagosian style photo while "
 "floating in the air white void studio background | "
 "red human with giant feet and hands and normal skin in white void studio with giant blade in chest | "
 "skinny tall orange fox anime creature inspired by pink panther standing on tip toes looking at the ground white void studio | "
 "egon schiele inspired expressive sculpture of a thatch figure shirtless extending one arm laughing maniacally full body shot | "
 "purple dragon spongebob skull with sapphire eyes and metallic teeth extending jaw shoulder abstract white void background studio | "
 "a bat balloon animal in white void studio | "
 "green human with giant muscular shoulder abstract poses and normal skin in white void studio with flannel blanket over face"
)

LEX = {
 "colors":["red","silver","green","purple","orange","pink","chrome","matte black","candy-apple red","pale rubber","flesh-toned","glossy white","blue"],
 "beings":["humanoid","pseudo-figure","warrior","saint","superhero","creature","figure","idol","mascot cadaver","action figure","robot body","animal-headed human","hybrid sculpture"],
 "animals":["shark","fox","dolphin","dragon","lizard","dog","bear","bat","goose","giraffe","panther","german shepherd","snake","otter","pelican","rat","cat","bird"],
 "bodyParts":["skull","ribs","jaw","neck","shoulders","hands","feet","elbows","wrists","calves","torso","spine","mouth","eyes","beak"],
 "distortions":["reversed elbows","long neck","giant hands","giant feet","head turned backwards","arms on opposite sides","extended jaw","balloon hands","wall-like torso","melting fingers","abstract shoulders","distorted limbs","exposed ribs","flannel over the face","fabric draped over head","one enormous mouth in the chest","backward wrists","beak-like face-shell"],
 "objects":["cymbals","drum","suitcase","bathtub","red scissors","pencil","mechanical whisk","rodeo sound equipment","dentist skull rig","laser beam apparatus","jewelry","biker jacket","paper texture","sound hardware","balloon dog mask","chrome dental jaw","sheet drape","cloth veil"],
 "materials":["paper-texture skin","rubber surface","glossy fiberglass","chrome-plated skin","metallic teeth","inflatable vinyl","dusty marble","smooth lacquer","skin-like silicone","polished resin","studded tech surface","hyper-slick skin"],
 "actions":["balancing on one leg while laughing","doing a handstand","bending backwards","floating in the air","hanging on the wall","looking at the ground on tip toes","extending one arm","projecting lasers onto the ground","twisting sideways","standing front-facing","laughing maniacally","leaning like it is about to tip over","standing in profile"],
 "environments":["in a white void studio","in a gallery environment","wall-mounted in a pristine gallery","inside an institutional white space","in a soft museum-clean studio","against a cyclorama background","in a blank showroom"],
 "photo":["front-facing soft diffuse lighting","Gagosian-style photography","shot on film","full body side angle shot","centered documentation shot","institutional soft light","clean product-style frontal shot","soft gallery documentation light"],
 "style":["post-Majerus energy","Koons energy","Goosebumps energy","Egon Schiele energy","Sigmar Polke energy","Richard Prince residue","Wes Anderson 1998 symmetry","neo-pop charge","clandestine manifesto aura","rhizomatic DNA"],
 "connectors":["with","fused with","attached to","wearing","holding","merged with","interrupting","contaminated by","crossed with","dragging","sprouting"],
 "intensifiers":["hyper-slick","elegant grotesque","maniacal","vampiric","bizzaro","ceremonial","luxury-grade","sinister","charged","weirdly graceful","neo-pop","down bad","ornate"],
 "references":["Ronald McDonald","Pink Panther","SpongeBob","Donald Duck","Looney Tunes","Ferrari","Picasso","Supreme","Demna","Richard Prince","Jeff Koons","Michel Majerus","Sigmar Polke","Wes Anderson"],
}
SYN = {
 "cat":["rat","bat","fox","panther","otter"], "skull":["head","death-mask","cranium","face-shell"],
 "humanoid":["pseudo-figure","saint","warrior","creature","idol"], "studio":["gallery","white room","cyclorama","institutional space"],
 "fused":["merged","crossed","spliced","welded","contaminated"], "laughing":["grinning","smirking","cackling","laughing maniacally"],
 "pink":["purple","red","orange","chrome","blue"], "dog":["bear","fox","shark","goose"],
 "head":["skull","mask","face","cranium"], "cloth":["fabric","sheet","veil","drape"],
}
# V2 "alex" preset (rougher phrasing, looser punctuation)
V2 = dict(mode="hybrid", voiceProfile="alex", punctuationMode="minimal",
          mutation=.70, structure=.60, chaos=.52, novelty=.82, fragmentation=.68,
          randomizeOrder=True, randomizeGrammar=True, useSeedFragments=True, lowercaseBias=True, preserveRough=True, preserveStudio=True)

_choose = lambda a: random.choice(a)
_maybe = lambda p: random.random() < p
def _shuffle(a): a=list(a); random.shuffle(a); return a
def _nw(s): return re.sub(r"\s+", " ", (s or "").replace(" "," ").replace(" "," ")).strip()
def _lowerish(s): s=_nw(s); return (s[0].lower()+s[1:]) if s else s
def _sentence(s): s=_nw(s); return (s[0].upper()+s[1:]) if s else s

VOICE_CORPUS = HERE / "voice_corpus.jsonl"      # perpetual log of every submitted creative direction
ITEMS_F = HERE / "items.json"

def _base_seeds():
    p = Path.home() / "Desktop" / "ankl-aleqth-os" / "_deploy" / "aleqth" / "prompt_machine.html"
    if p.exists():
        try:
            m = re.search(r'<textarea id="seedBank">(.*?)</textarea>', p.read_text(), re.DOTALL)
            if m:
                raw = re.split(r'\n\s*\n|\s{3,}', m.group(1))
                s = [_nw(x) for x in raw if len(_nw(x)) > 12]
                if s: return s
        except Exception: pass
    return [_nw(x) for x in _SEED_FALLBACK.split("|") if _nw(x)]

def _user_seeds():
    """Alex's OWN submitted directions — the evolving voice. Corpus log + current sessions."""
    out = []
    if VOICE_CORPUS.exists():
        for ln in VOICE_CORPUS.read_text().splitlines():
            try: t = _nw(json.loads(ln).get("text", ""))
            except Exception: t = ""
            if len(t) > 8: out.append(t)
    if ITEMS_F.exists():
        try:
            for it in json.loads(ITEMS_F.read_text()):
                t = _nw(it.get("prompt") or "")
                if len(t) > 8: out.append(t)
        except Exception: pass
    return out

_SEED_CACHE = {"seeds": None, "sig": None}
def seeds():
    sig = ((VOICE_CORPUS.stat().st_mtime if VOICE_CORPUS.exists() else 0),
           (ITEMS_F.stat().st_mtime if ITEMS_F.exists() else 0))
    if _SEED_CACHE["sig"] != sig:
        seen = set(); merged = []
        for s in _base_seeds() + _user_seeds():
            if s and s not in seen: seen.add(s); merged.append(s)
        _SEED_CACHE["seeds"] = merged; _SEED_CACHE["sig"] = sig
    return _SEED_CACHE["seeds"]

def log_direction(text):
    """Append a submitted creative direction to the perpetual voice corpus (informs the voice forever)."""
    t = _nw(text or "")
    if len(t) <= 4: return
    VOICE_CORPUS.parent.mkdir(parents=True, exist_ok=True)
    with VOICE_CORPUS.open("a") as f: f.write(json.dumps({"text": t}) + "\n")

def voice_stats():
    n = sum(1 for ln in VOICE_CORPUS.read_text().splitlines() if ln.strip()) if VOICE_CORPUS.exists() else 0
    return {"corpus": n, "total_seeds": len(seeds())}

def _source_fragment(prompt):
    bits = [_nw(x) for x in re.split(r",| and | while | with | in | shot | but ", prompt, flags=re.I) if len(_nw(x)) > 6]
    return _choose(bits) if bits else prompt

def _mutate_text(fragment, intensity):
    out = []
    for w in re.split(r"(\b)", fragment or ""):
        pl = w.lower()
        out.append(_choose(SYN[pl]) if (pl in SYN and _maybe(intensity)) else w)
    return _nw("".join(out))

def _compose(parts, s):
    p = [x for x in parts if x]
    if s["randomizeOrder"]: p = _shuffle(p)
    if s["fragmentation"] > .7: p = [re.sub(r"^(with|and) ", "", x, flags=re.I) for x in p]
    text = " ".join(p) if s["punctuationMode"] == "raw" else ", ".join(p)
    if s["lowercaseBias"]: text = _lowerish(text)
    if s["preserveRough"]:
        text = _nw(re.sub(r"\bthe\b", lambda m: "" if _maybe(.12) else m.group(), text, flags=re.I))
    return _nw(text.replace(", with ", ", ").replace(", and ", ", "))

def _clauses(s):
    src = _choose(seeds()) if seeds() else ""
    exact = _mutate_text(_source_fragment(src), s["mutation"]) if (s["useSeedFragments"] and src) else ""
    cl = [
        f"{_choose(LEX['intensifiers'])} {_choose(LEX['colors'])} {_choose(LEX['animals'])}-like {_choose(LEX['beings'])}",
        f"with {_choose(LEX['distortions'])} and {_choose(LEX['materials'])}",
        f"{_choose(LEX['connectors'])} {_choose(LEX['objects'])}",
        _choose(LEX['actions']), _choose(LEX['environments']), _choose(LEX['photo']),
        f"with {_choose(LEX['style'])} and {_choose(LEX['references'])} residue",
    ]
    if exact: cl.insert(0, exact)
    if _maybe(s["chaos"]): cl.append(_choose([f"whose {_choose(LEX['bodyParts'])} feel contaminated by {_choose(LEX['references'])}",
        "rendered as a hyper-slick gallery sculpture", "photographed like a major institutional acquisition",
        "where the composition feels ceremonial but unstable", "and the silhouette reads like a corrupted mascot relic"]))
    return cl

def _structured(s):
    cl = _clauses(s); cl = _shuffle(cl) if s["randomizeOrder"] else cl
    return _compose(cl[:6 + random.randint(0, 1)], s)

def _mutate_source(s):
    prompt = _choose(seeds()) if seeds() else ""
    prompt = _mutate_text(prompt, s["mutation"] * 1.2)
    if _maybe(s["novelty"]):
        prompt += ", " + _choose([_choose(LEX['distortions']), _choose(LEX['objects']), _choose(LEX['materials']),
                                   _choose(LEX['style']), _choose(LEX['actions']), _choose(LEX['photo'])])
    if _maybe(s["structure"]): prompt = ", ".join(_shuffle(re.split(r",| and ", prompt)))
    if s["preserveStudio"] and not re.search(r"studio|gallery|white void|lighting", prompt, re.I):
        prompt += ", " + _choose(LEX['environments']) + ", " + _choose(LEX['photo'])
    return _compose(re.split(r",\s*", prompt), s)

def _chaos(s):
    pool = _shuffle(_clauses(s))[:5 + random.randint(0, 2)]
    conns = [" while ", " but also ", " interrupted by ", " and at the same time ", " as if ", " with "] if s["randomizeGrammar"] else [", "]
    text = pool[0] if pool else ""
    for x in pool[1:]: text += _choose(conns) + x
    if _maybe(s["chaos"] * .7) and seeds():
        text += " " + " ".join(_choose(seeds()).split()[:8 + random.randint(0, 10)])
    return _compose(re.split(r",\s*| while | but also | interrupted by | and at the same time | as if | with ", text), s)


def voiceify(text, settings=None):
    """Filter the USER'S creative direction through Alex's voice — keep their intent, but
    synonym-swap toward his lexicon, season with a couple of his style fragments, and apply
    his rough/lowercase phrasing. Used by the aleqth-voice toggle on each session."""
    s = settings or V2
    t = _nw(text or "")
    if not t: return _choose(seeds()) if seeds() else ""
    base = _mutate_text(t, s["mutation"] * 0.7)
    season = ", " + _choose(LEX["intensifiers"]) + " " + _choose(LEX["style"])
    if _maybe(0.5): season += ", " + _choose(LEX["connectors"]) + " " + _choose(LEX["objects"])
    return _compose(re.split(r",\s*", base + season), s)


def generate(n=1, settings=None):
    """n creative-direction prompts in Alex's voice (hybrid of the three generators)."""
    s = settings or V2
    out = []
    for _ in range(n):
        out.append(_choose([_structured, _mutate_source, _chaos])(s))
    return out


if __name__ == "__main__":
    import sys
    for p in generate(int(sys.argv[1]) if len(sys.argv) > 1 else 5):
        print("•", p, "\n")

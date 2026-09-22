# The 4-Layer Prompt Architecture (L0–L3)

This repository structures prompts using a 4-layer physical ontology rather than generic adjectives or "cinematic" buzzwords. This framework produces grounded, materially believable, and visually singular imagery and video motion.

---

## The Four Layers

### Layer 0: L0 World (The Concrete Environment)
- **Definition:** An ordinary, precise, and socially legible environment with physical reality and history.
- **Why it matters:** Generative models default to floating voids or generic fantasy backdrops when unanchored. L0 establishes gravity, architecture, and lighting sources.
- **Examples:**
  - *"A fluorescent service corridor behind a discount department store at closing time"*
  - *"A roadside motel ice-machine alcove in flat morning light"*
  - *"A community-theater costume-storage room after rehearsal"*
  - *"A shuttered suburban mall food-court service entrance"*

### Layer 1: L1 Configuration (Subjects & Physical Staging)
- **Definition:** The figures, objects, or mechanical apparatuses arranged in an exact physical relationship. Bodies should be structural, caught in mid-action or bracing, rather than posed fashion figures.
- **Why it matters:** Establishes spatial composition, eye lines, physical contact points, and weight distribution.
- **Examples:**
  - *"A person half-hidden by a curtain holds an industrial machine at shoulder height while another checks the fit"*
  - *"Two coworkers quietly adjust a reflective emergency wrap around a third person standing motionless"*
  - *"No people: an abandoned changing-room arrangement left exactly as if a performance just ended"*

### Layer 2: L2 Material Event / Charge (The Singular Anomaly)
- **Definition:** Exactly **one** restrained physical inconsistency, material tension, or kinetic impossibility.
- **Rule:** Never overload the scene with multiple magic effects. One precise physical anomaly grounds the surrealism.
- **Examples:**
  - *"The bundle of cables makes one clean, protective enclosure around the object, with no magic glow or spectacle"*
  - *"A thin sheet of clear packing material holds a precise human-shaped pocket of air, but nothing else transforms"*
  - *"The reflective foil surface catches the flat light so aggressively that it briefly functions as a second person in the composition"*
  - *"A soft polyurethane mass is too large for its plastic crate, but neither worker reacts theatrically"*

### Layer 3: L3 Photographic / Video Receipt (Optical Capture)
- **Definition:** The camera, lens, lighting behavior, aspect ratio, and reproduction characteristics.
- **Why it matters:** Tells the model how the image or video was recorded, suppressing glossy AI CGI texture in favor of authentic documentary, editorial, or film artifacts.
- **Examples:**
  - *"Portrait 4:5, bright clinical practical light with a small direct flash lift, unglamorous crop, crisp editorial documentation"*
  - *"Vertical 9:16, 60fps, slow deliberate telephoto push-in, cold sodium-vapor light reflecting off wet concrete"*
  - *"Medium-format film scan, clean whites and restrained color separation, natural paper-dust grain, zero CGI gloss"*

---

## Translating L0–L3 into Video Prompts

When animating an L0–L3 still into video (via Veo, Kling, or Seedance):
1. **Preserve L0 & L1 Stability:** Lock character anatomy, clothing, and background architecture.
2. **Animate L2 Motion:** Make the material event dynamically evolve (e.g. cables flexing, fluids dripping, foil rippling).
3. **Control L3 Optics:** Add purposeful camera choreography (slow push-in, low-angle tracking, Dutch angle) rather than erratic panning.
4. **Dialogue & Audio Cues:** If the model supports native audio (Veo 3.1), specify ambient acoustic cues (echo in empty hall, rain on metal dock) alongside spoken lines.

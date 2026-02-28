#!/usr/bin/env python3
import re
import sys

def check_prompt_physics(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    prompt_match = re.search(r'\*\*PROMPT:\*\*(.*?)\n---', content, re.DOTALL | re.IGNORECASE)
    if not prompt_match:
        return False, "PROMPT: Блок промпта не найден или не закрыт '---'."

    p = prompt_match.group(1).lower()
    
    # Обязательные категории токенов для V3.0
    physics = ["refraction", "diffraction", "volumetric", "subsurface", "scattering", "caustics"]
    optics = ["chromatic", "aberration", "depth of field", "bokeh", "f/", "mm", "lens", "anamorphic"]
    textures = ["tactile", "micro-structure", "pores", "grain", "dust"]

    found_physics = [t for t in physics if t in p]
    found_optics = [t for t in optics if t in p]
    found_textures = [t for t in textures if t in p]

    score = len(found_physics) + len(found_optics) + len(found_textures)

    if score < 4:
        return False, f"PROMPT: Слишком простой промпт (Score: {score}). Добавьте физику света или параметры оптики."
    
    return True, f"PROMPT: Visual Masterpiece Level Confirmed (Score: {score})."

if __name__ == "__main__":
    if len(sys.argv) < 2: sys.exit(1)
    ok, msg = check_prompt_physics(sys.argv[1])
    if ok:
        print(f"✅ {msg}")
        sys.exit(0)
    else:
        print(f"❌ {msg}")
        sys.exit(1)

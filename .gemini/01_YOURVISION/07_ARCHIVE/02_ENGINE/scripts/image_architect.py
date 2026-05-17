import json
import os
import random

CORE_PATH = "/home/levdanskiy/.gemini/CORE/knowledge/"
MANIFEST_PATH = os.path.join(CORE_PATH, "visual_manifest.json")

class ImageArchitect:
    def __init__(self):
        self.manifest = self._load_manifest()

    def _load_manifest(self):
        if not os.path.exists(MANIFEST_PATH):
            return {}
        with open(MANIFEST_PATH, 'r') as f:
            return json.load(f)

    def _get_default_model(self, channel):
        models = {
            "AC": ["An elegant architect (Female, 30s) in a minimalist coat", "A visionary designer (Male, 40s) looking at the structure"],
            "NB": ["A local traveler (Female, 20s) with expressive eyes", "An authentic resident (Male, 50s) wearing traditional textures"],
            "YV": ["A charismatic host (Female, 25s) in high fashion", "A cool DJ (Male, 20s) with stylish accessories"]
        }
        return random.choice(models.get(channel, ["A model"]))

    def construct_prompt(self, channel, scene_desc, model_desc=None, title=None, ar="16:9"):
        config = self.manifest.get(channel, {})
        if not config: return "Error"

        template = config.get("prompt_template", "")
        
        # Обработка модели
        if config.get("model_mandate") == "REQUIRED":
            if not model_desc:
                model_desc = self._get_default_model(channel)
            template = template.replace("[MODEL DESCRIPTION]", model_desc)
        elif config.get("model_mandate") == "FORBIDDEN":
            template = template.replace("[MODEL DESCRIPTION]", "") # Удаляем плейсхолдер если он был

        # Заполнение сцены и AR
        final_prompt = template.replace("[SCENE DESCRIPTION]", scene_desc)
        final_prompt = final_prompt.replace("[AR]", ar)
        
        # Обработка заголовка (YV)
        if "[TITLE]" in final_prompt:
            clean_title = (title or "Title").replace('"', '').replace("'", "")
            final_prompt = final_prompt.replace("[TITLE]", f'"{clean_title}"')

        return final_prompt

if __name__ == "__main__":
    arch = ImageArchitect()
    print(arch.construct_prompt("AC", "Modern concrete museum", title="Test"))
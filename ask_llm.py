import requests
import sys
import json
import os

MODELS = {
    "mistral": "mistralai/mistral-small-4-119b-2603",
    "qwen": "qwen/qwen3.5-122b-a10b",
    "minimax": "minimaxai/minimax-m2.5",
    "glm": "z-ai/glm5",
    "deepseek": "deepseek-ai/deepseek-v3.2",
    "gpt-oss": "openai/gpt-oss-20b",
    "gemma": "google/gemma-3n-e4b-it",
    "llama": "meta/llama-3.1-405b-instruct",
    "nemotron": "nvidia/nemotron-4-340b-instruct",
    "phi": "microsoft/phi-3-medium-128k-instruct",
    "kimi": "moonshotai/kimi-k2.5"
}

# Terminal colors
_USE_COLOR = sys.stdout.isatty() and os.getenv("NO_COLOR") is None
_REASONING_COLOR = "\033[90m" if _USE_COLOR else ""
_RESET_COLOR = "\033[0m" if _USE_COLOR else ""

def ask_llm(model_key, prompt):
    if model_key not in MODELS:
        return f"Error: Unknown model key '{model_key}'"
    
    model_name = MODELS[model_key]
    invoke_url = "https://integrate.api.nvidia.com/v1/chat/completions"
    api_key = "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"

    headers = {
      "Authorization": f"Bearer {api_key}",
      "Accept": "application/json"
    }

    payload = {
      "model": model_name,
      "messages": [{"role": "user", "content": prompt}],
      "max_tokens": 16384 if model_key not in ["gemma", "phi"] else 1024,
      "temperature": 1.0 if model_key in ["kimi", "gpt-oss"] else (0.6 if model_key == "qwen" else 0.1),
      "top_p": 0.95,
      "stream": False
    }

    # Model specific logic
    if model_key == "qwen":
        payload["chat_template_kwargs"] = {"enable_thinking": True}
    if model_key == "glm":
        payload["chat_template_kwargs"] = {"enable_thinking": True, "clear_thinking": False}
    if model_key in ["deepseek", "kimi"]:
        payload["extra_body"] = {"chat_template_kwargs": {"thinking": True}}
    if model_key == "mistral":
        payload["reasoning_effort"] = "high"

    try:
        response = requests.post(invoke_url, headers=headers, json=payload)
        response.raise_for_status()
        result = response.json()
        
        choice = result['choices'][0]['message']
        reasoning = choice.get('reasoning_content', '')
        content = choice.get('content', '')
        
        output = f"--- MODEL: {model_name} ---\n"
        if reasoning:
            output += f"{_REASONING_COLOR}--- REASONING ---\n{reasoning}\n---{_RESET_COLOR}\n"
        output += content
        return output
    except Exception as e:
        return f"Error with {model_name}: {str(e)}"

if __name__ == "__main__":
    if len(sys.argv) > 2:
        m_key = sys.argv[1]
        u_prompt = " ".join(sys.argv[2:])
        print(ask_llm(m_key, u_prompt))
    else:
        print("Usage: python3 ask_llm.py [model_key] 'your prompt'")
        print(f"Available keys: {list(MODELS.keys())}")

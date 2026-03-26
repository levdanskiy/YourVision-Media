import requests
import sys
import json
import os

# OpenRouter API Configuration
OPENROUTER_API_KEY = "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"
INVOKE_URL = "https://openrouter.ai/api/v1/chat/completions"

# Terminal colors for reasoning
_USE_COLOR = sys.stdout.isatty() and os.getenv("NO_COLOR") is None
_REASONING_COLOR = "\033[90m" if _USE_COLOR else ""
_RESET_COLOR = "\033[0m" if _USE_COLOR else ""

def ask_openrouter(model_name, prompt, thinking=False):
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "HTTP-Referer": "https://github.com/levdanskiy/YourVision-Hub",
        "X-Title": "YourVision Elite Hub",
        "Content-Type": "application/json"
    }

    payload = {
        "model": model_name,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7,
        "top_p": 1,
        "repetition_penalty": 1,
    }
    
    # Enable thinking/reasoning for supported models
    if thinking:
        payload["include_reasoning"] = True

    try:
        response = requests.post(INVOKE_URL, headers=headers, json=payload)
        response.raise_for_status()
        result = response.json()
        
        if 'choices' not in result:
            return f"Error: No choices in response. Raw: {result}"
            
        message = result['choices'][0]['message']
        content = message.get('content', '')
        reasoning = message.get('reasoning', '') # OpenRouter specific reasoning field
        
        output = f"--- OPENROUTER MODEL: {model_name} ---\n"
        if reasoning:
            output += f"{_REASONING_COLOR}--- REASONING ---\n{reasoning}\n---{_RESET_COLOR}\n"
        output += content
        return output
    except Exception as e:
        return f"Error with OpenRouter ({model_name}): {str(e)}"

if __name__ == "__main__":
    if len(sys.argv) > 2:
        # Check if first arg is --thinking
        idx = 1
        is_thinking = False
        if sys.argv[idx] == "--thinking":
            is_thinking = True
            idx += 1
        
        m_name = sys.argv[idx]
        u_prompt = " ".join(sys.argv[idx+1:])
        print(ask_openrouter(m_name, u_prompt, is_thinking))
    else:
        print("Usage: python3 ask_openrouter.py [--thinking] [model_name] 'your prompt'")
        print("Example: python3 ask_openrouter.py anthropic/claude-3.5-sonnet 'Hello'")

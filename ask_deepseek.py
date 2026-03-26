import requests
import sys
import json

def ask_deepseek(prompt):
    invoke_url = "https://integrate.api.nvidia.com/v1/chat/completions"
    api_key = "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"

    headers = {
      "Authorization": f"Bearer {api_key}",
      "Accept": "application/json"
    }

    payload = {
      "model": "deepseek-ai/deepseek-v3.2",
      "messages": [{"role": "user", "content": prompt}],
      "max_tokens": 8192,
      "temperature": 1,
      "top_p": 0.95,
      "extra_body": {"chat_template_kwargs": {"thinking": True}},
      "stream": False
    }

    try:
        response = requests.post(invoke_url, headers=headers, json=payload)
        response.raise_for_status()
        result = response.json()
        
        # Extracting reasoning and content if available
        choice = result['choices'][0]['message']
        reasoning = choice.get('reasoning_content', '')
        content = choice.get('content', '')
        
        output = ""
        if reasoning:
            output += f"--- REASONING ---\n{reasoning}\n---\n"
        output += content
        return output
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == "__main__":
    if len(sys.argv) > 1:
        user_prompt = " ".join(sys.argv[1:])
        print(ask_deepseek(user_prompt))
    else:
        print("Usage: python3 ask_deepseek.py 'your prompt'")

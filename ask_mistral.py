import requests
import sys
import json

def ask_mistral(prompt):
    invoke_url = "https://integrate.api.nvidia.com/v1/chat/completions"
    api_key = "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"

    headers = {
      "Authorization": f"Bearer {api_key}",
      "Accept": "application/json"
    }

    payload = {
      "model": "mistralai/mistral-small-4-119b-2603",
      "reasoning_effort": "high",
      "messages": [{"role": "user", "content": prompt}],
      "max_tokens": 16384,
      "temperature": 0.1,
      "top_p": 1,
      "stream": False
    }

    try:
        response = requests.post(invoke_url, headers=headers, json=payload)
        response.raise_for_status()
        result = response.json()
        return result['choices'][0]['message']['content']
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == "__main__":
    if len(sys.argv) > 1:
        user_prompt = " ".join(sys.argv[1:])
        print(ask_mistral(user_prompt))
    else:
        print("Usage: python3 ask_mistral.py 'your prompt'")

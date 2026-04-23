import requests
import prompts

url = "http://127.0.0.1:8000/generate_template"

payload = {
    "user_input": prompts.mobile_shop,
    "num_variations": 3
}

try:
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        data = response.json()
except Exception:
    pass

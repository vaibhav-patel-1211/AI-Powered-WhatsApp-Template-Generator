import requests
import prompts
from pprint import pprint

url = "http://127.0.0.1:8000/generate_template"

payload = {
    "user_input": (
       prompts.mobile_shop
    ),
    "num_variations": 3
}

try:
    # API call with timeout
    response = requests.post(url, json=payload)

    print("Status Code:", response.status_code)

    if response.status_code != 200:
        print("Error Response:")
        print(response.text)
        exit()

    data = response.json()

except requests.exceptions.RequestException as e:
    print("Network or server error:")
    print(e)
    exit()

except ValueError:
    print("Failed to parse JSON response")
    exit()

# -------------------------------
# Print output
# -------------------------------
# for i, item in enumerate(data, start=1):
#     print("\n" + "=" * 30)
#     print(f"       VARIATION {i}")
#     print("=" * 30)

#     print("Style        :", item.get("variation_style"))
#     print("Heading      :", item.get("heading"))

#     print("\nBody:")
#     print(item.get("body"))

#     print("\nButtons:")
#     pprint(item.get("buttons", []))

#     print("\nImage Prompt:")
#     print(item.get("image_prompt"))

#     print("Image Path   :", item.get("image_path"))
pprint(data)

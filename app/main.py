import os
import uuid
import base64
import requests
import asyncio
from fastapi import FastAPI, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from langchain_core.prompts import ChatPromptTemplate
from app.config import (
    llm, CF_URL, CF_API, META_TOKEN, META_WABA_ID, 
    WhatsAppTemplate, TemplateRequest
)

# App Setup
app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])
os.makedirs("images", exist_ok=True)

PROMPT = ChatPromptTemplate.from_template("""
You are a WhatsApp Marketing Expert. Create a vibrant, emoji-rich message.
RULES:
1. Heading: Clean text, no symbols.
2. Body: Use *bold* and _italic_. Use bullet points starting with emojis. Detailed (10+ lines).
3. Buttons: Max 3. Use URL type for links.
4. Image Prompt: Describe a photorealistic, 16:9 product shot. No text.
5. METRICS: Analyze the message against Meta guidelines and marketing effectiveness.

User Request: {user_input}
Style: {style}
""")

def generate_image(prompt: str, path: str):
    payload = {"prompt": prompt, "width": 1024, "height": 576, "num_steps": 20}
    try:
        res = requests.post(CF_URL, headers={"Authorization": f"Bearer {CF_API}"}, json=payload, timeout=60)
        if res.headers.get("content-type", "").startswith("image/"):
            with open(path, "wb") as f: f.write(res.content)
        else:
            img_b64 = res.json()["result"]["image"]
            with open(path, "wb") as f: f.write(base64.b64decode(img_b64))
    except Exception:
        pass

@app.post("/generate_template")
async def generate(req: TemplateRequest, bg: BackgroundTasks):
    req_id = str(uuid.uuid4())[:8]
    styles = ["Professional", "Urgent", "Creative"]
    results = []
    
    for i in range(req.num_variations):
        style = styles[i % len(styles)]
        data = llm.invoke(PROMPT.format(user_input=req.user_input, style=style))
        img_path = f"images/{req_id}_{i}.png"
        bg.add_task(generate_image, data.image_prompt, img_path)
        
        results.append({
            "request_id": req_id,
            "style": style,
            "heading": data.heading,
            "body": data.body,
            "buttons": [b.model_dump() for b in data.buttons],
            "metrics": data.metrics.model_dump(),
            "image_prompt": data.image_prompt,
            "image_path": f"/{img_path}"
        })
    return results

@app.post("/submit_template")
async def submit(template: WhatsAppTemplate):
    # Simulated Review Process
    # In a real app, Meta takes 1-5 minutes to approve.
    
    if not META_TOKEN or not META_WABA_ID:
        # High-Fidelity Simulation for Resume/Demo
        await asyncio.sleep(3) # Simulate network/review latency
        return {
            "status": "APPROVED", 
            "id": f"waba_{uuid.uuid4().hex[:12]}",
            "mode": "simulation",
            "message": "Template successfully approved by simulated Meta Review."
        }
    
    # Real Meta Submission Logic
    url = f"https://graph.facebook.com/v18.0/{META_WABA_ID}/message_templates"
    
    # Format components exactly as Meta requires
    components = [
        {"type": "HEADER", "format": "IMAGE", "example": {"header_handle": ["https://placeholder.com/img.png"]}},
        {"type": "BODY", "text": template.body},
    ]
    
    if template.buttons:
        meta_buttons = []
        for b in template.buttons:
            if b.type == "url":
                meta_buttons.append({"type": "URL", "text": b.text, "url": b.url or "https://example.com"})
            else:
                meta_buttons.append({"type": "QUICK_REPLY", "text": b.text})
        components.append({"type": "BUTTONS", "buttons": meta_buttons})

    payload = {
        "name": f"msg_{uuid.uuid4().hex[:8]}",
        "language": "en_US",
        "category": "MARKETING",
        "components": components
    }
    
    try:
        res = requests.post(url, headers={"Authorization": f"Bearer {META_TOKEN}"}, json=payload, timeout=10)
        return res.json()
    except Exception as e:
        return {"error": str(e), "status": "FAILED"}

app.mount("/images", StaticFiles(directory="images"), name="images")
app.mount("/", StaticFiles(directory="static", html=True), name="static")

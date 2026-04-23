import os
from dotenv import load_dotenv
from langchain_nvidia_ai_endpoints import ChatNVIDIA
from pydantic import BaseModel, Field
from typing import List, Optional, Literal

load_dotenv()

# API Keys
NVIDIA_API_KEY = os.getenv("NVIDIA_API_KEY")
CF_API = os.getenv("CLOUD_FLARE_API")
CF_ACCOUNT = os.getenv("ACCOUNT")
META_TOKEN = os.getenv("META_ACCESS_TOKEN")
META_WABA_ID = os.getenv("META_WABA_ID")

if not all([NVIDIA_API_KEY, CF_API, CF_ACCOUNT]):
    raise RuntimeError("Missing API Credentials in .env")

# AI Models Configuration
CF_MODEL = "@cf/stabilityai/stable-diffusion-xl-base-1.0"
CF_URL = f"https://api.cloudflare.com/client/v4/accounts/{CF_ACCOUNT}/ai/run/{CF_MODEL}"

# Pydantic Models
class Button(BaseModel):
    type: Literal["url", "quick_reply"]
    text: str
    url: Optional[str] = None

class MarketingMetrics(BaseModel):
    engagement_score: int = Field(description="Score from 0-100")
    readability: str = Field(description="Easy, Medium, or Hard")
    sentiment: str = Field(description="e.g., Professional, Urgent, Friendly")
    compliance_status: Literal["Safe", "Risk", "Rejected"]
    compliance_reason: str = Field(description="Why this status was given")

class WhatsAppTemplate(BaseModel):
    heading: str
    body: str
    image_prompt: str
    buttons: List[Button]
    metrics: MarketingMetrics

class TemplateRequest(BaseModel):
    user_input: str
    num_variations: int = 1

# LLM Instance with Structured Output
llm = ChatNVIDIA(
    api_key=NVIDIA_API_KEY,
    model="meta/llama-3.1-8b-instruct",
    temperature=0.3
).with_structured_output(WhatsAppTemplate)

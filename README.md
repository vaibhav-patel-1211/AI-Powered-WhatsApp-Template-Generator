# WhatsApp Marketing Template Generator 🚀

An AI-powered tool to generate high-converting, emoji-rich marketing templates for WhatsApp, complete with photorealistic image headers and one-click Meta verification.

![Project Screenshot](https://via.placeholder.com/800x450?text=WhatsApp+Generator+Dashboard)

## ✨ Features

-   **AI Copywriting**: Generates structured, persuasive body text with formatting (*bold*, _italic_) and emojis.
-   **Image Generation**: Creates context-aware, 16:9 photorealistic marketing images for headers.
-   **Demo Mode**: Simulates Meta's template verification process for testing/student use.
-   **Meta Integration** (Optional): Direct submission to Meta Graph API if credentials are provided.
-   **Multi-Variation**: Generate up to 20 variations at once.
-   **Download & Copy**: Copy text with formatting, or download a visual preview of the message card.

## 🛠️ Setup

### Prerequisites
- Python 3.10+
- `uvicorn` and required python packages.

### 1. Install Dependencies
```bash
pip install fastapi uvicorn requests python-dotenv langchain-nvidia-ai-endpoints langchain-core
```

### 2. Environment Variables
Create a `.env` file in the root directory:
```env
# Required for Text Generation
NVIDIA_API_KEY=your_nvidia_api_key
```
# Required for Image Generation
CLOUD_FLARE_API=your_cloudflare_api_token
ACCOUNT=your_cloudflare_account_id


### 3. Run the Application
```bash
uvicorn main:app --reload
```
The app will be available at: **http://127.0.0.1:8000/**

## 📖 Usage Guide

1.  **Enter a Prompt**: Describe your product (e.g., "Summer sale for a gym membership").
2.  **Select Variations**: Choose how many unique versions you want.
3.  **Generate**: Click the button and wait for AI to craft the content.
4.  **Review**: Scroll through the generated cards.
5.  **Submit/Copy**:
    -   Click "Auto-Submit" to send to Meta (or simulate it).
    -   Click "Copy Image" to copy the visual to your clipboard.
    -   Click "Copy Text" to copy the caption with formatting.
    -   Click "Download" to save a PNG preview.

## 🤝 Adding Cloudflare & Meta Keys
-   **Cloudflare Workers AI**: Get `ACCOUNT` ID from your URL bar in Cloudflare Dash, and create a Token with *Workers AI Read/Edit* permissions.
-   **Meta (Facebook)**: Using the App Dashboard, get your `WABA ID` and `System User Token`.

## 📜 License
Unlicensed (Student/Personal Use)

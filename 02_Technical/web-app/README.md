# Azərbaycan TTS — Web Application

A modern web application for Azerbaijani Text-to-Speech synthesis, powered by Microsoft Azure Cognitive Services Speech. Built with Next.js 15, Tailwind CSS 4, and deployed to Vercel.

## Features

- **Two neural voices** — Banu (female) and Babək (male)
- **Adjustable speech rate** — 5 speed levels from 0.7x to 1.3x
- **Custom audio player** — seekable progress bar, play/pause, waveform animation
- **Example sentences** — one-click Azerbaijani phrases
- **Responsive design** — mobile, tablet, and desktop
- **Keyboard shortcut** — Ctrl+Enter to synthesize

---

## Getting Azure Speech API Key

The app uses **Microsoft Azure AI Speech** (formerly Cognitive Services Speech) for neural voice synthesis.

### Step 1 — Create an Azure Account

1. Go to [https://azure.microsoft.com/free](https://azure.microsoft.com/free)
2. Click **Start free** and sign in with a Microsoft account (or create one)
3. Complete the sign-up — you get **$200 free credit** for 30 days, and the Speech free tier remains free after that

### Step 2 — Create a Speech Resource

1. Go to [Azure Portal](https://portal.azure.com)
2. Click **+ Create a resource** (top-left)
3. Search for **"Speech"** in the marketplace
4. Select **Speech** by Microsoft (under Azure AI services)
5. Click **Create**
6. Fill in the form:
   - **Subscription**: Your Azure subscription
   - **Resource group**: Create new or use existing (e.g., `tts-app-rg`)
   - **Region**: Pick one close to your users (e.g., `East US`, `West Europe`, or `North Europe`)
   - **Name**: Any unique name (e.g., `az-tts-speech`)
   - **Pricing tier**: **Free F0** (500K characters/month) or **Standard S0** (pay-as-you-go)
7. Click **Review + create**, then **Create**
8. Wait for deployment to complete (~30 seconds)

### Step 3 — Get Your Key and Region

1. Once deployed, click **Go to resource**
2. In the left sidebar, click **Keys and Endpoint**
3. Copy **KEY 1** (or KEY 2 — both work)
4. Note the **Location/Region** (e.g., `eastus`, `westeurope`)

> **Important**: The region must be the lowercase, no-spaces version (e.g., `eastus` not `East US`)

### Free Tier Limits

| Tier | Characters/Month | Neural Voices | Cost |
|------|:-----------------:|:-------------:|------|
| **F0 (Free)** | 500,000 | Yes | $0 |
| **S0 (Standard)** | Unlimited | Yes | $16 per 1M chars |

The free tier is more than enough for development and demos.

### Available Azerbaijani Voices

| Voice ID | Name | Gender |
|----------|------|--------|
| `az-AZ-BanuNeural` | Banu | Female |
| `az-AZ-BabekNeural` | Babək | Male |

---

## Local Development

### Prerequisites

- [Node.js](https://nodejs.org) 18+ installed
- An Azure Speech API key (see above)

### Setup

```bash
# Navigate to the web app
cd web-app

# Install dependencies
npm install

# Create environment file
cp .env.local.example .env.local
```

Edit `.env.local` with your Azure credentials:

```env
AZURE_SPEECH_KEY=your_key_here
AZURE_SPEECH_REGION=eastus
```

### Run

```bash
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) in your browser.

### Build

```bash
npm run build
npm start
```

---

## Deploy to Vercel

### Option A — Deploy via GitHub (Recommended)

#### 1. Push to GitHub

Make sure the `web-app/` directory is committed and pushed to your repository.

#### 2. Import to Vercel

1. Go to [https://vercel.com](https://vercel.com) and sign in with GitHub
2. Click **Add New → Project**
3. Select your repository: `ulvibashir/TTS-system-for-Azerbaijani-language`
4. In **Configure Project**:
   - **Root Directory**: Click **Edit** and set to `web-app`
   - **Framework Preset**: Next.js (auto-detected)
   - **Build Command**: `npm run build` (default)
   - **Output Directory**: `.next` (default)

#### 3. Add Environment Variables

Before clicking Deploy, expand **Environment Variables** and add:

| Key | Value |
|-----|-------|
| `AZURE_SPEECH_KEY` | Your Azure KEY 1 |
| `AZURE_SPEECH_REGION` | Your region (e.g., `eastus`) |

> **Never commit API keys to Git.** Vercel environment variables are encrypted and injected at build/runtime.

#### 4. Deploy

Click **Deploy**. Vercel will build and deploy your app. You'll get a URL like `https://your-project.vercel.app`.

### Option B — Deploy via Vercel CLI

```bash
# Install Vercel CLI
npm i -g vercel

# Navigate to web-app
cd web-app

# Deploy (follow prompts)
vercel

# Set environment variables
vercel env add AZURE_SPEECH_KEY
vercel env add AZURE_SPEECH_REGION

# Redeploy with env vars
vercel --prod
```

### Custom Domain (Optional)

1. In Vercel dashboard → your project → **Settings → Domains**
2. Add your custom domain
3. Update DNS records as instructed by Vercel

---

## Project Structure

```
web-app/
├── src/app/
│   ├── page.tsx              # Main UI — text input, controls, audio player
│   ├── layout.tsx            # Root layout, metadata, fonts
│   ├── globals.css           # Tailwind + custom animations
│   ├── icon.svg              # Favicon (gradient speaker icon)
│   └── api/synthesize/
│       └── route.ts          # Azure Speech REST API proxy
├── .env.local.example        # Environment variable template
├── .gitignore
├── package.json
├── tsconfig.json
├── next.config.ts
└── postcss.config.mjs
```

## Tech Stack

- **Next.js 15** — React framework with App Router
- **Tailwind CSS 4** — Utility-first styling
- **TypeScript** — Type safety
- **Azure AI Speech** — Neural TTS voices
- **Vercel** — Serverless deployment

---

## Troubleshooting

### "Azure Speech credentials not configured"
Your `.env.local` is missing or has placeholder values. Add your real key and region.

### "Speech synthesis failed" (401)
Your API key is invalid or expired. Regenerate it in Azure Portal → your Speech resource → Keys and Endpoint.

### "Speech synthesis failed" (403)
Your free tier quota may be exhausted, or the region doesn't match. Double-check `AZURE_SPEECH_REGION`.

### "Failed to connect to speech service" (502)
Network issue reaching Azure. Check your internet connection and that the region is correct.

### No sound plays
Check browser console for errors. Make sure your browser allows audio playback (some browsers block autoplay).

---

## License

Part of the master's dissertation project — UNEC 2026.

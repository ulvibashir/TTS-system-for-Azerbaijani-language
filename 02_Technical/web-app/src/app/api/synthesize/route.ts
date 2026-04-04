import { NextRequest, NextResponse } from "next/server";

export async function POST(req: NextRequest) {
  const { text, voice, speed } = await req.json();

  const key = process.env.AZURE_SPEECH_KEY;
  const region = process.env.AZURE_SPEECH_REGION;

  if (!key || !region || key === "your_azure_speech_key_here") {
    return NextResponse.json(
      {
        error:
          "Azure Speech API açarı konfiqurasiya edilməyib. .env.local faylına real API açarınızı əlavə edin.",
      },
      { status: 500 }
    );
  }

  if (!text || typeof text !== "string" || text.trim().length === 0) {
    return NextResponse.json({ error: "Text is required" }, { status: 400 });
  }

  if (text.length > 3000) {
    return NextResponse.json(
      { error: "Text must be under 3000 characters" },
      { status: 400 }
    );
  }

  const voiceName = voice || "az-AZ-BanuNeural";
  const rate = speed || "0%";

  const ssml = `
<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xml:lang="az-AZ">
  <voice name="${voiceName}">
    <prosody rate="${rate}">
      ${escapeXml(text.trim())}
    </prosody>
  </voice>
</speak>`.trim();

  try {
    const response = await fetch(
      `https://${region}.tts.speech.microsoft.com/cognitiveservices/v1`,
      {
        method: "POST",
        headers: {
          "Ocp-Apim-Subscription-Key": key,
          "Content-Type": "application/ssml+xml",
          "X-Microsoft-OutputFormat": "audio-24khz-96kbitrate-mono-mp3",
          "User-Agent": "AzTTS-WebApp",
        },
        body: ssml,
      }
    );

    if (!response.ok) {
      const errorText = await response.text();
      console.error("Azure TTS error:", response.status, errorText);
      return NextResponse.json(
        { error: "Speech synthesis failed" },
        { status: response.status }
      );
    }

    const audioBuffer = await response.arrayBuffer();

    return new NextResponse(audioBuffer, {
      headers: {
        "Content-Type": "audio/mpeg",
        "Content-Length": audioBuffer.byteLength.toString(),
      },
    });
  } catch (error) {
    console.error("Azure TTS request failed:", error);
    return NextResponse.json(
      { error: "Failed to connect to speech service" },
      { status: 502 }
    );
  }
}

function escapeXml(text: string): string {
  return text
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&apos;");
}

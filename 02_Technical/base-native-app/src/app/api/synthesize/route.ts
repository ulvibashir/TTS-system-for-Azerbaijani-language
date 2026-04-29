import { NextRequest, NextResponse } from "next/server";

export async function POST(req: NextRequest) {
  const { text, style, speed } = await req.json();

  const flaskUrl = process.env.FLASK_API_URL;

  if (!flaskUrl) {
    return NextResponse.json(
      { error: "FLASK_API_URL mühit dəyişəni konfiqurasiya edilməyib." },
      { status: 500 }
    );
  }

  if (!text || typeof text !== "string" || text.trim().length === 0) {
    return NextResponse.json({ error: "Mətn tələb olunur" }, { status: 400 });
  }

  if (text.length > 3000) {
    return NextResponse.json(
      { error: "Mətn 3000 simvoldan çox olmamalıdır" },
      { status: 400 }
    );
  }

  try {
    const response = await fetch(`${flaskUrl}/synthesize`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        text: text.trim(),
        style: style || "neutral",
        speed: speed || "1x",
      }),
    });

    if (!response.ok) {
      const err = await response.json().catch(() => ({}));
      return NextResponse.json(
        { error: (err as { error?: string }).error || "Sintez uğursuz oldu" },
        { status: response.status }
      );
    }

    const audioBuffer = await response.arrayBuffer();

    return new NextResponse(audioBuffer, {
      headers: {
        "Content-Type": "audio/wav",
        "Content-Length": audioBuffer.byteLength.toString(),
      },
    });
  } catch (error) {
    console.error("Flask API error:", error);
    return NextResponse.json(
      { error: "TTS serverinə qoşulmaq mümkün olmadı" },
      { status: 502 }
    );
  }
}

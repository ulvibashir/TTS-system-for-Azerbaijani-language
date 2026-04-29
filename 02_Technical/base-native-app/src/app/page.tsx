"use client";

import { useState, useRef, useEffect, useCallback } from "react";

const STYLES = [
  { id: "neutral", label: "Neytral" },
  { id: "formal", label: "Rəsmi" },
  { id: "conversational", label: "Danışıq" },
];

const SPEEDS = [
  { value: "0.7x", label: "0.7x" },
  { value: "0.85x", label: "0.85x" },
  { value: "1x", label: "1x" },
  { value: "1.15x", label: "1.15x" },
  { value: "1.3x", label: "1.3x" },
];

const EXAMPLES = [
  "Azərbaycan gözəl ölkədir.",
  "Bakı Xəzər dənizinin sahilində yerləşir.",
  "Bu gün hava çox gözəldir.",
  "Sənin adın nədir?",
  "Xoş gəlmisiniz!",
  "Kitabı oxumağı çox sevirəm.",
];

export default function Home() {
  const [text, setText] = useState("");
  const [style, setStyle] = useState(STYLES[0].id);
  const [speed, setSpeed] = useState("1x");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [isPlaying, setIsPlaying] = useState(false);
  const [hasAudio, setHasAudio] = useState(false);
  const [progress, setProgress] = useState(0);
  const [duration, setDuration] = useState(0);
  const audioRef = useRef<HTMLAudioElement>(null);
  const audioUrlRef = useRef<string | null>(null);
  const progressInterval = useRef<ReturnType<typeof setInterval> | null>(null);

  const clearProgress = useCallback(() => {
    if (progressInterval.current) {
      clearInterval(progressInterval.current);
      progressInterval.current = null;
    }
  }, []);

  useEffect(() => {
    return () => clearProgress();
  }, [clearProgress]);

  function startProgressTracking() {
    clearProgress();
    progressInterval.current = setInterval(() => {
      if (audioRef.current) {
        setProgress(audioRef.current.currentTime);
        setDuration(audioRef.current.duration || 0);
      }
    }, 100);
  }

  async function handleSynthesize() {
    if (!text.trim()) return;

    setLoading(true);
    setError("");
    setIsPlaying(false);
    setHasAudio(false);
    setProgress(0);
    clearProgress();

    if (audioUrlRef.current) {
      URL.revokeObjectURL(audioUrlRef.current);
      audioUrlRef.current = null;
    }

    try {
      const res = await fetch("/synthesize", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text, style, speed }),
      });

      if (!res.ok) {
        const data = await res.json().catch(() => ({}));
        throw new Error((data as { error?: string }).error || "Sintez uğursuz oldu");
      }

      const blob = await res.blob();
      const url = URL.createObjectURL(blob);
      audioUrlRef.current = url;

      if (audioRef.current) {
        audioRef.current.src = url;
        audioRef.current.play();
        setIsPlaying(true);
        setHasAudio(true);
        startProgressTracking();
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : "Xəta baş verdi");
    } finally {
      setLoading(false);
    }
  }

  function togglePlayPause() {
    if (!audioRef.current || !hasAudio) return;
    if (isPlaying) {
      audioRef.current.pause();
      setIsPlaying(false);
      clearProgress();
    } else {
      audioRef.current.play();
      setIsPlaying(true);
      startProgressTracking();
    }
  }

  function handleSeek(e: React.MouseEvent<HTMLDivElement>) {
    if (!audioRef.current || !duration) return;
    const rect = e.currentTarget.getBoundingClientRect();
    const ratio = (e.clientX - rect.left) / rect.width;
    audioRef.current.currentTime = ratio * duration;
    setProgress(ratio * duration);
  }

  function formatTime(s: number) {
    if (!s || !isFinite(s)) return "0:00";
    const m = Math.floor(s / 60);
    const sec = Math.floor(s % 60);
    return `${m}:${sec.toString().padStart(2, "0")}`;
  }

  const selectedStyle = STYLES.find((s) => s.id === style)!;

  return (
    <>
      {/* Background effects */}
      <div className="fixed inset-0 overflow-hidden pointer-events-none">
        <div className="absolute -top-40 -left-40 w-96 h-96 bg-emerald-600/10 rounded-full blur-[120px] animate-float" />
        <div className="absolute -bottom-40 -right-40 w-96 h-96 bg-teal-600/10 rounded-full blur-[120px] animate-float-delayed" />
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[600px] bg-emerald-600/5 rounded-full blur-[150px]" />
      </div>

      <main className="relative min-h-screen flex flex-col items-center justify-center px-4 py-8 sm:py-12">
        <div className="w-full max-w-2xl space-y-8 animate-fade-in-up">
          {/* Header */}
          <header className="text-center space-y-3">
            <div className="inline-flex items-center gap-2 bg-emerald-500/10 border border-emerald-500/20 rounded-full px-4 py-1.5 text-emerald-300 text-xs font-medium tracking-wide uppercase animate-fade-in-up">
              <span className="w-1.5 h-1.5 bg-emerald-400 rounded-full animate-pulse" />
              Qaydaya Əsaslanan TTS
            </div>
            <h1 className="text-4xl sm:text-5xl font-extrabold tracking-tight bg-gradient-to-r from-white via-emerald-100 to-teal-200 bg-clip-text text-transparent animate-fade-in-up delay-100">
              Azərbaycan TTS
            </h1>
            <p className="text-gray-400 text-sm sm:text-base max-w-md mx-auto animate-fade-in-up delay-200">
              Azərbaycan dilində mətni yazın, səsləndirin
            </p>
          </header>

          {/* Main Card */}
          <div className="glass rounded-3xl border border-white/[0.06] shadow-2xl shadow-emerald-500/5 p-5 sm:p-8 space-y-6 animate-fade-in-up delay-300">
            {/* Text Input */}
            <div className="relative group">
              <textarea
                value={text}
                onChange={(e) => setText(e.target.value)}
                onKeyDown={(e) => {
                  if (e.key === "Enter" && (e.ctrlKey || e.metaKey)) {
                    handleSynthesize();
                  }
                }}
                placeholder="Mətni bura yazın..."
                rows={4}
                maxLength={3000}
                className="w-full bg-white/[0.03] border border-white/[0.08] rounded-2xl p-4 sm:p-5 text-gray-100 placeholder-gray-500 focus:outline-none focus:border-emerald-500/40 focus:bg-white/[0.05] transition-all duration-300 resize-none text-base sm:text-lg leading-relaxed"
              />
              <div className="flex items-center justify-between mt-2 px-1">
                <span className="text-[11px] text-gray-600">
                  Ctrl+Enter ilə göndərin
                </span>
                <span
                  className={`text-[11px] transition-colors ${text.length > 2500 ? "text-amber-400" : "text-gray-600"}`}
                >
                  {text.length.toLocaleString()}/3,000
                </span>
              </div>
            </div>

            {/* Controls Row */}
            <div className="grid grid-cols-2 gap-3 sm:gap-4">
              {/* Style Selector */}
              <div>
                <label className="block text-[11px] text-gray-500 uppercase tracking-wider mb-2 font-medium">
                  Üslub
                </label>
                <div className="flex gap-2">
                  {STYLES.map((s) => (
                    <button
                      key={s.id}
                      onClick={() => setStyle(s.id)}
                      className={`flex-1 px-2 py-2.5 rounded-xl text-sm font-medium transition-all duration-200 cursor-pointer border ${
                        style === s.id
                          ? "bg-emerald-500/15 border-emerald-500/30 text-emerald-200 shadow-lg shadow-emerald-500/5"
                          : "bg-white/[0.03] border-white/[0.06] text-gray-400 hover:bg-white/[0.06] hover:text-gray-300"
                      }`}
                    >
                      {s.label}
                    </button>
                  ))}
                </div>
              </div>

              {/* Speed Selector */}
              <div>
                <label className="block text-[11px] text-gray-500 uppercase tracking-wider mb-2 font-medium">
                  Sürət
                </label>
                <div className="flex gap-1">
                  {SPEEDS.map((s) => (
                    <button
                      key={s.value}
                      onClick={() => setSpeed(s.value)}
                      className={`flex-1 py-2.5 rounded-xl text-xs font-medium transition-all duration-200 cursor-pointer border ${
                        speed === s.value
                          ? "bg-teal-500/15 border-teal-500/30 text-teal-200 shadow-lg shadow-teal-500/5"
                          : "bg-white/[0.03] border-white/[0.06] text-gray-400 hover:bg-white/[0.06] hover:text-gray-300"
                      }`}
                    >
                      {s.label}
                    </button>
                  ))}
                </div>
              </div>
            </div>

            {/* Synthesize Button */}
            <button
              onClick={handleSynthesize}
              disabled={loading || !text.trim()}
              className="group/btn relative w-full py-4 px-6 rounded-2xl font-semibold text-base transition-all duration-300 flex items-center justify-center gap-3 cursor-pointer disabled:cursor-not-allowed overflow-hidden bg-gradient-to-r from-emerald-600 to-teal-600 hover:from-emerald-500 hover:to-teal-500 disabled:from-gray-800 disabled:to-gray-800 text-white disabled:text-gray-500 shadow-lg shadow-emerald-500/20 hover:shadow-emerald-500/30 disabled:shadow-none active:scale-[0.98]"
            >
              <div className="absolute inset-0 bg-gradient-to-r from-emerald-400/20 to-teal-400/20 opacity-0 group-hover/btn:opacity-100 transition-opacity duration-300" />

              <span className="relative flex items-center gap-3">
                {loading ? (
                  <>
                    <svg
                      className="animate-spin h-5 w-5"
                      viewBox="0 0 24 24"
                      fill="none"
                    >
                      <circle
                        className="opacity-25"
                        cx="12"
                        cy="12"
                        r="10"
                        stroke="currentColor"
                        strokeWidth="4"
                      />
                      <path
                        className="opacity-75"
                        fill="currentColor"
                        d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"
                      />
                    </svg>
                    Sintez edilir...
                  </>
                ) : (
                  <>
                    <svg
                      className="h-5 w-5"
                      fill="none"
                      viewBox="0 0 24 24"
                      strokeWidth={2}
                      stroke="currentColor"
                    >
                      <path
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        d="M19.114 5.636a9 9 0 010 12.728M16.463 8.288a5.25 5.25 0 010 7.424M6.75 8.25l4.72-4.72a.75.75 0 011.28.53v15.88a.75.75 0 01-1.28.53l-4.72-4.72H4.51c-.88 0-1.704-.507-1.938-1.354A9.009 9.009 0 012.25 12c0-.83.112-1.633.322-2.396C2.806 8.756 3.63 8.25 4.51 8.25H6.75z"
                      />
                    </svg>
                    Dinlə
                  </>
                )}
              </span>
            </button>

            {/* Error */}
            {error && (
              <div className="flex items-start gap-3 bg-red-500/10 border border-red-500/20 text-red-300 rounded-xl px-4 py-3 text-sm animate-fade-in-up">
                <svg
                  className="w-5 h-5 shrink-0 mt-0.5"
                  fill="none"
                  viewBox="0 0 24 24"
                  strokeWidth={1.5}
                  stroke="currentColor"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    d="M12 9v3.75m9-.75a9 9 0 11-18 0 9 9 0 0118 0zm-9 3.75h.008v.008H12v-.008z"
                  />
                </svg>
                {error}
              </div>
            )}

            {/* Custom Audio Player */}
            {hasAudio && (
              <div className="bg-white/[0.03] border border-white/[0.06] rounded-2xl p-4 space-y-3 animate-fade-in-up">
                <div className="flex items-center gap-4">
                  {/* Play/Pause */}
                  <button
                    onClick={togglePlayPause}
                    className="w-10 h-10 flex items-center justify-center rounded-full bg-emerald-500/20 text-emerald-300 hover:bg-emerald-500/30 transition-all cursor-pointer shrink-0"
                  >
                    {isPlaying ? (
                      <svg
                        className="w-5 h-5"
                        fill="currentColor"
                        viewBox="0 0 24 24"
                      >
                        <path d="M6 4h4v16H6V4zm8 0h4v16h-4V4z" />
                      </svg>
                    ) : (
                      <svg
                        className="w-5 h-5 ml-0.5"
                        fill="currentColor"
                        viewBox="0 0 24 24"
                      >
                        <path d="M8 5v14l11-7z" />
                      </svg>
                    )}
                  </button>

                  {/* Progress */}
                  <div className="flex-1 space-y-2">
                    <div
                      className="relative h-1.5 bg-white/[0.06] rounded-full cursor-pointer group"
                      onClick={handleSeek}
                    >
                      <div
                        className="absolute inset-y-0 left-0 bg-gradient-to-r from-emerald-500 to-teal-500 rounded-full transition-all duration-100"
                        style={{
                          width: duration
                            ? `${(progress / duration) * 100}%`
                            : "0%",
                        }}
                      />
                      <div
                        className="absolute top-1/2 -translate-y-1/2 w-3 h-3 bg-white rounded-full shadow-lg opacity-0 group-hover:opacity-100 transition-opacity"
                        style={{
                          left: duration
                            ? `calc(${(progress / duration) * 100}% - 6px)`
                            : "0%",
                        }}
                      />
                    </div>
                    <div className="flex justify-between text-[10px] text-gray-500">
                      <span>{formatTime(progress)}</span>
                      <span>{formatTime(duration)}</span>
                    </div>
                  </div>

                  {/* Sound Wave Animation */}
                  {isPlaying && (
                    <div className="flex items-center gap-[3px] h-8">
                      {[...Array(5)].map((_, i) => (
                        <div
                          key={i}
                          className="w-[3px] bg-gradient-to-t from-emerald-500 to-teal-400 rounded-full wave-bar"
                          style={{ minHeight: 4 }}
                        />
                      ))}
                    </div>
                  )}
                </div>

                {/* Style info */}
                <div className="flex items-center gap-2 text-[11px] text-gray-500">
                  <div className="w-4 h-4 rounded-full bg-gradient-to-br from-emerald-500 to-teal-500 flex items-center justify-center">
                    <span className="text-[8px] text-white font-bold">
                      {selectedStyle.label[0]}
                    </span>
                  </div>
                  {selectedStyle.label} üslubu &middot; {speed}
                </div>
              </div>
            )}

            {/* Hidden audio element */}
            <audio
              ref={audioRef}
              className="hidden"
              onEnded={() => {
                setIsPlaying(false);
                clearProgress();
              }}
              onLoadedMetadata={() => {
                if (audioRef.current) {
                  setDuration(audioRef.current.duration);
                }
              }}
            />
          </div>

          {/* Example Sentences */}
          <div className="space-y-3 animate-fade-in-up delay-400">
            <p className="text-[11px] text-gray-500 uppercase tracking-widest font-medium px-1">
              Nümunə cümlələr
            </p>
            <div className="flex flex-wrap gap-2">
              {EXAMPLES.map((ex) => (
                <button
                  key={ex}
                  onClick={() => setText(ex)}
                  className="glass border border-white/[0.06] hover:border-white/[0.12] text-gray-400 hover:text-gray-200 text-sm px-3.5 py-2 rounded-xl transition-all duration-200 cursor-pointer hover:bg-white/[0.04]"
                >
                  {ex}
                </button>
              ))}
            </div>
          </div>

          {/* Footer */}
          <footer className="text-center space-y-1 pt-4">
            <p className="text-[11px] text-gray-600">
              Magistr dissertasiyası &middot; UNEC 2026
            </p>
            <p className="text-[10px] text-gray-700">
              Azərbaycan dili üçün qaydaya əsaslanan mətndən nitqə sintezi
              sistemi
            </p>
          </footer>
        </div>
      </main>
    </>
  );
}

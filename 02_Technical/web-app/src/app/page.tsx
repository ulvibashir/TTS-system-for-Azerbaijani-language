"use client";

import { useState, useRef, useEffect, useCallback } from "react";

const TRANSLATIONS = {
  az: {
    badge: "Azure Neural TTS",
    title: "Azərbaycan TTS",
    subtitle: "Azərbaycan dilində mətni yazın, səsləndirin",
    placeholder: "Mətni bura yazın...",
    hint: "Ctrl+Enter ilə göndərin",
    voiceLabel: "Səs",
    speedLabel: "Sürət",
    listenBtn: "Dinlə",
    synthesizing: "Sintez edilir...",
    examplesLabel: "Nümunə cümlələr",
    footer1: "Magistr dissertasiyası · UNEC 2026",
    footer2: "Azərbaycan dili üçün mətndən nitqə sintezi sistemi",
    madeBy: "Ulvi Bashirov tərəfindən",
    genderF: "Qadın",
    genderM: "Kişi",
    dot: "·",
  },
  en: {
    badge: "Azure Neural TTS",
    title: "Azerbaijani TTS",
    subtitle: "Type in Azerbaijani and listen",
    placeholder: "Type text here...",
    hint: "Send with Ctrl+Enter",
    voiceLabel: "Voice",
    speedLabel: "Speed",
    listenBtn: "Listen",
    synthesizing: "Synthesizing...",
    examplesLabel: "Example sentences",
    footer1: "Master's Dissertation · UNEC 2026",
    footer2: "Text-to-speech synthesis system for the Azerbaijani language",
    madeBy: "by Ulvi Bashirov",
    genderF: "Female",
    genderM: "Male",
    dot: "·",
  },
};

const VOICES = [
  { id: "az-AZ-BanuNeural", label: "Banu", genderKey: "genderF" as const },
  { id: "az-AZ-BabekNeural", label: "Babək", genderKey: "genderM" as const },
];

const SPEEDS = [
  { value: "-30%", label: "0.7x" },
  { value: "-15%", label: "0.85x" },
  { value: "0%", label: "1x" },
  { value: "+15%", label: "1.15x" },
  { value: "+30%", label: "1.3x" },
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
  const [voice, setVoice] = useState(VOICES[0].id);
  const [speed, setSpeed] = useState("0%");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [isPlaying, setIsPlaying] = useState(false);
  const [hasAudio, setHasAudio] = useState(false);
  const [progress, setProgress] = useState(0);
  const [duration, setDuration] = useState(0);
  const [theme, setTheme] = useState<"dark" | "light">("dark");
  const [lang, setLang] = useState<"az" | "en">("az");
  const audioRef = useRef<HTMLAudioElement>(null);
  const audioUrlRef = useRef<string | null>(null);
  const progressInterval = useRef<ReturnType<typeof setInterval> | null>(null);

  const t = TRANSLATIONS[lang];
  const isDark = theme === "dark";

  const clearProgress = useCallback(() => {
    if (progressInterval.current) {
      clearInterval(progressInterval.current);
      progressInterval.current = null;
    }
  }, []);

  useEffect(() => () => clearProgress(), [clearProgress]);

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
    if (audioUrlRef.current) { URL.revokeObjectURL(audioUrlRef.current); audioUrlRef.current = null; }

    try {
      const res = await fetch("/api/synthesize", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text, voice, speed }),
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
    if (isPlaying) { audioRef.current.pause(); setIsPlaying(false); clearProgress(); }
    else { audioRef.current.play(); setIsPlaying(true); startProgressTracking(); }
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
    return `${Math.floor(s / 60)}:${Math.floor(s % 60).toString().padStart(2, "0")}`;
  }

  const selectedVoice = VOICES.find((v) => v.id === voice)!;

  // ── Theme-aware class helpers ──────────────────────────────────────────────
  const pageBg    = isDark ? "bg-[#06060f]"  : "bg-[#f0f4ff]";
  const cardBg    = isDark ? "glass"          : "glass-light border-blue-200/60";
  const textMain  = isDark ? "text-gray-100"  : "text-gray-900";
  const textSub   = isDark ? "text-gray-400"  : "text-gray-500";
  const textMuted = isDark ? "text-gray-600"  : "text-gray-400";
  const badgeCls  = isDark
    ? "bg-blue-500/10 border-blue-500/20 text-blue-300"
    : "bg-blue-100 border-blue-300 text-blue-700";
  const dotCls    = isDark ? "bg-blue-400" : "bg-blue-500";
  const titleGrad = isDark
    ? "from-white via-blue-100 to-violet-200"
    : "from-blue-800 via-blue-600 to-violet-600";
  const inputCls  = isDark
    ? "bg-white/[0.03] border-white/[0.08] text-gray-100 placeholder-gray-500 focus:border-blue-500/40 focus:bg-white/[0.05]"
    : "bg-white border-gray-200 text-gray-900 placeholder-gray-400 focus:border-blue-400 focus:bg-white";
  const activeVoice = isDark
    ? "bg-blue-500/15 border-blue-500/30 text-blue-200 shadow-lg shadow-blue-500/5"
    : "bg-blue-100 border-blue-400 text-blue-800";
  const inactiveBtn = isDark
    ? "bg-white/[0.03] border-white/[0.06] text-gray-400 hover:bg-white/[0.06] hover:text-gray-300"
    : "bg-white border-gray-200 text-gray-500 hover:bg-gray-50 hover:text-gray-700";
  const activeSpeed = isDark
    ? "bg-violet-500/15 border-violet-500/30 text-violet-200 shadow-lg shadow-violet-500/5"
    : "bg-violet-100 border-violet-400 text-violet-800";
  const playerBg  = isDark ? "bg-white/[0.03] border-white/[0.06]" : "bg-white border-gray-200";
  const playBtn   = isDark
    ? "bg-blue-500/20 text-blue-300 hover:bg-blue-500/30"
    : "bg-blue-100 text-blue-600 hover:bg-blue-200";
  const exampleBtn = isDark
    ? "glass border-white/[0.06] hover:border-white/[0.12] text-gray-400 hover:text-gray-200 hover:bg-white/[0.04]"
    : "bg-white border-gray-200 hover:border-blue-300 text-gray-500 hover:text-gray-800";
  const controlBtn = isDark
    ? "bg-white/[0.05] border-white/[0.08] text-gray-300 hover:bg-white/[0.1]"
    : "bg-white border-gray-200 text-gray-600 hover:bg-gray-50";
  const orb1 = isDark ? "bg-blue-600/10"   : "bg-blue-300/20";
  const orb2 = isDark ? "bg-violet-600/10" : "bg-violet-300/20";
  const orb3 = isDark ? "bg-indigo-600/5"  : "bg-indigo-200/30";

  return (
    <div className={`${pageBg} ${textMain} min-h-screen transition-colors duration-300`}>
      {/* Background orbs */}
      <div className="fixed inset-0 overflow-hidden pointer-events-none">
        <div className={`absolute -top-40 -left-40 w-96 h-96 ${orb1} rounded-full blur-[120px] animate-float`} />
        <div className={`absolute -bottom-40 -right-40 w-96 h-96 ${orb2} rounded-full blur-[120px] animate-float-delayed`} />
        <div className={`absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[600px] ${orb3} rounded-full blur-[150px]`} />
      </div>

      {/* Top-right controls */}
      <div className="fixed top-4 right-4 flex gap-2 z-50">
        <button
          onClick={() => setLang(lang === "az" ? "en" : "az")}
          className={`px-3 py-1.5 rounded-full text-xs font-semibold border transition-all duration-200 cursor-pointer ${controlBtn}`}
        >
          {lang === "az" ? "ENG" : "AZE"}
        </button>
        <button
          onClick={() => setTheme(isDark ? "light" : "dark")}
          className={`w-8 h-8 flex items-center justify-center rounded-full border transition-all duration-200 cursor-pointer ${controlBtn}`}
        >
          {isDark ? (
            <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 24 24">
              <path d="M12 3a9 9 0 1 0 9 9c0-.46-.04-.92-.1-1.36a5.389 5.389 0 0 1-4.4 2.26 5.403 5.403 0 0 1-3.14-9.8c-.44-.06-.9-.1-1.36-.1z"/>
            </svg>
          ) : (
            <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 24 24">
              <path d="M12 7a5 5 0 1 0 0 10A5 5 0 0 0 12 7zm0-2a1 1 0 0 0 1-1V2a1 1 0 0 0-2 0v2a1 1 0 0 0 1 1zm0 16a1 1 0 0 0-1 1v2a1 1 0 0 0 2 0v-2a1 1 0 0 0-1-1zm9-9h-2a1 1 0 0 0 0 2h2a1 1 0 0 0 0-2zM5 12a1 1 0 0 0-1-1H2a1 1 0 0 0 0 2h2a1 1 0 0 0 1-1zm11.95-6.364-1.414 1.414a1 1 0 1 0 1.414 1.414l1.414-1.414a1 1 0 0 0-1.414-1.414zM6.464 17.536 5.05 18.95a1 1 0 1 0 1.414 1.414l1.414-1.414a1 1 0 0 0-1.414-1.414zm12.072 1.414-1.414-1.414a1 1 0 0 0-1.414 1.414l1.414 1.414a1 1 0 0 0 1.414-1.414zM7.878 7.05 6.464 5.636A1 1 0 0 0 5.05 7.05l1.414 1.414A1 1 0 1 0 7.878 7.05z"/>
            </svg>
          )}
        </button>
      </div>

      <main className="relative min-h-screen flex flex-col items-center justify-center px-4 py-8 sm:py-12">
        <div className="w-full max-w-2xl space-y-8 animate-fade-in-up">

          {/* Header */}
          <header className="text-center space-y-3">
            <div className={`inline-flex items-center gap-2 ${badgeCls} border rounded-full px-4 py-1.5 text-xs font-medium tracking-wide uppercase animate-fade-in-up`}>
              <span className={`w-1.5 h-1.5 ${dotCls} rounded-full animate-pulse`} />
              {t.badge}
            </div>
            <h1 className={`text-4xl sm:text-5xl font-extrabold tracking-tight bg-gradient-to-r ${titleGrad} bg-clip-text text-transparent animate-fade-in-up delay-100`}>
              {t.title}
            </h1>
            <p className={`${textSub} text-sm sm:text-base max-w-md mx-auto animate-fade-in-up delay-200`}>
              {t.subtitle}
            </p>
          </header>

          {/* Main Card */}
          <div className={`${cardBg} rounded-3xl border shadow-2xl shadow-blue-500/5 p-5 sm:p-8 space-y-6 animate-fade-in-up delay-300`}>
            {/* Textarea */}
            <div className="relative group">
              <textarea
                value={text}
                onChange={(e) => setText(e.target.value)}
                onKeyDown={(e) => { if (e.key === "Enter" && (e.ctrlKey || e.metaKey)) handleSynthesize(); }}
                placeholder={t.placeholder}
                rows={4}
                maxLength={3000}
                className={`w-full ${inputCls} border rounded-2xl p-4 sm:p-5 focus:outline-none transition-all duration-300 resize-none text-base sm:text-lg leading-relaxed`}
              />
              <div className="flex items-center justify-between mt-2 px-1">
                <span className={`text-[11px] ${textMuted}`}>{t.hint}</span>
                <span className={`text-[11px] transition-colors ${text.length > 2500 ? "text-amber-400" : textMuted}`}>
                  {text.length.toLocaleString()}/3,000
                </span>
              </div>
            </div>

            {/* Controls */}
            <div className="grid grid-cols-2 gap-3 sm:gap-4">
              <div>
                <label className={`block text-[11px] ${textMuted} uppercase tracking-wider mb-2 font-medium`}>{t.voiceLabel}</label>
                <div className="flex gap-2">
                  {VOICES.map((v) => (
                    <button key={v.id} onClick={() => setVoice(v.id)}
                      className={`flex-1 px-3 py-2.5 rounded-xl text-sm font-medium transition-all duration-200 cursor-pointer border ${voice === v.id ? activeVoice : inactiveBtn}`}>
                      <div className="text-center">
                        <div>{v.label}</div>
                        <div className="text-[10px] opacity-60">{t[v.genderKey]}</div>
                      </div>
                    </button>
                  ))}
                </div>
              </div>
              <div>
                <label className={`block text-[11px] ${textMuted} uppercase tracking-wider mb-2 font-medium`}>{t.speedLabel}</label>
                <div className="flex gap-1">
                  {SPEEDS.map((s) => (
                    <button key={s.value} onClick={() => setSpeed(s.value)}
                      className={`flex-1 py-2.5 rounded-xl text-xs font-medium transition-all duration-200 cursor-pointer border ${speed === s.value ? activeSpeed : inactiveBtn}`}>
                      {s.label}
                    </button>
                  ))}
                </div>
              </div>
            </div>

            {/* Synthesize Button */}
            <button onClick={handleSynthesize} disabled={loading || !text.trim()}
              className="group/btn relative w-full py-4 px-6 rounded-2xl font-semibold text-base transition-all duration-300 flex items-center justify-center gap-3 cursor-pointer disabled:cursor-not-allowed overflow-hidden bg-gradient-to-r from-blue-600 to-violet-600 hover:from-blue-500 hover:to-violet-500 disabled:from-gray-400 disabled:to-gray-400 text-white shadow-lg shadow-blue-500/20 hover:shadow-blue-500/30 disabled:shadow-none active:scale-[0.98]">
              <div className="absolute inset-0 bg-gradient-to-r from-blue-400/20 to-violet-400/20 opacity-0 group-hover/btn:opacity-100 transition-opacity duration-300" />
              <span className="relative flex items-center gap-3">
                {loading ? (
                  <>
                    <svg className="animate-spin h-5 w-5" viewBox="0 0 24 24" fill="none">
                      <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"/>
                      <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"/>
                    </svg>
                    {t.synthesizing}
                  </>
                ) : (
                  <>
                    <svg className="h-5 w-5" fill="none" viewBox="0 0 24 24" strokeWidth={2} stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" d="M19.114 5.636a9 9 0 010 12.728M16.463 8.288a5.25 5.25 0 010 7.424M6.75 8.25l4.72-4.72a.75.75 0 011.28.53v15.88a.75.75 0 01-1.28.53l-4.72-4.72H4.51c-.88 0-1.704-.507-1.938-1.354A9.009 9.009 0 012.25 12c0-.83.112-1.633.322-2.396C2.806 8.756 3.63 8.25 4.51 8.25H6.75z"/>
                    </svg>
                    {t.listenBtn}
                  </>
                )}
              </span>
            </button>

            {/* Error */}
            {error && (
              <div className="flex items-start gap-3 bg-red-500/10 border border-red-500/20 text-red-400 rounded-xl px-4 py-3 text-sm animate-fade-in-up">
                <svg className="w-5 h-5 shrink-0 mt-0.5" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" d="M12 9v3.75m9-.75a9 9 0 11-18 0 9 9 0 0118 0zm-9 3.75h.008v.008H12v-.008z"/>
                </svg>
                {error}
              </div>
            )}

            {/* Audio Player */}
            {hasAudio && (
              <div className={`${playerBg} border rounded-2xl p-4 space-y-3 animate-fade-in-up`}>
                <div className="flex items-center gap-4">
                  <button onClick={togglePlayPause} className={`w-10 h-10 flex items-center justify-center rounded-full ${playBtn} transition-all cursor-pointer shrink-0`}>
                    {isPlaying
                      ? <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 24 24"><path d="M6 4h4v16H6V4zm8 0h4v16h-4V4z"/></svg>
                      : <svg className="w-5 h-5 ml-0.5" fill="currentColor" viewBox="0 0 24 24"><path d="M8 5v14l11-7z"/></svg>}
                  </button>
                  <div className="flex-1 space-y-2">
                    <div className={`relative h-1.5 ${isDark ? "bg-white/[0.06]" : "bg-gray-200"} rounded-full cursor-pointer group`} onClick={handleSeek}>
                      <div className="absolute inset-y-0 left-0 bg-gradient-to-r from-blue-500 to-violet-500 rounded-full transition-all duration-100"
                        style={{ width: duration ? `${(progress / duration) * 100}%` : "0%" }}/>
                      <div className="absolute top-1/2 -translate-y-1/2 w-3 h-3 bg-white rounded-full shadow-lg opacity-0 group-hover:opacity-100 transition-opacity"
                        style={{ left: duration ? `calc(${(progress / duration) * 100}% - 6px)` : "0%" }}/>
                    </div>
                    <div className={`flex justify-between text-[10px] ${textMuted}`}>
                      <span>{formatTime(progress)}</span>
                      <span>{formatTime(duration)}</span>
                    </div>
                  </div>
                  {isPlaying && (
                    <div className="flex items-center gap-[3px] h-8">
                      {[...Array(5)].map((_, i) => (
                        <div key={i} className="w-[3px] bg-gradient-to-t from-blue-500 to-violet-400 rounded-full wave-bar" style={{ minHeight: 4 }}/>
                      ))}
                    </div>
                  )}
                </div>
                <div className={`flex items-center gap-2 text-[11px] ${textMuted}`}>
                  <div className="w-4 h-4 rounded-full bg-gradient-to-br from-blue-500 to-violet-500 flex items-center justify-center">
                    <span className="text-[8px] text-white font-bold">{selectedVoice.label[0]}</span>
                  </div>
                  {selectedVoice.label} ({t[selectedVoice.genderKey]}) {t.dot} {SPEEDS.find((s) => s.value === speed)?.label}
                </div>
              </div>
            )}

            <audio ref={audioRef} className="hidden"
              onEnded={() => { setIsPlaying(false); clearProgress(); }}
              onLoadedMetadata={() => { if (audioRef.current) setDuration(audioRef.current.duration); }}/>
          </div>

          {/* Examples */}
          <div className="space-y-3 animate-fade-in-up delay-400">
            <p className={`text-[11px] ${textMuted} uppercase tracking-widest font-medium px-1`}>{t.examplesLabel}</p>
            <div className="flex flex-wrap gap-2">
              {EXAMPLES.map((ex) => (
                <button key={ex} onClick={() => setText(ex)}
                  className={`${exampleBtn} border text-sm px-3.5 py-2 rounded-xl transition-all duration-200 cursor-pointer`}>
                  {ex}
                </button>
              ))}
            </div>
          </div>

          {/* Footer */}
          <footer className="text-center space-y-1 pt-4">
            <p className={`text-[11px] ${textMuted}`}>{t.footer1}</p>
            <p className={`text-[11px] ${isDark ? "text-gray-700" : "text-gray-400"}`}>{t.footer2}</p>
            <p className={`text-[11px] font-medium ${isDark ? "text-blue-700/60" : "text-blue-600/70"}`}>{t.madeBy}</p>
          </footer>
        </div>
      </main>
    </div>
  );
}

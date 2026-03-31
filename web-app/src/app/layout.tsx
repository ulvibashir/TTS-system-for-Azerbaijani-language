import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Azərbaycan TTS — Mətndən Nitqə",
  description:
    "Azərbaycan dili üçün mətndən nitqə sintezi sistemi. UNEC magistr dissertasiyası.",
  icons: {
    icon: "/icon.svg",
  },
  openGraph: {
    title: "Azərbaycan TTS — Mətndən Nitqə",
    description:
      "Azərbaycan dili üçün mətndən nitqə sintezi sistemi.",
    type: "website",
  },
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="az">
      <head>
        <link
          href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap"
          rel="stylesheet"
        />
      </head>
      <body className="bg-[#07070f] text-gray-100 min-h-screen antialiased font-sans overflow-x-hidden">
        {children}
      </body>
    </html>
  );
}

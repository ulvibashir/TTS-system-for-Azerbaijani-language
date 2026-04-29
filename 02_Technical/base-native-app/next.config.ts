import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  output: "export",   // generates static files in /out — served by Flask
};

export default nextConfig;

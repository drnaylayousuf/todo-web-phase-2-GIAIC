import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  // Disable experimental features that might trigger Turbopack
  experimental: {
    turbo: false,
    serverSourceMaps: true,
  },
  // Ensure Tailwind CSS works properly
  transpilePackages: [],
};

export default nextConfig;
import path from 'path';
import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  // Ensure Tailwind CSS works properly
  transpilePackages: [],
  experimental: {
    serverSourceMaps: true,
  },
};

export default nextConfig;
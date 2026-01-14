import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  // Ensure Tailwind CSS works properly
  transpilePackages: [],
  experimental: {
    serverSourceMaps: true,
  },
  // Explicitly define the basePath to ensure consistent path resolution
  basePath: '',
  // Ensure assetPrefix is empty to avoid conflicts
  assetPrefix: '',
};

export default nextConfig;
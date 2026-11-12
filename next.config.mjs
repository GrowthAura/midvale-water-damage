/** @type {import('next').NextConfig} */
const nextConfig = {
  output: "export",
  trailingSlash: false,
  basePath: "/midvale-water-damage",
  assetPrefix: "/midvale-water-damage",
  images: { unoptimized: true },
};
export default nextConfig;

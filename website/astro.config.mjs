import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';

// Set `site` to your real domain before deploying (needed for RSS + sitemap).
export default defineConfig({
  site: 'https://powertothemicrobes.org',
  integrations: [sitemap()],
});

import adapter from '@sveltejs/adapter-vercel';
import { vitePreprocess } from '@sveltejs/vite-plugin-svelte';
/** @type {import('@sveltejs/kit').Config} */
const config = {
  kit: {
    adapter: adapter(),
    csp: {
      mode: 'hash',
      directives: {
        'script-src': ['self', 'unsafe-eval', 'https://us-assets.i.posthog.com', 'https://vercel.live'],
        'connect-src': ['self', 'https://us.i.posthog.com', 'https://us-assets.i.posthog.com', 'https://uc-investments-80f94956a47a.herokuapp.com', 'https://vitals.vercel-analytics.com'],
        'img-src': ['self', 'data:', 'https:'],
        'style-src': ['self', 'unsafe-inline', 'https://fonts.googleapis.com'],
        'font-src': ['self', 'https://fonts.gstatic.com'],
        'frame-src': ['self'],
        'object-src': ['none'],
        'base-uri': ['self']
      }
    }
  },
  preprocess: vitePreprocess()
};
export default config;
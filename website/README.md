# Power to the Microbes (website)

Static site built with [Astro](https://astro.build). Content is plain Markdown.

```bash
npm install
npm run dev      # http://localhost:4321
npm run build    # output in dist/
```

## Add content
- New article: `src/content/articles/my-title.md`
- New blog post: `src/content/blog/my-title.md`
- Frontmatter: `title`, `summary`, `date`, `topic`, `tags`, `level`, `draft` (see `src/content.config.ts`)
- Add/rename topics in `src/topics.ts`

## Deploy
Push to GitHub and connect Cloudflare Pages / Netlify / GitHub Pages
(build command `npm run build`, output dir `dist`). Set `site` in `astro.config.mjs`.

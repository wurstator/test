import rss from '@astrojs/rss';
import { getCollection } from 'astro:content';

// RSS feed of blog posts + articles, newest first.
export async function GET(context) {
  const pub = (e) => !e.data.draft;
  const items = [
    ...(await getCollection('blog', pub)).map((e) => ({ e, base: 'blog' })),
    ...(await getCollection('articles', pub)).map((e) => ({ e, base: 'articles' })),
  ].sort((a, b) => +b.e.data.date - +a.e.data.date);
  return rss({
    title: 'Power to the Microbes',
    description: 'Microbial biotechnology, explained.',
    site: context.site,
    items: items.map(({ e, base }) => ({ title: e.data.title, description: e.data.summary, pubDate: e.data.date, link: `/${base}/${e.id}/` })),
  });
}

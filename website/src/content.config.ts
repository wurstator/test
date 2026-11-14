// Content collections: every .md file in these folders is validated against the schema.
import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';
import { TOPIC_IDS } from './topics';

const schema = z.object({
  title: z.string(),
  summary: z.string(),                                   // one-sentence teaser
  date: z.coerce.date(),
  topic: z.enum(TOPIC_IDS),                              // must match a topic in topics.ts
  tags: z.array(z.string()).default([]),
  level: z.enum(['beginner', 'intermediate', 'advanced']).default('beginner'),
  draft: z.boolean().default(false),                     // drafts are hidden from the site
});

const load = (dir: string) => glob({ pattern: '**/*.md', base: `./src/content/${dir}` });

export const collections = {
  articles: defineCollection({ loader: load('articles'), schema }), // evergreen, by topic
  blog: defineCollection({ loader: load('blog'), schema }),         // timely, by date
};

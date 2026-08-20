import { defineCollection, z } from 'astro:content';
import { docsLoader } from '@astrojs/starlight/loaders';
import { docsSchema } from '@astrojs/starlight/schema';

export const collections = {
  docs: defineCollection({
    loader: docsLoader(),
    schema: docsSchema({
      // Extra frontmatter fields every topic page in this atlas can use.
      extend: z.object({
        /** Rough reading time in minutes, shown in the page header. */
        readingTime: z.number().optional(),
        /** Highest depth tier the page reaches. Drives the header badge. */
        depth: z
          .enum(['intuition', 'mechanics', 'formal', 'frontier'])
          .default('frontier'),
        /** Slugs the reader should ideally have read first. */
        prereqs: z
          .array(z.object({ label: z.string(), slug: z.string() }))
          .default([]),
        /** Papers this page is built on. Rendered as a citation block. */
        papers: z
          .array(
            z.object({
              title: z.string(),
              authors: z.string(),
              year: z.number(),
              url: z.string().url(),
            })
          )
          .default([]),
      }),
    }),
  }),
};

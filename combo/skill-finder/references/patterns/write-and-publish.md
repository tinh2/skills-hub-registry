# Pattern: write-and-publish

Draft a blog post and publish it through the WordPress pipeline.

## Trigger Phrases

* write a blog post
* write and publish
* draft a post
* publish a post
* blog about
* publish to the site

## Required Steps

1. **blog-writer.** Skill: `skills-hub-registry-blog-writer`. Purpose: draft the post.
2. **wp-publish.** Skill: `wp-publish`. Purpose: publish to WordPress with SEO and verification.

## Handoff Notes

* blog-writer to wp-publish: pass the draft path, target slug, and tags.

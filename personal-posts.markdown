---
layout: archive
title: "Personal Blog"
permalink: /personal-posts/
author_profile: true
---

These posts are more typical personal blog posts, mostly written when I was an
undergrad during the pandemic.

{% assign personal_posts = site.categories.Personal %}

<div class="entries-grid">
  {% for post in personal_posts %}
    {% include archive-single.html %}
  {% endfor %}
</div>

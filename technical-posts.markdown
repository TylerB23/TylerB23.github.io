---
layout: archive
title: "Technical Posts"
permalink: /technical-posts/
author_profile: true
---

These posts tend to focus on math and computer science topics, especially
related to finance.

{% assign technical_posts = site.categories.Technical %}

<div class="entries-grid">
  {% for post in technical_posts %}
    {% include archive-single.html %}
  {% endfor %}
</div>

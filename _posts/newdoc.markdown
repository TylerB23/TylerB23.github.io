---
layout: post
title: "test post"
date: 2020-06-17
---
This is a markdown file. 

## Hello! ##

this is a link: [blue underlined text](www.google.com/)

Here's info on testing the site locally:

{% highlight bash %}
gem install jekyll bundler
#if necessary:
export PATH="/home/tylerb/.gem/ruby/2.7.0/bin:$PATH"

bundle exec jekyll build
bundle exec jekyll serve
{% endhighlight %}

Here's an image: ![internal title](/assets/image.png)



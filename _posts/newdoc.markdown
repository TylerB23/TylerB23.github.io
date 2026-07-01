---
layout: post
categories: Technical, Personal
title: "test post"
header:
    overlay_image: /assets/Allen-Memorial-Library.jpg
    overlay_filter: 0.1
toc: true
---
This is a markdown file. 

## Major Section with Underline ##

I can write *italicized text* or **bold text**. I can make unordered lists:

- Item
- Item
- Item

Or ordered lists:

1. Item
2. Item
3. Item

### Minor Section without Underline ### 

this is a link: [blue underlined text](www.google.com/)

Here's an image: ![internal title](/assets/image.png)

Inline LaTeX is like $f(x) = x^2$. A block is like this:

$$
\frac{a}{b} = 1 \\
a = b
$$

Inline code is like `this`. A block is like this:

```python
import numpy as np

def myFunction(text):
    print(f"here's your text: {text}")
    return
```

Here's info on testing the site locally:

{% highlight bash %}
gem install jekyll bundler
#if necessary:
export PATH="/home/tylerb/.gem/ruby/2.7.0/bin:$PATH"

bundle exec jekyll build
bundle exec jekyll serve
{% endhighlight %}

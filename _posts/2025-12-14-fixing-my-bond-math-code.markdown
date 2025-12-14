---
layout: post
title: "Fixing my Bond Math Code from the Last Post"
header:
    overlay_image: /assets/Dutch_Bond.jpg
    overlay_filter: 0
---
While playing around with the Python I wrote in my last blog post, I realized
that it had a fatal error. Muni bonds are typically sold in \\$5,000 lots, so in
my first attempt I tried to deal with this by taking the floor of my calculated
principal amounts element-wise. However, by doing that I ended up reducing the
interest that needed to be paid in earlier periods, since I was reducing the
principal due in later periods by rounding down. That meant that, especially for
longer maturities, my solutions weren't solving for debt service up to the full
revenue constraint. Whoops.

Adding the wrinkle of bond denominations makes the problem much less elegant;
we're no longer just solving a system of linear equations. There's still a lot
we can learn from the linear algebra approach, however; we'll just ignore
denominations for now to build up some intuition. 

Anyways, I've written below two bond model solving functions. The first takes
the same approach as last time, but without the rounding. This means that we can
get "weird" amounts of principal, but I think it's still analytically
interesting. The second mirrors what I do in Excel at work. It solves for each
year's principal and interest sequentially, starting from the maturity date of
the bonds. It's much more practical, but not as analytically tractable.

{% highlight python %}
import numpy as np
import pandas as pd

def simple_solve(n, R, r):

    # n is the number of periods
    # R is the annual revenue constraint
    # r is the coupon rate

    # First, create coefficients matrix

    A = (1 + r) * np.eye(n) + r * np.triu(np.ones([n,n]),1)

    # Next, create vector R of revenues

    R = R * np.ones(n)

    # Next, solve

    principal = np.linalg.solve(A,R)
    
    # Calculate the interest for each year
    interest = np.zeros(n)
    for i in range(n):
        interest[n-i-1] = sum(P[-i-1:]) * c
    
    return principal, interest
    
def better_solve(n, R, r):

    # n is the number of periods
    # R is the revenue constraint
    # r is the coupon rate

    # Create our principal and interest arrays
    principal = np.zeros(n)
    interest = np.zeros(n)

    # Calculate the last year's principal and interest
    # I'm creating the arrays backwards because it makes the indexing easier
    # the '.T' at the end flips them so the first entry is the first year
    principal[0] = np.floor((r / (1 + c)) / 5000) * 5000
    interest[0] = principal[0] * c
    for i in range(n-1):
        principal[i+1] = np.floor(((r - interest[i]) / (1 + c)) / 5000) * 5000
        interest[i+1] = interest[i] + principal[i+1] * c

    return principal.T, interest.T

{% endhighlight %}


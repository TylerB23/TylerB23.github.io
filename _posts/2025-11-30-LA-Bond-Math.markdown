---
layout: post
title: "Using Linear Algebra for Bond Math"
header:
    overlay_image: /assets/Dutch_Bond.jpg
    overlay_filter: 0
---
I'm training two new analysts at work, which means introducing them to bond
math. This can be a steep learning curve for some new hires since it often isn't
covered in their finance classes as undergrads. Luckily it's not too difficult,
and Excel really is an excellent tool for both doing it and building intuition
around it.

When I was first hired, I spent a fair bit of time building my intuition around
it. In particular, I realized I could represent our usual bond models with
linear algebra. I'm currently taking a refresher course on linear algebra from U
Chicago (their [Quant Foundation Series
course](https://finmath.uchicago.edu/admissions/quant-foundation-series/)), which frames the subject around
solving problems like $Ax=b$. I thought it'd be a good exercise to write up the
investment banking bond math I'm teaching our new guys in a more math-y format.

First, I should note a few conventions around municipal bonds to prevent
confusion. The most important thing to note is that almost all munis amortize
completely over time; there's rarely a balloon payment at the end, and while
it's common for issuers to refinance existing debt, bonds are almost always set up so
that's not necessary. That's a key difference from corporate bonds, which
typically pay interest until their maturity date when all the principal comes
due. Typically, munis are denominated in \\$5,000 increments (though this
can vary). It's also worth mentioning that by default, munis pay out interest
semiannually and principal annually. We talk about rates (coupons, yields, etc.)
in annual terms to keep things comparable. So for example, a 5% coupon on a \\$1
million bond will pay two coupon payments of \\$25 thousand each year.

## Setting Up the Matrix ##

I work on the Project Finance team, so most of our bond models start with a
projected revenue curve and end with a par amount and net proceeds. The problem
is to fit debt service and fees under the revenue curve, leaving as little gap
as possible so we raise as much debt as possible for the client.

Let $R_n$ be the revenue available in period $n$, which we'll say is the last
period. For now, we'll keep things simple and assume annual payments of
principal and interest, so $n$ is the total number of years the bonds will be
outstanding. Let 
$P_n$ be the principal due and $I_n$ be the interest due. For purposes of
calculating the interest, let $r$ be the coupon rate. The interest due on $P$
principal after a year is $rP$.

We need $R_n \geq D_n$, where $D_n$ is the debt service due in year $n$.
Clearly, $D_n = P_n + I_n = P_n + rP_n$. Isolate $P_n$ by writing $D_n =
P_n(1+r)$. Remember we are given $R_n$ and will come up with an appropriate
coupon rate, $r$. We're solving for $P_n$: $P_n \leq \frac{R_n}{1+r}$.

Great, that's the last period's principal payment figured out. You may be
wondering why we started from the last year. The reason is that the interest due
in any given year is a function of the principal that's outstanding at that
time, which is equal to the sum of all future principal payments. By starting
from the last year, we can use our calculated $P_l$ to find constraints on
earlier principal payments. 

So, we'll get:

$$
P_n \leq \frac{R_n}{1+r} \\
P_{n-1} \leq \frac{R_{n-1}-rP_n}{1+r} \\
P_{n-2} \leq \frac{R_{n-2}-rP_n-rP_{n-1}}{1+r}
$$

And so on. This is what I showed to our new analysts to help them put together a
basic Excel document for computing a bond model. For this blog post, I'm getting
a step ahead of myself; see below the equations before rearranging them:

$$
R_n \geq P_n(1+r)\\
R_{n-1} \geq P_{n-1}(1+r) + rP_n\\
\cdots \\
R_i \geq P_i(1+r) + \sum_{l > i}^n rP_l
$$

These equations can be represented as matrix multiplication. Let $b$ be the
vector of revenues $R_i$, and let $x$ be the vector of principal amounts we're
solving for, $P_i$. Then we construct the matrix $A$ as follows:

$$
\begin{aligned}
 A &= \left( \begin{array}{ccc}
      1+r & \cdots & r \\
      \vdots & \ddots & \vdots \\
      0 & \cdots & 1+r 
    \end{array} \right)
\end{aligned}
$$

This is a pretty nice matrix; it's upper triangular and invertible, so we can
always solve the equation. See below a quick python script which solves this
problem as we've laid it out:

{% highlight python %}
import numpy as np
import pandas as pd

def basic_solve(n, R, r):

    # n is the number of periods
    # R is the annual revenue constraint
    # r is the coupon rate

    # First, create coefficients matrix

    A = (1 + r) * np.eye(n) + r * np.triu(np.ones([n,n]),1)

    # Next, create vector R of revenues

    R = R * np.ones(n)

    # Next, solve

    Soln = np.linalg.solve(A,R)
    
    # Lastly, round down to nearest $5,000

    return np.floor(Soln / 5000) * 5000
{% endhighlight %}

## Discussion ##

The script assumes revenues (1) start right away and (2) are level. That's
reasonable for a municipality issuing a General Obligation bond; most cities
want to start paying down their debt immediately, and it's standard to have
level annual payments (similar to a mortgage). However, those assumptions are
rarely the case in a project finance context.

You can't pay back negative principal, so every element of our $x$ vector
must be nonnegative. There are plenty of examples of revenue curves which might
resolve in a naive solution giving us negative principal payments - for example,
suppose a 3-period model with zero revenue in the first two years and \\$1
million in revenue in the last year.

That specific example is actually easy to handle; we would just set aside funds
from the bond sale to pay interest in the first two years (referred to as
capitalized interest). The majority of the projects we work on use this concept,
usually because the project has a 12-24 month construction period before it'll
generate any meaningful revenue.
There are legal and practical limitations on how much capitalized interest we can
set aside, however.

A more interesting example is a high growth rate in the revenues; just by
playing around in Excel, it's easy to find examples here that don't work.
Consider a revenue curve which is zero for the first two years 
and then grows at 5% annually
from years three through fourty. There will be so much revenue in the later years
compared to what's available to pay interest in the early years that we'll
inevitably run past a realistic amount of capitalized interest to fund. In
situations like this, we often propose either shortening the bond maturity or
lowering the growth in the revenue curve; the reduced capitalized interest is
both possible/legal to sell, and often results in more net proceeds for the
client.

That specific example is actually easy to handle; we would just set aside funds
from the bond sale to pay interest in the first two years (referred to as
capitalized interest). There are legal and practical limitations on how much
capitalized interest we can set aside, however.

A more interesting example is a high growth rate in the revenues; just by
playing around in Excel, it's easy to find examples here that don't work.
Consider a revenue curve which is zero for the first two years (this is common
for real estate projects with construction times) and then grows at 5% annually
from year three through fourty. There will be so much revenue in the later years
compared to what's available to pay interest in the early years that we'll
inevitably run past a realistic amount of capitalized interest to fund. In
situations like this, we often propose either shortening the bond maturity or
lowering the growth in the revenue curve; the reduced capitalized interest is
both possible/legal to sell, and often results in more net proceeds for the
client.

It'd be nice to develop some heuristics around what kinds of revenue curves
result in "nice" bond models, where we don't need too much capitalized interest
and we're able to make efficient use of the revenues. That will be the subject
of a future blog post.

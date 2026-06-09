---
layout: post
categories: Technical
title: "Amortizing Bond Models Investigation, Part 2"
excerpt: "Analytic solution to an amortizing bond model."
header:
    overlay_image: /assets/pascals_triangle.jpg
    overlay_filter: 0.7
toc: true
---
We're picking up where we left off with using linear algebra to consider
amortizing bond models like the ones I implement at work. Last time, we wrote
the coefficients matrix which encodes the model: multiply the below matrix by a
vector with annual principal payments, and you'll get a vector representing the
total annual payment.

$$
P_n \leq \frac{R_n}{1+r} \\
P_{n-1} \leq \frac{R_{n-1}-rP_n}{1+r} \\
P_{n-2} \leq \frac{R_{n-2}-rP_n-rP_{n-1}}{1+r}
$$

I wrote a short follow-up note correcting my code, which had a rounding error as
originally written. Typically, muni bonds are sold in denominations of \\$5,000,
but for our purposes we're going to pretend denominations don't matter and we
can sell any amount of principal.

You can invert the matrix, but it's easy to solve. It's 
upper triangular, so you just need to do back substitution. It's simplest in the
case where annual revenue is constant, discussed in the next section.

In college I used a lot of Mathematica, which unfortunately is very expensive.
For this project, I wanted to use something like that to do the back
substitution. I ended up using Sympy for the first time, with the help of
ChatGPT to learn the syntax. 

## Scenario 1: Level Payments ##

Let's start with a 10 period model:    

{% highlight python %}
# R is the annual revenue constraint
# r is the coupon rate
R, r = symbols('R r')

# A is our coefficients matrix
A = Matrix((1+r) * np.eye(10) + r * np.triu(np.ones([10,10]),1))
A
{% endhighlight %}

<div style="overflow-x:auto;">
$$\small \displaystyle \left[\begin{matrix}1.0 r + 1.0 & 1.0
r & 1.0 r & 1.0 r & 1.0 r & 1.0 r & 1.0 r & 1.0 r & 1.0 r & 1.0 r\\
0 & 1.0 r + 1.0 & 1.0 r & 1.0 r & 1.0 r
& 1.0 r & 1.0 r & 1.0 r & 1.0 r & 1.0 r\\0 & 0 & 1.0 r + 1.0 & 1.0 r & 1.0 r &
1.0 r & 1.0 r & 1.0 r & 1.0 r & 1.0 r\\0 & 0 & 0 & 1.0 r + 1.0 & 1.0 r & 1.0 r &
1.0 r & 1.0 r & 1.0 r & 1.0 r\\0 & 0 & 0 & 0 & 1.0 r + 1.0 & 1.0 r & 1.0 r & 1.0
r & 1.0 r & 1.0 r\\0 & 0 & 0 & 0 & 0 & 1.0 r + 1.0 & 1.0 r & 1.0 r & 1.0 r & 1.0
r\\0 & 0 & 0 & 0 & 0 & 0 & 1.0 r + 1.0 & 1.0 r & 1.0 r & 1.0 r\\0 & 0 & 0 & 0 &
0 & 0 & 0 & 1.0 r + 1.0 & 1.0 r & 1.0 r\\0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 & 1.0 r +
1.0 & 1.0 r\\0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 & 1.0 r + 1.0\end{matrix}\right]$$
</div>

{% highlight python %}
# revenue is our revenue vector
revenue = Matrix(R * np.ones(10))

principal = A.solve(revenue)
principal
{% endhighlight %}

$$\small \displaystyle \left[\begin{matrix}\frac{1.0 R}{1.0 r^{10} + 10.0 r^{9} + 45.0
r^{8} + 120.0 r^{7} + 210.0 r^{6} + 252.0 r^{5} + 210.0 r^{4} + 120.0 r^{3} +
45.0 r^{2} + 10.0 r + 1.0}\\\frac{1.0 R}{1.0 r^{9} + 9.0 r^{8} + 36.0 r^{7} +
84.0 r^{6} + 126.0 r^{5} + 126.0 r^{4} + 84.0 r^{3} + 36.0 r^{2} + 9.0 r +
1.0}\\\frac{1.0 R}{1.0 r^{8} + 8.0 r^{7} + 28.0 r^{6} + 56.0 r^{5} + 70.0 r^{4}
+ 56.0 r^{3} + 28.0 r^{2} + 8.0 r + 1.0}\\\frac{1.0 R}{1.0 r^{7} + 7.0 r^{6} +
21.0 r^{5} + 35.0 r^{4} + 35.0 r^{3} + 21.0 r^{2} + 7.0 r + 1.0}\\\frac{1.0
R}{1.0 r^{6} + 6.0 r^{5} + 15.0 r^{4} + 20.0 r^{3} + 15.0 r^{2} + 6.0 r +
1.0}\\\frac{1.0 R}{1.0 r^{5} + 5.0 r^{4} + 10.0 r^{3} + 10.0 r^{2} + 5.0 r +
1.0}\\\frac{1.0 R}{1.0 r^{4} + 4.0 r^{3} + 6.0 r^{2} + 4.0 r + 1.0}\\\frac{1.0
R}{1.0 r^{3} + 3.0 r^{2} + 3.0 r + 1.0}\\\frac{1.0 R}{1.0 r^{2} + 2.0 r +
1.0}\\\frac{1.0 R}{1.0 r + 1.0}\end{matrix}\right]$$

I watched a [Mathologer video](https://www.youtube.com/watch?v=fw1kRz83Fj0) on
YouTube recently about solving power sums which reminded me of Pascal's
Triangle. If I hadn't watched that video, I probably wouldn't have realized that
the denominators in each of those terms are just expanded versions of
$$(1+r)^n$$. It was pretty neat to make the connection, especially since that
vector is a bit intimidating at first glance.

{% highlight python %}
principal.applyfunc(factor)
{% endhighlight %}

$$\small \displaystyle \left[\begin{matrix}\frac{1.0 R}{\left(1.0 r +
1.0\right)^{10}}\\\frac{1.0 R}{\left(1.0 r + 1.0\right)^{9}}\\\frac{1.0
R}{\left(1.0 r + 1.0\right)^{8}}\\\frac{1.0 R}{\left(1.0 r +
1.0\right)^{7}}\\\frac{1.0 R}{\left(1.0 r + 1.0\right)^{6}}\\\frac{1.0
R}{\left(1.0 r + 1.0\right)^{5}}\\\frac{1.0 R}{\left(1.0 r +
1.0\right)^{4}}\\\frac{1.0 R}{\left(1.0 r + 1.0\right)^{3}}\\\frac{1.0
R}{\left(1.0 r + 1.0\right)^{2}}\\\frac{1.0 R}{r + 1}\end{matrix}\right]$$

It's pretty easy to see that for a bond model with maturity $$n$$, the principal
paid in the first period is $$\frac{R}{(1+r)^n}$$, and so requiring principal to
be greater than or equal to zero is equivalent to requiring $$R \geq (1+r)^n$$.
This is intuititive; for the level payments scenario, extending the maturity or
raising the coupon could potentially lead to a bond model which doesn't pencil
(i.e., where we can't maximize principal paid in later periods without debt
service exceeding the revenue constraint early on). But, this is very unlikely
with realistic coupon rates which make $$1+r \approx 1$$.

## Scenario 2: Growing Payments ##

Now let's consider a revenue constraint which grows at some constant rate each
period. We'll call the growth rate $$g$$, so the revenue available to pay debt
service in period $$k$$ is the product of our base revenue $$R_0$$ and a growth
factor: $$R_k = R_0 (1+g)^k$$.

{% highlight python %}
# g is the growth rate in the annual revenue constraint
g = symbols('g')

revenue2 = Matrix(np.zeros(10))
growth_rate = lambda i, n : (1+g)**i

for i in range(0,10):
    revenue2[i] = growth_rate(i,9) * R

revenue2
{% endhighlight %}

$$\small \displaystyle \left[\begin{matrix}R\\R \left(g + 1\right)\\R \left(g +
1\right)^{2}\\R \left(g + 1\right)^{3}\\R \left(g + 1\right)^{4}\\R \left(g +
1\right)^{5}\\R \left(g + 1\right)^{6}\\R \left(g + 1\right)^{7}\\R \left(g +
1\right)^{8}\\R \left(g + 1\right)^{9}\end{matrix}\right]$$

This solution is much less pretty, even after I spent a few hours learning how
to factor expressions in Sympy:

{% highlight python %}
principal2 = A.solve(revenue2)
principal2
{% endhighlight %}

<div style="overflow-x:auto;">
$$\small \displaystyle \left[\begin{matrix}\frac{- 1.0 R g^{9} r - 1.0 R g^{8} r^{2} -
10.0 R g^{8} r - 1.0 R g^{7} r^{3} - 10.0 R g^{7} r^{2} - 45.0 R g^{7} r - 1.0 R
g^{6} r^{4} - 10.0 R g^{6} r^{3} - 45.0 R g^{6} r^{2} - 120.0 R g^{6} r - 1.0 R
g^{5} r^{5} - 10.0 R g^{5} r^{4} - 45.0 R g^{5} r^{3} - 120.0 R g^{5} r^{2} -
210.0 R g^{5} r - 1.0 R g^{4} r^{6} - 10.0 R g^{4} r^{5} - 45.0 R g^{4} r^{4} -
120.0 R g^{4} r^{3} - 210.0 R g^{4} r^{2} - 252.0 R g^{4} r - 1.0 R g^{3} r^{7}
- 10.0 R g^{3} r^{6} - 45.0 R g^{3} r^{5} - 120.0 R g^{3} r^{4} - 210.0 R g^{3}
r^{3} - 252.0 R g^{3} r^{2} - 210.0 R g^{3} r - 1.0 R g^{2} r^{8} - 10.0 R g^{2}
r^{7} - 45.0 R g^{2} r^{6} - 120.0 R g^{2} r^{5} - 210.0 R g^{2} r^{4} - 252.0 R
g^{2} r^{3} - 210.0 R g^{2} r^{2} - 120.0 R g^{2} r - 1.0 R g r^{9} - 10.0 R g
r^{8} - 45.0 R g r^{7} - 120.0 R g r^{6} - 210.0 R g r^{5} - 252.0 R g r^{4} -
210.0 R g r^{3} - 120.0 R g r^{2} - 45.0 R g r + 1.0 R}{1.0 r^{10} + 10.0 r^{9}
+ 45.0 r^{8} + 120.0 r^{7} + 210.0 r^{6} + 252.0 r^{5} + 210.0 r^{4} + 120.0
r^{3} + 45.0 r^{2} + 10.0 r + 1.0}\\\frac{- 1.0 R g^{9} r - 1.0 R g^{8} r^{2} -
10.0 R g^{8} r - 1.0 R g^{7} r^{3} - 10.0 R g^{7} r^{2} - 45.0 R g^{7} r - 1.0 R
g^{6} r^{4} - 10.0 R g^{6} r^{3} - 45.0 R g^{6} r^{2} - 120.0 R g^{6} r - 1.0 R
g^{5} r^{5} - 10.0 R g^{5} r^{4} - 45.0 R g^{5} r^{3} - 120.0 R g^{5} r^{2} -
210.0 R g^{5} r - 1.0 R g^{4} r^{6} - 10.0 R g^{4} r^{5} - 45.0 R g^{4} r^{4} -
120.0 R g^{4} r^{3} - 210.0 R g^{4} r^{2} - 252.0 R g^{4} r - 1.0 R g^{3} r^{7}
- 10.0 R g^{3} r^{6} - 45.0 R g^{3} r^{5} - 120.0 R g^{3} r^{4} - 210.0 R g^{3}
r^{3} - 252.0 R g^{3} r^{2} - 210.0 R g^{3} r - 1.0 R g^{2} r^{8} - 10.0 R g^{2}
r^{7} - 45.0 R g^{2} r^{6} - 120.0 R g^{2} r^{5} - 210.0 R g^{2} r^{4} - 252.0 R
g^{2} r^{3} - 210.0 R g^{2} r^{2} - 120.0 R g^{2} r - 1.0 R g r^{8} - 9.0 R g
r^{7} - 36.0 R g r^{6} - 84.0 R g r^{5} - 126.0 R g r^{4} - 126.0 R g r^{3} -
84.0 R g r^{2} - 36.0 R g r + 1.0 R g + 1.0 R}{1.0 r^{9} + 9.0 r^{8} + 36.0
r^{7} + 84.0 r^{6} + 126.0 r^{5} + 126.0 r^{4} + 84.0 r^{3} + 36.0 r^{2} + 9.0 r
+ 1.0}\\\frac{- 1.0 R g^{9} r - 1.0 R g^{8} r^{2} - 10.0 R g^{8} r - 1.0 R g^{7}
r^{3} - 10.0 R g^{7} r^{2} - 45.0 R g^{7} r - 1.0 R g^{6} r^{4} - 10.0 R g^{6}
r^{3} - 45.0 R g^{6} r^{2} - 120.0 R g^{6} r - 1.0 R g^{5} r^{5} - 10.0 R g^{5}
r^{4} - 45.0 R g^{5} r^{3} - 120.0 R g^{5} r^{2} - 210.0 R g^{5} r - 1.0 R g^{4}
r^{6} - 10.0 R g^{4} r^{5} - 45.0 R g^{4} r^{4} - 120.0 R g^{4} r^{3} - 210.0 R
g^{4} r^{2} - 252.0 R g^{4} r - 1.0 R g^{3} r^{7} - 10.0 R g^{3} r^{6} - 45.0 R
g^{3} r^{5} - 120.0 R g^{3} r^{4} - 210.0 R g^{3} r^{3} - 252.0 R g^{3} r^{2} -
210.0 R g^{3} r - 2.0 R g^{2} r^{7} - 17.0 R g^{2} r^{6} - 64.0 R g^{2} r^{5} -
140.0 R g^{2} r^{4} - 196.0 R g^{2} r^{3} - 182.0 R g^{2} r^{2} - 112.0 R g^{2}
r + 1.0 R g^{2} - 1.0 R g r^{7} - 8.0 R g r^{6} - 28.0 R g r^{5} - 56.0 R g
r^{4} - 70.0 R g r^{3} - 56.0 R g r^{2} - 28.0 R g r + 2.0 R g + 1.0 R}{1.0
r^{8} + 8.0 r^{7} + 28.0 r^{6} + 56.0 r^{5} + 70.0 r^{4} + 56.0 r^{3} + 28.0
r^{2} + 8.0 r + 1.0}\\\frac{- 1.0 R g^{9} r - 1.0 R g^{8} r^{2} - 10.0 R g^{8} r
- 1.0 R g^{7} r^{3} - 10.0 R g^{7} r^{2} - 45.0 R g^{7} r - 1.0 R g^{6} r^{4} -
10.0 R g^{6} r^{3} - 45.0 R g^{6} r^{2} - 120.0 R g^{6} r - 1.0 R g^{5} r^{5} -
10.0 R g^{5} r^{4} - 45.0 R g^{5} r^{3} - 120.0 R g^{5} r^{2} - 210.0 R g^{5} r
- 1.0 R g^{4} r^{6} - 10.0 R g^{4} r^{5} - 45.0 R g^{4} r^{4} - 120.0 R g^{4}
r^{3} - 210.0 R g^{4} r^{2} - 252.0 R g^{4} r - 3.0 R g^{3} r^{6} - 24.0 R g^{3}
r^{5} - 85.0 R g^{3} r^{4} - 175.0 R g^{3} r^{3} - 231.0 R g^{3} r^{2} - 203.0 R
g^{3} r + 1.0 R g^{3} - 3.0 R g^{2} r^{6} - 22.0 R g^{2} r^{5} - 70.0 R g^{2}
r^{4} - 126.0 R g^{2} r^{3} - 140.0 R g^{2} r^{2} - 98.0 R g^{2} r + 3.0 R g^{2}
- 1.0 R g r^{6} - 7.0 R g r^{5} - 21.0 R g r^{4} - 35.0 R g r^{3} - 35.0 R g
r^{2} - 21.0 R g r + 3.0 R g + 1.0 R}{1.0 r^{7} + 7.0 r^{6} + 21.0 r^{5} + 35.0
r^{4} + 35.0 r^{3} + 21.0 r^{2} + 7.0 r + 1.0}\\\frac{- 1.0 R g^{9} r - 1.0 R
g^{8} r^{2} - 10.0 R g^{8} r - 1.0 R g^{7} r^{3} - 10.0 R g^{7} r^{2} - 45.0 R
g^{7} r - 1.0 R g^{6} r^{4} - 10.0 R g^{6} r^{3} - 45.0 R g^{6} r^{2} - 120.0 R
g^{6} r - 1.0 R g^{5} r^{5} - 10.0 R g^{5} r^{4} - 45.0 R g^{5} r^{3} - 120.0 R
g^{5} r^{2} - 210.0 R g^{5} r - 4.0 R g^{4} r^{5} - 30.0 R g^{4} r^{4} - 100.0 R
g^{4} r^{3} - 195.0 R g^{4} r^{2} - 246.0 R g^{4} r + 1.0 R g^{4} - 6.0 R g^{3}
r^{5} - 40.0 R g^{3} r^{4} - 115.0 R g^{3} r^{3} - 186.0 R g^{3} r^{2} - 185.0 R
g^{3} r + 4.0 R g^{3} - 4.0 R g^{2} r^{5} - 25.0 R g^{2} r^{4} - 66.0 R g^{2}
r^{3} - 95.0 R g^{2} r^{2} - 80.0 R g^{2} r + 6.0 R g^{2} - 1.0 R g r^{5} - 6.0
R g r^{4} - 15.0 R g r^{3} - 20.0 R g r^{2} - 15.0 R g r + 4.0 R g + 1.0 R}{1.0
r^{6} + 6.0 r^{5} + 15.0 r^{4} + 20.0 r^{3} + 15.0 r^{2} + 6.0 r + 1.0}\\\frac{-
1.0 R g^{9} r - 1.0 R g^{8} r^{2} - 10.0 R g^{8} r - 1.0 R g^{7} r^{3} - 10.0 R
g^{7} r^{2} - 45.0 R g^{7} r - 1.0 R g^{6} r^{4} - 10.0 R g^{6} r^{3} - 45.0 R
g^{6} r^{2} - 120.0 R g^{6} r - 5.0 R g^{5} r^{4} - 35.0 R g^{5} r^{3} - 110.0 R
g^{5} r^{2} - 205.0 R g^{5} r + 1.0 R g^{5} - 10.0 R g^{4} r^{4} - 60.0 R g^{4}
r^{3} - 155.0 R g^{4} r^{2} - 226.0 R g^{4} r + 5.0 R g^{4} - 10.0 R g^{3} r^{4}
- 55.0 R g^{3} r^{3} - 126.0 R g^{3} r^{2} - 155.0 R g^{3} r + 10.0 R g^{3} -
5.0 R g^{2} r^{4} - 26.0 R g^{2} r^{3} - 55.0 R g^{2} r^{2} - 60.0 R g^{2} r +
10.0 R g^{2} - 1.0 R g r^{4} - 5.0 R g r^{3} - 10.0 R g r^{2} - 10.0 R g r + 5.0
R g + 1.0 R}{1.0 r^{5} + 5.0 r^{4} + 10.0 r^{3} + 10.0 r^{2} + 5.0 r +
1.0}\\\frac{- 1.0 R g^{9} r - 1.0 R g^{8} r^{2} - 10.0 R g^{8} r - 1.0 R g^{7}
r^{3} - 10.0 R g^{7} r^{2} - 45.0 R g^{7} r - 6.0 R g^{6} r^{3} - 39.0 R g^{6}
r^{2} - 116.0 R g^{6} r + 1.0 R g^{6} - 15.0 R g^{5} r^{3} - 80.0 R g^{5} r^{2}
- 185.0 R g^{5} r + 6.0 R g^{5} - 20.0 R g^{4} r^{3} - 95.0 R g^{4} r^{2} -
186.0 R g^{4} r + 15.0 R g^{4} - 15.0 R g^{3} r^{3} - 66.0 R g^{3} r^{2} - 115.0
R g^{3} r + 20.0 R g^{3} - 6.0 R g^{2} r^{3} - 25.0 R g^{2} r^{2} - 40.0 R g^{2}
r + 15.0 R g^{2} - 1.0 R g r^{3} - 4.0 R g r^{2} - 6.0 R g r + 6.0 R g + 1.0
R}{1.0 r^{4} + 4.0 r^{3} + 6.0 r^{2} + 4.0 r + 1.0}\\\frac{- 1.0 R g^{9} r - 1.0
R g^{8} r^{2} - 10.0 R g^{8} r - 7.0 R g^{7} r^{2} - 42.0 R g^{7} r + 1.0 R
g^{7} - 21.0 R g^{6} r^{2} - 98.0 R g^{6} r + 7.0 R g^{6} - 35.0 R g^{5} r^{2} -
140.0 R g^{5} r + 21.0 R g^{5} - 35.0 R g^{4} r^{2} - 126.0 R g^{4} r + 35.0 R
g^{4} - 21.0 R g^{3} r^{2} - 70.0 R g^{3} r + 35.0 R g^{3} - 7.0 R g^{2} r^{2} -
22.0 R g^{2} r + 21.0 R g^{2} - 1.0 R g r^{2} - 3.0 R g r + 7.0 R g + 1.0 R}{1.0
r^{3} + 3.0 r^{2} + 3.0 r + 1.0}\\\frac{- 1.0 R g^{9} r - 8.0 R g^{8} r + 1.0 R
g^{8} - 28.0 R g^{7} r + 8.0 R g^{7} - 56.0 R g^{6} r + 28.0 R g^{6} - 70.0 R
g^{5} r + 56.0 R g^{5} - 56.0 R g^{4} r + 70.0 R g^{4} - 28.0 R g^{3} r + 56.0 R
g^{3} - 8.0 R g^{2} r + 28.0 R g^{2} - 1.0 R g r + 8.0 R g + 1.0 R}{1.0 r^{2} +
2.0 r + 1.0}\\\frac{1.0 R g^{9} + 9.0 R g^{8} + 36.0 R g^{7} + 84.0 R g^{6} +
126.0 R g^{5} + 126.0 R g^{4} + 84.0 R g^{3} + 36.0 R g^{2} + 9.0 R g + 1.0
R}{1.0 r + 1.0}\end{matrix}\right]$$
</div>

We can do a bit better:

{% highlight python %}
principal2_factored = Matrix(np.zeros(len(principal2)))

for i in range(0,len(principal2)):
    num, den = fraction(principal2[i])
    coeff, factors = factor_list(nsimplify(factor(num)))
    principal2_factored[i] = Mul(*[base**exp for base, exp in factors[:-1]]) * Mul(coeff, factors[-1][0]) / factor(den)

principal2_factored
{% endhighlight %}

<div style="overflow-x:auto;">
$$\small \displaystyle \left[\begin{matrix}\frac{1.0 R \left(- g^{9} r - g^{8} r^{2} -
10 g^{8} r - g^{7} r^{3} - 10 g^{7} r^{2} - 45 g^{7} r - g^{6} r^{4} - 10 g^{6}
r^{3} - 45 g^{6} r^{2} - 120 g^{6} r - g^{5} r^{5} - 10 g^{5} r^{4} - 45 g^{5}
r^{3} - 120 g^{5} r^{2} - 210 g^{5} r - g^{4} r^{6} - 10 g^{4} r^{5} - 45 g^{4}
r^{4} - 120 g^{4} r^{3} - 210 g^{4} r^{2} - 252 g^{4} r - g^{3} r^{7} - 10 g^{3}
r^{6} - 45 g^{3} r^{5} - 120 g^{3} r^{4} - 210 g^{3} r^{3} - 252 g^{3} r^{2} -
210 g^{3} r - g^{2} r^{8} - 10 g^{2} r^{7} - 45 g^{2} r^{6} - 120 g^{2} r^{5} -
210 g^{2} r^{4} - 252 g^{2} r^{3} - 210 g^{2} r^{2} - 120 g^{2} r - g r^{9} - 10
g r^{8} - 45 g r^{7} - 120 g r^{6} - 210 g r^{5} - 252 g r^{4} - 210 g r^{3} -
120 g r^{2} - 45 g r + 1\right)}{\left(1.0 r + 1.0\right)^{10}}\\\frac{1.0 R
\left(g + 1\right) \left(- g^{8} r - g^{7} r^{2} - 9 g^{7} r - g^{6} r^{3} - 9
g^{6} r^{2} - 36 g^{6} r - g^{5} r^{4} - 9 g^{5} r^{3} - 36 g^{5} r^{2} - 84
g^{5} r - g^{4} r^{5} - 9 g^{4} r^{4} - 36 g^{4} r^{3} - 84 g^{4} r^{2} - 126
g^{4} r - g^{3} r^{6} - 9 g^{3} r^{5} - 36 g^{3} r^{4} - 84 g^{3} r^{3} - 126
g^{3} r^{2} - 126 g^{3} r - g^{2} r^{7} - 9 g^{2} r^{6} - 36 g^{2} r^{5} - 84
g^{2} r^{4} - 126 g^{2} r^{3} - 126 g^{2} r^{2} - 84 g^{2} r - g r^{8} - 9 g
r^{7} - 36 g r^{6} - 84 g r^{5} - 126 g r^{4} - 126 g r^{3} - 84 g r^{2} - 36 g
r + 1\right)}{\left(1.0 r + 1.0\right)^{9}}\\\frac{1.0 R \left(g + 1\right)^{2}
\left(- g^{7} r - g^{6} r^{2} - 8 g^{6} r - g^{5} r^{3} - 8 g^{5} r^{2} - 28
g^{5} r - g^{4} r^{4} - 8 g^{4} r^{3} - 28 g^{4} r^{2} - 56 g^{4} r - g^{3}
r^{5} - 8 g^{3} r^{4} - 28 g^{3} r^{3} - 56 g^{3} r^{2} - 70 g^{3} r - g^{2}
r^{6} - 8 g^{2} r^{5} - 28 g^{2} r^{4} - 56 g^{2} r^{3} - 70 g^{2} r^{2} - 56
g^{2} r - g r^{7} - 8 g r^{6} - 28 g r^{5} - 56 g r^{4} - 70 g r^{3} - 56 g
r^{2} - 28 g r + 1\right)}{\left(1.0 r + 1.0\right)^{8}}\\\frac{1.0 R \left(g +
1\right)^{3} \left(- g^{6} r - g^{5} r^{2} - 7 g^{5} r - g^{4} r^{3} - 7 g^{4}
r^{2} - 21 g^{4} r - g^{3} r^{4} - 7 g^{3} r^{3} - 21 g^{3} r^{2} - 35 g^{3} r -
g^{2} r^{5} - 7 g^{2} r^{4} - 21 g^{2} r^{3} - 35 g^{2} r^{2} - 35 g^{2} r - g
r^{6} - 7 g r^{5} - 21 g r^{4} - 35 g r^{3} - 35 g r^{2} - 21 g r +
1\right)}{\left(1.0 r + 1.0\right)^{7}}\\\frac{1.0 R \left(g + 1\right)^{4}
\left(- g^{5} r - g^{4} r^{2} - 6 g^{4} r - g^{3} r^{3} - 6 g^{3} r^{2} - 15
g^{3} r - g^{2} r^{4} - 6 g^{2} r^{3} - 15 g^{2} r^{2} - 20 g^{2} r - g r^{5} -
6 g r^{4} - 15 g r^{3} - 20 g r^{2} - 15 g r + 1\right)}{\left(1.0 r +
1.0\right)^{6}}\\\frac{1.0 R \left(g + 1\right)^{5} \left(- g^{4} r - g^{3}
r^{2} - 5 g^{3} r - g^{2} r^{3} - 5 g^{2} r^{2} - 10 g^{2} r - g r^{4} - 5 g
r^{3} - 10 g r^{2} - 10 g r + 1\right)}{\left(1.0 r + 1.0\right)^{5}}\\\frac{1.0
R \left(g + 1\right)^{6} \left(- g^{3} r - g^{2} r^{2} - 4 g^{2} r - g r^{3} - 4
g r^{2} - 6 g r + 1\right)}{\left(1.0 r + 1.0\right)^{4}}\\\frac{1.0 R \left(g +
1\right)^{7} \left(- g^{2} r - g r^{2} - 3 g r + 1\right)}{\left(1.0 r +
1.0\right)^{3}}\\\frac{1.0 R \left(g + 1\right)^{8} \left(- g r +
1\right)}{\left(1.0 r + 1.0\right)^{2}}\\\frac{1.0 R \left(g + 1\right)}{r +
1}\end{matrix}\right]$$
</div>

I was hoping this would simplify a bit more, but I didn't have any luck. If you
know of a way to simplify the third term in the numerator, let me know - I
suspect it has something to do with a multinomial missing some terms.

In the absense of a nicer solution, we can try to build intuition by
approximating the entries in the vector. Since both $$g$$ and $$r$$ are small 
decimals, we should be able to approximate
the values in the vector pretty well by ignoring high degree terms of those two
variables. 

I intend to play around with that some more, but I also want to do
some numerical analyses. At work I've noticed that a 30-year term and a growth
rate of 3% in the revenue constraint / payments tends to lead to trouble; it'd
be helpful to run a bunch of these models in Python to see where we begin to run
into issues with (i) higher growth rates, (ii) higher coupon rates, and (iii)
longer maturities. That will be the topic of a future post.

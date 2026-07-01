---
layout: post
categories: Technical
title: "Muni Bond Math Prime: The Basics"
excerpt: "Everything I would teach a Public Finance intern. Part One of a three-part series."
header:
    overlay_image:
    overlay_filter: 
toc: true
---

## Introduction ##
Inspiration for post, where my experience comes from, what makes this distinct
from other content. Quick overview of the roadmap.

Part One - The Basics:
- Time value of money
- Discount bonds
- Coupon paying, bullet maturity bonds (like Corporates or Muni serial bonds)
- Coupon paying, self-amortizing bonds (like Muni term bonds)
- Capital Appreciation Bonds & Duration

Part Two - Building Bond Models:
- Two ways to size: Project Funds and DS / Revenue Constraints
- Key bond features
  - Capitalized Interest
  - DSRF
  - Costs of issuance
  - Ongoing fees

Part Three - Advanced Structures:
- Turbo amortization
- Senior / Sub structures
- Cash flow bonds
- Convertible CABs

## Let's Get Started ##
### Why Borrow? Why Lend? ###
Why does anyone borrow money? The obvious answer is that you don't have enough
for whatever it is you're doing. Excepting generous parents, no one lends money
for free, so hopefully you have a plan to make enough money to pay back your
borrowings on time.

That leads to the complementary question: why does anyone lend money? They do so
to make a return on funds that they weren't going to use for something else
already. In order to compel someone to lend you money, you need to promise a
return high enough to make it worth their while. When people have a lot of money
laying around, not being productive, that rate of return will be pretty low.
When there are lots of competing uses for their money, the rate will be higher.

### Time Value of Money ###
If I asked you to lend me money and promised I'd pay you back in a year's time,
what kind of return would you ask for? What if instead I asked to wait to pay
you back until five years from now?

You would probably want to earn a higher return (i.e., be paid more interest)
for a five-year loan. Locking up your money for longer means that, if a good
investment opportunity comes up two years from now, for example, you wouldn't be
able to take advantage of it. You need to be compensated for the opportunity
cost of lending to me.

There are markets where that relationship is inverted, and shorter borrowing
durations actually pay higher returns. Exactly why that happens is beyond the
scope of this post, but to give you an idea: investors may have reason to think
they have better investment alternatives in the short term that will dry up in
the medium-to-long term, compelling them to lend at higher rates for short
maturities than longer ones. They'll take a lower rate on the longer term loans
because they want to get that return locked in today.

The idea that you should have to offer a return in order to borrow money is
synonymous with the idea that a rational person would rather have money today
than in the future, also referred to as the *time value of money*. This is
the fundamental concept underlying bond pricing. Everything else is a matter of
figuring out just how many of today's dollars those future dollars are worth.

### Discount Bonds ###

Alright, let's get into the sexy stuff.

Suppose I come to you and ask to borrow $100 today and promise I'll pay you back
$110 in a year's time. That's a bond! A simple, no-coupon bond. Your cash flows
look like this:

![figure 1](/assets/figure_1.png)

On a gross cash basis, this is a +$10 move. But, we just discussed how money in
the future isn't worth as much as money today. How do we account for that?

![figure 2](/assets/figure_2.png)

Suppose you tell me that a dollar a year from now is worth (to you) 95 cents
today. To get a comparable value in today's dollars for the cash owed to you a
year from now, we multiply the future cash flow by 95%. Whatever you decide a
dollar in the future is worth to you now serves as the conversion rate between
money then and money now.

So, would you lend me the money? In this example, the answer is yes. The
*present value (PV)* of the loan is positive for you; the $100 you give me today is
more than offset by the $104.50 that my repayment with interest is worth to you
in today's dollars. We'd say this deal has a *positive PV* of $4.50.

If I know exactly what that future dollar is worth to you, I can ask the
question, "how little do I need to pay him or her in order to get this loan?". 

![figure 3](/assets/figure_3.png)

If it's true that a dollar in a year is worth 95 cents to you today, you
wouldn't have a preference as to whether or not to lend to me if I promised to
pay you back $105.26. A penny less, and you'd rather have the $100 today. A
penny more, and you'd rather loan me the money for the $105.27 a year from now.

Before we move on, let's have a quick aside on conventions for talking about
bond prices and yields.

### Prices and Yields of a Discount Bond ###

In our toy example, we've established that 95 cents today is equivalent to a
dollar a year from now. This is our first example of a *bond price*. These
simple discount bonds are typically quoted with the amount today that a lender
would need to provide in order to receive a dollar at maturity. You would say,
"the dollar price of this bond is 95 cents". The dollar price is directly
connected to what it would cost to buy a bond (equivalent to loaning money).

In 

Next, suppose another friend of ours (call him Bob) asks you to loan him $100 instead.
In return, he'll give you $120 two years from now. You think about it and decide
that a dollar two years from now is worth about 90 cents today.

The $120 in two years is worth about $108 of today's dollars.


---
layout: post
title: "Spot the Arb Game"
excerpt: "Try out my game!"
permalink: /spot-the-arb/
author_profile:  true
---

There are tons of resources out there to prep for quant trading interviews.
Common topics include mental math tests, Fermi estimation questions, and market
making games. I've been using
[Tradermath](https://www.tradermath.org/dashboard) to help me prep for
internship interviews. There's plenty of similar offerings out there.

However, I'm not aware of any which help candidates prepare for questions about
reading order books. It's not quite as common, but some interviewers will ask
you to review an order book and spot an opportunity for arbitrage. It tests
quick thinking and your understanding of both how bid-asks work and how related
products influence each other's pricing.

So, I built a game in Python to help me prepare for exactly that. In this game,
there are three securities: A and B, which are normal futures, and the AB
Spread, which is a future on the difference between the closing price of A and
B. Buying the AB Spread is equivalent to going long A and short B - either way,
your payoff at the end is the final price of A minus the final price of B. That
means today, the bid and ask of the AB spread should be completely determined by
the markets in A and B. If not, an arbitrage exists.

Try it out yourself below. Under each security, the first number is the bid and
the second is the ask.

<div class="streamlit-wrapper">
  <iframe
    src="http://34.72.167.41:8501/?embed=true"
    style="width:100%; height:800px; border:none;"
  ></iframe>
</div>

If you found this helpful or just enjoyed playing it, please let me know! You can reach
out via email or LinkedIn at the links in the sidebar.

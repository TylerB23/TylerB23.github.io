---
layout: post
title: "Simple Amortizing Bond Model App"
permalink: /simple-model-app/
---

I built a simple amortizing bond model application using python and Streamlit.
This is a follow-up to my series of posts on amortizing bond models. The app
lets the user quickly examine a bunch of simple models by varying the
parameters.

This is version one of the app. It implements a simple bond model with a simple
growing/shrinking revenue curve which the user controls. It's set up to be one
term bond, priced to maturity. It can handle premium and discount pricing. It
also generates a simple sources and uses table, including percentage-based cost
of issuance and a toggle for a market-standard debt service reserve fund.

<div class="streamlit-wrapper">
  <iframe
    src="https://simple-amortizing-bond-model.streamlit.app/?embed=true"
    style="width:100%; height:800px; border:none;"
  ></iframe>
</div>

For version two, I'm planning to implement the following changes:
- Arbitrary revenue curve input;
- Automatically calculated capitalized interest with a toggle for whether or not
  to respect the IRS 3-year limit;
- Arbitrary ongoing fees, on top of debt service;
- A debt service coverage ratio calculation; and
- Date-based inputs for dated date, maturity date, and principal payments.

For version three, I'm planning to add even more features:
- Arbitrary pricing scale inputs, including serial/term bond structures;
- TIC and arb yield calculations;
- Annual/semiannual amortization options; and
- Warning messages pointing out common structuring issues.


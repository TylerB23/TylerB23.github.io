---
layout: post
title: "Simple Amortizing Bond Model App"
permalink: /simple-model-app/
---

I built a simple amortizing bond model application using python and Streamlit.
This is a follow-up to my series of posts on amortizing bond models. The app
lets the user quickly examine a bunch of simple models by varying the
parameters.

This is version two of the app. Version two added arbitrary revenue input,
automatically calculated capitalized interest, arbitrary ongoing fee input, a
debt service coverage ratio feature, and date-based inputs for the dated/closing
date and the final maturity date. It handles the initial stub period interest
payment correctly. Based on the user's inputs, it outputs a simple graph of the
debt service along with a sources and uses table and debt service table. There
are download buttons at the bottom to download csv's for those two tables.

<div class="streamlit-wrapper">
  <iframe
    src="https://simple-amortizing-bond-model.streamlit.app/?embed=true"
    style="width:100%; height:800px; border:none;"
  ></iframe>
</div>

For version three, I'm planning to add even more features:
- Arbitrary pricing scale inputs, including serial/term bond structures;
- TIC and arb yield calculations;
- Annual/semiannual amortization options; and
- Warning messages pointing out common structuring issues.

I may shift some of those into a version 2.5, depending on how tricky the
implementation is. In particular, coming up with helpful and comprehensive
warning messages will be time-consuming.

At work, I build these sorts of models in Excel all the time. It's been very
satisfying to relearn Python by working on a project where I'm so familiar with
the goal and implementation. It's been especially helpful in transitioning from
thinking in an Excel way (i.e., data-first) into a more traditional coding way
(i.e., manipulating functions with objects and then observing the result).

---
layout: post
title: "Translating the Gillespie Algorithm from Python to OCaml, pt. 2"
date: 2020-05-14
categories: python ocaml coding
excerpt: "Believe it or not, translating code between paradigms is easier said
than done."
header:
  overlay_image: /assets/dictyostelium.jpg
  overlay_filter: 0.25 
---
## Learning OCaml ##
Believe it or not, translating code between languages with entirely different
paradigms is easier said than done. That goes doubly so when adapting to an
entirely new one, as is my case with OCaml. Regardless, I've had a fun time
learning the basics of the language. It was hard at first to come to terms with
the "let... in" syntax, but as I read more of the theory behind OCaml and
functional programming in general, I began to appreciate the elegance of the
approach.

That process started on OCaml's [website], which has some of the better intro
tutorials I've read (though that may just be a byproduct of my increasing
comfort with reading and writing code). I also liked the guide on
[learnxinyminutes] for quicker reference material. That was where I first heard
mention of the Hindley-Milner algorithm that OCaml uses for typing. The
[Wikipedia page] on that is remarkably clear in its description of the problems
typing systems attempt to address, the aims of type inference, and the HM type
system as a whole.

### The Naive Approach ###
The tools familiar to me (easily mutable variables, while loops, and vector
operations with NumPy) sort of, kind of exist in OCaml, but are not the
preferred way to do things.
For example, recursion and loops: the tutorials linked above refer to loops as 'second
class citizens' in OCaml, with relatively weak implementation and a number of
caveats. The naive approach would be to directly recreate each part of the
python script in OCaml, references and while loops alike. However, this might be
trickier than just trying to implement the algorithm in a more "OCaml-y" way,
using recursion and avoiding updating an array at each step. 

### What functions do we need? ###
There's a few basic elements of the Gillespie algorithm:
1. Calculate hazard functions to describe the probability of each reaction in
   the system. Also, add these to get a total hazard (the chance at any moment
   for any reaction to occur). Parameters include constants and the count of
   each reactant.
2. Draw a wait time. This uses the total hazard as a parameter, and requires a
   uniform distribution draw, which should be accomplishable with base.Stats in
   OCaml.
3. Choose a reaction. This takes as a parameter a probability vector with
   entries being the hazards of each reaction. It makes use of a multinomial
   distribution, and outputs an integer array. In this case, we only need to
   choose one reaction, so we don't really need the array, but that's what the
   function returns.
4. Execute the reaction. Using Python, this step is just adjusting the variables
   for each reactant's counts. In OCaml, an implementation using a while loop
   should probably do the same. However, the recursive version would likely pass
   the updated reactant counts back into the function.

On a side note: this represents a departure from the planning stage when I first
implemented the algorithm in Python. There, I first determined what parameters
needed to be set for the entire function; then I initialized all the necessary
variables; then I set up the while loop; and finally, I printed the results and
(optionally) generated the plot. Doing all of that in one function body is
intuitive at this point to me, but not at all how OCaml does things. Instead of
building the program top-down, so to speak, I'm instead building it bottom-up:
asking myself, what are the most basic operations needed? How do these fit
together? What operations are codependent, passing or requiring each other's
outputs? And so on and so forth.

{% highlight ocaml %}

(*Generate Hazards*)
let h1 k1 a b =
    k1 *. a *. b;
let h2 k2 c = 
    k2 *. c;
let htot h1 h2 = 
    h1 +. h2;
    
(*Draw Wait Time*)
let t_wait htot =
    (-1. /. htot) *. (log (1. -. (Stats.uniform_rvs 0. 1.)));

(*Choose a Reaction*)
let rxn h1 h2 =
   if (Stats.uniform_rvs 0. (htot h1 h2)) >= h1 then 2 else 1;


{% endhighlight %}

### Tail Recursion ###
The issue with recursion (as I was taught) was its memory expense. Adding
all those function calls to the stack quickly grows, since each must be
'collapsed down', so to speak, at the end in order to get your result. Luckily,
OCaml uses compiler magic to avoid this issue. This requires using tail
recursion -- where the last call in a recursive function is to the function.
This can be less obvious than it seems. To borrow an example directly from the
OCaml tutorials:

{% highlight ocaml %}
let rec range a b =
  if a > b then []
  else a :: range (a+1) b;;
{% endhighlight %}

While the recursive call is in the last line, it isn't the last operation
completed:
1. (a+1)
2. range (a+1) b
3. a :: range (a+1) b

This results in the typical recursion memory issue. tail recursion is of the
following form:

{% highlight ocaml %}
let rec loop () =
  (*loop contents*)
  loop ();;
{% endhighlight %}

The compiler basically turns that syntax into a while loop. There's a great
Computerphile video about tail recursion on [YouTube], if you're interested.

## Part 2 Conclusion ##
This was an especially hard post to write, in particular because I wanted to get
my info right and relevant to what the final product will be. This isn't meant
to be so much a tutorial as a dive into my thought process in my first attempt
at functional programming. Part 3, which'll include and analyze some final code,
will come soon!

[website]: (https://ocaml.org/learn/)
[learnxinyminutes]: (https://learnxinyminutes.com/docs/ocaml/)
[Wikipedia page]: (https://en.wikipedia.org/wiki/Hindley%E2%80%93Milner_type_system)
[YouTube]: (https://www.youtube.com/watch?v=_JtPhF8MshA)

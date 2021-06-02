---
layout: post
title: "Learning to Script"
date: 2021-06-01
---
I'm pretty sure I first got interested in linux around the same time Edward
Snowden fled the US. I was 13 years old and captivated by how much one could
determine from the metadata and other stuff the NSA was collecting. There was also
some part of me that really, really hated the idea that someone out there knew
what I was doing on the computer (again, I was 13, so that was mostly downloading
Minecraft mods). While exploring ways to be more private online, I
was introduced to the open source community and Linux.

I put Ubuntu on the first computer I built myself later that year,
and after failing to figure out wireless card drivers, caved and bought Windows.
The fascination with Linux remained, and today, it's all I use
on my personal computer. 

So of course, when I saw a special topics course in the CS department titled
"Linux Scripting", I signed up right away. Like any Linux user I'd tried to use
the terminal before, and figured out some basics, but generally avoided it where
I could. And like most math majors, I was really excited to take a class where
I'd learn stuff I could use on a daily basis. While no doubt run-of-the-mill
for the engineers in the class, I found it really cool that everything we did was
something I could reasonably see myself doing with my own machine. The
assignments were wonderfully open-ended: we got to build whatever we
wanted with the scripting language we had talked about that week, and record a
short video talking about what we built. 

The course went over half a dozen languages, including PHP, Perl, Javascript,
Bash, TCL, Python, awk, and while it's not a language, we spent a lot of time
on regular expressions. Of these, I'd only written extensively in Python and by
chance a few times in Bash. 

To my surprise, the current maintainer of Bash,
[Chet Ramey](https://tiswww.case.edu/php/chet/) works at CWRU. Including Bash
under 'My Projects' on a personal website has got to be one of the biggest FOSS
flexes I've ever seen, personally. He came into our class to talk about how he
got involved on the project and some of the challenges of maintaining support
for very old code.

Anyway, I thought it would be fun to write up some of my favorite projects from that
class. Writing Bash feels like such a pure form of coding to me, in that it's a
lot of frustration and things not working until I find the exact issue or just
the right way to do something, and then it all falls into place in a rush of
satisfaction.

(A quick digression: a friend once pointed out to me that code
will work on the first try if you write it correctly. I doubt I've ever been so
annoyed in my life).

There are many, many definitions of what a 'scripting language' is, and that was
a source of great discussion in class. I don't want to attempt to retread the
same ground you can find on a million different blogs and stackoverflows, so
I'll summarise here how I use scripting: either for something very simple, or
very temporary. 

I have some startup scripts that run every time a program is
opened or I log into my computer, and those scripts do very simple things:
launching a program or changing the appearance of Vim, for example. I also
sometimes write one-liners to do quick-and-dirty operations, like finding uses
of a particular command in a set of R files. That's about the amount of
programming/computing I do that I consider 'scripting'. That said, I really
enjoy this hacky approach to problem-solving: it sort of represents 
the can-do spirit I like about Linux and open source. Anyways.

### Cleaning up File Names ###
The PI in charge of the lab I've been part of since freshman year tells
everyone in the group, over and over, never to give a file a name with spaces in
it. When I was on Windows, I always did this since it looked nicer in the
Explorer window. On Linux, as well as any system with a lot of similarly named
files, that's an awful way to do things because of how annoying whitespace is
to parse. On the command line, if a file or folder name has spaces, it needs to
be enclosed in single quotes like so:

{% highlight bash %}
# the following doesn't work
cd folder with spaces
# this line does
cd 'folder with spaces'
{% endhighlight %}

For my first video assignment in Bash, I thought it'd be useful to have a script
which removes spaces from file names and replaces them with underlines. The
basic functions here (listing file names and editing strings) are very
well-suited to Bash and scripting in general. I ended up running this over my
entire home directory, which fixed some files I had named with spaces on
accident, some oddly-named downloads, and a few crash logs from Matlab.

Here's the code I turned in:

{% highlight bash %}
ls -R | while read line; do
    if [[ ${line:(-1)} == ":" ]]; then
        directory="${line::(-1)}"
    fi
    if [[ "$line" =~ [[:space:]] ]]; then
        mv "$directory/$line" "$directory/${line// /_}"
    fi
done
{% endhighlight %}

So much fun stuff there. The `|` character is a pipe, which gives the output of
the first command to the following command as input. The Unix Philosophy of
having many utilities that do one thing very well is so satisfying to me: it's
'clean' in some way that I have a hard time describing. 

By the way, I don't intend this to be a tutorial on Bash or anything like that.
If you're curious and want to learn more, try the manual pages accessed in the
terminal with `man ls`, for example. I also really like the [How-To
Geek](https://www.howtogeek.com/438882/how-to-use-pipes-on-linux/) guides on
individual Linux commands, written by Dave McKay.

The double bracket notation for conditionals, combined with the parameter
expansions, were my professor's favorite part of Bash. I've come to appreciate
them too for how powerful they are (especially that 6th line),
but the notation still feels needlessly concise to me, as do so many 
conventions from the era when memory and storage were not cheap. These are the
sorts of things that make a friend of mine call the early Unix utility devs 
wizards. It builds into this sense of lore that I think many people in my 
generation get when we play with older tools.

### Finding Functions in R files ###
My last project for the class could have been done in Python or Javascript, but
I was really enjoying getting used to Bash and I had a good problem for the
language. I maintain an R package for my lab,
[SunsVoc](https://cran.r-project.org/package=SunsVoc), which provides a way for
photovoltaics researchers to create artificial IV curves from outdoor time
series data. Our lab collects IV curves from freshly built solar panels with an
indoor testing machine called Suns-Voc, so the package provides a great way to
compare the attributes of the panel after exposure and weathering.

R packages have relatively simple structure, including an "R" folder which
contains all the package functions. A common frustration when working on these
packages is having to change how one function works, then having to track down
each occurence of it to see where it may cause issues. No doubt there are better
ways to write the code to ensure future changes don't create future issues, but
our lab develops this code mostly by having one or two researchers prototype the
code, then once a paper is published on the concept, the same researchers and
others work on packaging the code for others to use. So best software
engineering practices are usually of secondary concern to developing the core
functions.

Anyways, I started using `grep` for the first time a while ago with the terminal
built into RStudio in order to find the places where I use functions. The idea
for the project was to grep through the "R" folder, find all the function
definitions, and print their locations with all the locations they are called.
My implementation is far from perfect: it misses uses of functions within
`apply` functions, for example. That said, it satisifies a need for me, and
likely wouldn't be too difficult to make more thorough. This does sort-of
break the description I wrote above about how I tend to use scripting languages,
which brings up interesting questions about the best way to do this sort of
task. I'm always open to suggestions!

The main source of my attraction towards Bash is building up commands
bit-by-bit. For the first part of this project, I tested in the terminal each of
the following snippets:

```
# find function declarations, with location of file and line
grep -rn '<- function(.*' | sed 's/<-.*$//'

# Find use of a function, func_name
grep -r func_name\(.*\)

# Exclude comments and examples
grep -v \#\'

# Match only nested functions
grep -rn '<- function(.*' | sed 's/<-.*$//' | sed 's/^.*:.*://' | grep \^[[:space:]]
```

This eventually became:

```
#! /usr/bin/bash

declare -a functions
readarray -t functions < <(grep -rn '<- function(.*' | sed 's/<-.*$//' | sed 's/^.*:.*://')

for i in "${functions[@]}"; do
    if [[ $i =~ \# ]]; then
          :
    elif [[ $i =~ ^[[:space:]] ]]; then
        func="$(echo "$i" | sed 's/^[[:space:]]*//')"
        printf "Nested Function: %s\n" $func
        unset func
    else
        printf "Function: %s\n" $i
    fi
done

unset IFS
```

I wasn't happy with using the array, though, since it made the code more verbose
than it needed to be. After fiddling with delimiters, I got to this:

```
#! /usr/bin/bash

IFS=$'\n'

#grep -rn '<- function(.*' | sed 's/<-.*$//' | sed 's/^.*:.*://' | while read i; do
for i in $(grep -rn '<- function(.*' | sed 's/<-.*$//' | sed 's/^.*:.*://'); do
    if [[ $i =~ \# ]]; then
          :
    elif [[ $i =~ ^[[:space:]] ]]; then
        func="$(echo "$i" | sed 's/^[[:space:]]*//')"
        printf "Nested Function: %s\n" $func
        unset func
    else
        printf "Function: %s\n" $i
    fi
done

unset IFS
```

I just had to set the IFS (interfield seperator) to newline characters to get
the same behavior from a for loop as from `readarray`. To me, this method is
just as easy to read and simpler to troubleshoot, since it cuts down on the
number of unique functions used. 

Next, I wanted to find all the occasions of a function being used:

```
#!/usr/bin/bash

# Input should be the name of the function you're looking for
func=$1
# Separate the array items below by newlines, not spaces
IFS=$'\n'

# Grep for that function name (being used as a function)

for i in $(grep -rn $func\( | grep -v ^.*\#); do
    file="$(echo $i | grep -o ^.*R)"
    line="$(echo $i | grep -Eo :[0-9]+*: | sed 's/://g')"
    printf "Used on line %s in file %s\n" $line $file
done
unset IFS
```

I remember hating all the time we spent manipulating strings in my first comp
sci class in high school. I've come to appreciate it a lot more now that I'm
doing it with a purpose in mind - arbitrary problems like "remove everything
before the first occasion of this substring" are both easy to do with Bash and
much more satisfying when they get you what you want.

The only step remaining was to combine them together:
```
#!/usr/bin/bash

# Get a function, then print the uses of that function

IFS=$'\n' 
for i in $(source ~/Documents/CSDS397/video3/find_funcs.sh);
do
    # First, print the name of the function we'll be examining
    printf "$i\n"
    # Now, get that $i down to just the function name
    func="$(echo $i | grep -o ": .*$")"
    func=${func#* }
    func=$(echo $func | sed 's/ //g')

    output=$(source ~/Documents/CSDS397/video3/find_func_uses.sh $func; echo x)
    output=${output%?}
    printf "$output%s" ''
done
```

This one was interesting for the printing challenges. I'm not sure that I have
the most concise form of this code, but I landed here after playing with
trailing whitespace and adding newlines and so on for an hour or two. This was
definitely the most tedious part of developing the script, since I was so close
to done but still dealing with Bash quirks. 

### Concluding Thoughts ###

I still use the three scripts I wrote for finding R functions all the time. They
were immediately useful for finding some small problems, like a nested function
that was defined identically in two different functions or a few deprecated
functions I hadn't yet removed. What's most helpful is having the
greps and seds on hand to quickly get what I want instead of having to come up
with a new one-liner each time.

Since the semester ended, I've found myself using bash and the command line much
more often. At this point, the only two things I typically have open are Firefox
and a few terminals, plus the occasional PDF reader if I'm annotating something.
I've found this to be marginally quicker than using file explorers and other
applications, but also much more satisfying. That's for most of the same reasons
I've come to enjoy scripting - this sense of freedom in personal control. 

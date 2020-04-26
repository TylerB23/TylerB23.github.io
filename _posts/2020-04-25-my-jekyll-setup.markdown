---
layout: post
title: "My Jekyll Setup"
date: 2020-04-25
categories: website
---
A friend of mine introduced me to [github.io] a few back and showed me some of
the personal projects he has on his blog.
My curiosity was piqued, so I set up a github repo, added a "hello, world!" 
html file, and... left it at that for about 6 months.
Now that I'm quarantined at home with nothing to do except study for finals,
I figured it's the perfect time to figure this all out. 

A quick note: this isn't meant to be a full tutorial (for that, see the official
documentation linked further down!) but hopefully an interesting overview of my
usecase and workflow. If you want to follow along, first go to github.io and follow
their guide on creating the repo, cloning it locally, writing your first html file,
and then pushing it up.

Anyways, I went back to the github repo and tried to view my website. Nothing
but a mono plain text "hello, world!", which while riveting, doesn't exactly
fulfill my original vision. I pulled the repo to my new desktop
(I've switched to KDE Manjaro after a little bit too much time on [r/unixporn])
and set out to install Jekyll. Here's the series of commands I used, keeping in mind
that Manjaro is an Arch-based distro:

{% highlight bash %}

# Install a full ruby environment
sudo pacman -S ruby base-devel

# Install ruby gems to ~/gems by adding lines to our .bashrc
echo '# Install Ruby Gems to ~/gems' >>  ~/.bashrc
echo 'export GEM_HOME="$HOME/gems" >> ~/.bashrc
echo export PATH="$HOME/gems/bin:$PATH"' >> ~/.bashrc

# source our .bashrc so the gems are properly set up in the PATH
source ~/.bashrc

# Now we get to install Jekyll (and bundler!)
gem install jekyll bundler

{% endhighlight %}

I've found that when I forget to add those lines to .bashrc and source it,
I get an error like: "WARNING: You don't have /home/tylerb/.gem/ruby/2.7.0/bin in your
PATH, gem executables will not run", which, as you might imagine, means that
the gem executables won't run and we can't install and use jekyll and bundler.
I fix that by running
{% highlight bash%}
export PATH="/home/tylerb/.gem/ruby/2.7.0/bin:$PATH"
{% endhighlight %}
Obviously, change my directory path to whatever yours is in the error message.


Bundler is a Ruby package manager which tracks and installs the gems necessary to
do your work. It wraps our Jekyll functions and makes sure Ruby is set up behind
the scenes. If you want more in-depth information on all of this, check out
the official documentation on [jekyll doc] and [github.io doc]. 

After that's all set up, we type into the command line:

{% highlight bash %}

# build your site!
bundle exec jekyll build
bundle exec jekyll serve

{% endhighlight %}
This will host your website from the command line on your computer. Look
at the output to see something like "Server address: http://127.0.0.1:4000/".
Type that into your web browser, and you'll see your local build!

Alternatively, go to [http://localhost:4000], which always works.

Building your website locally like this is the best way to test it and write your posts.
Changes pushed to your github repo will take some time to appear on the live version.

So, a bit more on my workflow. I use [Yakuake] and [tmux] for anything
command-line-intensive. I really like writing in [Vim], if only because it scratches
that little-kid itch to feel like a hacker. Here's a screenshot of me editing this document:
![Yakuake Setup](/assets/Screenshot_20200425_151631.png)

The top right is where the local build is running from. Below it is the default
'Welcome to Jekyll!' post created when we built the website. I keep
this open for reference on adding code blocks and stuff like that. To the top left is my
Vim window where I'm writing the post, and below that is an extra spot to run
commands (I'm running ytop here to keep an eye on system resources). I use the 
[Dracula] theme for my KDE, tmux, and vim setups, which is where
the colors and HUD along the bottom bar come from. In the future, I'll make a 
post about my .vimrc, .bashrc, and .tmux.conf files.

It's also worth mentioning that I use [Starship] as my shell prompt. Again,
for another post.

The generic Jekyll post outlines how to create a post. I did:
{% highlight bash %}

cd repo_directory_here/_posts
vim YEAR-MONTH-DAY-title.markdown

{% endhighlight %}
To create a new blog post in markdown. It's important to have the date right
and title the document exactly like this so Jekyll recognizes it! Add your front matter
and type your post. here's a direct link to this post's markdown for the interested:
[markdown document](/assets/2020-04-25-my-jekyll-setup.txt)
The front matter is commented out to prevent Jekyll from processing it and
turning it into html so it's more readable for you.

I follow the Jekyll documentation advice and add YAML front matter to every
document, which looks something like this:
{% highlight markdown %}
---
# front matter goes here!
---
# the document goes here!
{% endhighlight %}

I also put things like images, document links, and datasets into an /assets/
folder in the main directory. Then I can link to anything and be sure it's
accessible via the online github repo without worrying about links breaking or
assets disappearing. As long as the site is being hosted, all those things in
the /assets/ folder should stay there.

Whenever I'm done writing a post, I push the changes up to my repo with some
variation of the following:
{% highlight bash %}
# pushing up changes
git add --all
git commit -m 'a meaningful commit message'
git push
{% endhighlight %}

Keep in mind that all has to be done from the directory of your local branch.
For the non-git initiated, I'll recommend the documentation at [git-scm].
There's a nice cheat sheet at the top that explains the basic commands, and
it should be more than fine for any solo github project.

This is about the extent of my workflow for now. In the future if I decide to
get more fancy with it, I'll write an update to this post and fill you in. For
now, I'm enjoying how quick and easy it is to write in markdown, and the themes
in jekyll suit me nicely enough to not bother messing around with html and css
files all day. My next planned post will describe some more of my KDE
customizations, theming, and workflow: stay tuned for that!

[r/unixporn]: https://reddit.com/r/unixporn/
[github.io]: https://github.io/
[http://localhost:4000]: http://localhost:4000]
[jekyll doc]: https://jekyllrb.com/docs/
[github.io doc]: https://help.github.com/en/github/working-with-github-pages/setting-up-a-github-pages-site-with-jekyll
[Yakuake]: https://wiki.archlinux.org/index.php/Yakuake
[Dracula]: https://draculatheme.com/
[Starship]: https://starship.rs/
[tmux]: https://github.com/tmux/tmux
[Vim]: https://www.vim/org
[git-scm]: https://git-scm.com/docs

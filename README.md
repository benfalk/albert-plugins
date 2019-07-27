
## Albert Plugins

A grab-bag of plugins that I have come up with to keep productivity higher

### Spell

![](doc_assets/spell-demo.gif?raw=true)

A simple speller that uses [aspell](http://aspell.net/) under the hood.  You'll
need to ensure that you have it on your operating system for this plugin to
work.  To install the plugin simply copy the contents inside of `spell/` into
your Albert python modules directory.

### Github Repos

![](doc_assets/github-demo.gif?raw=true)

If you find yourself jumping around different repos that you or your company
have on Github this may be the plugin for you.  This plugin is expecting a
newline text file with every repo on it's own line.  The location of this
file should be:

```
~/.github_cache/repo-names.txt
```

As luck would have it; I got your back on this one.  If you want to generate
a big list based on users and orgs I have added a helper script that generates
this file for you.  To auto-generate this list:

1. Copy the `github_cache` directory to `~/.github_cache`
2. Optionally rename the `token.example` file to `token` and ensure
   it has the correct username and token.  You can generate a token
   [by reading this](https://help.github.com/en/articles/creating-a-personal-access-token-for-the-command-line)
3. Rename `config.example` to `config` and update the lists to contain
   the users and orgs you want to make a list for
4. Run `python3.6 github_cache.py`

To install the plugin copy the contents of `github` into your Albert python
modules directory and activate it.  **NOTE** - The list is only loaded by
the plugin when albert is initialized.  If you want to refresh your list
for now you'll need to restart albert.

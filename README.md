# Sublime Trello

This is a package for [Sublime Text 3](http://www.sublimetext.com/3) that provides a number of useful commands for interacting with Trello (using the [Trello API](https://trello.com/docs/index.html)).

## Usage

This package allows you to navigate the data Trello provides using the Trello API. It's heavily inspired in the [File Navigator](https://github.com/Chris---/SublimeText-File-Navigator) package.

### Navigate

If you [run][1] the `Trello: Navigate` command, you'll see your boards, and from there you can go into the Trello element structure `(Board -> List -> Card -> Actions)`.

### Unread notifications

When you [run][1] `Trello: Unread Notifications`, you'll see the amount of unread notifications the current user has, and a *little* description of what happened, for example:

````
Total unread: 1

1) Nofitication type: commentCard
Card: Some Card
Board: Some Board
````

This could be improved a lot, but I think it's understandable (with a little bit of brain parsing) and I prefer adding some other stuff before making it prettier (pull requests are welcome!).

### Cache

By default most requests will be cached, to improve performance. When you do an action that requires the element to be realoaded, for example creating a new card in a list, the package will try to delete only that cache, maintaining the rest.

But if you make changes in the web version or by some chance elements remain cached, changes will not be reflected.

To avoid this you have two options, [run][1] the `Trello: Delete cache` command, which will clean the cache and will request everything again *or* you can switch the `use_cache` (which is true by default) option to `false` on your [settings][3], like this:

````json
{ "use_cache": false }
````

which is not really recommended because the package will request everything on *every* request, but it's an option just in case.

## Generating Your Keys
By default the package uses a Trello app generated only to be used here. If the `token` isn't present the package will pop up a message telling you how to get it.

Basically because of the way Trello authentication works, you'll need to copy a url in your browser and pase the result in the `token` property of the [settings][3], for example:

Url:

````
https://trello.com/1/connect?key={KEY}&name=sublime_app&response_type=token&scope=read,write
````

Options:

````json
{
    "key"   : "",
    "secret": "",
    "token" : "{token_goes_here}"
}
````

If you don't want to use the default app, you can change it by adding your own key and secret to the json [settings][3]. You can get them from [here](https://trello.com/1/appKey/generate).

Also, if you want to enable only some access to your account, you can modify the scope of the url, for example from `&scope=read,write` to `&scope=read` 

## Shortcut Keys

**Windows and Linux:**

 * Navigate: `ctrl+alt+t`
 * Unread notifications: `ctrl+alt+n`

**OSX**

 * Navigate: `super+alt+t`
 * Unread notifications: `super+alt+n`


`Delete cache` does not have a shortcut, but you can set it in `Preferences -> Key Bindings - User` by adding:

````json
{ "keys": ["ctrl+alt+d"], "command": "trello_delete_cache" }
````

## Settings location
Preferences -> Package Settings -> Trello -> Settings User

## Instalation

### PackageControl
If you have [PackageControl](http://wbond.net/sublime_packages/package_control) installed, you can use that to install the package.

Just type `cmd-shift-p`/`ctrl-shift-p` to bring up the command pallate and pick `Package Control: Install Package` from the dropdown.

Then type `Trello` and choose this package from the dropdown. That's it!

### Manual

You can clone the repo in your `/Packages` (*Preferences -> Browse Packages...*) folder and start using/hacking it.
    
    cd ~/path/to/Packages
    git clone git://github.com/NicoSantangelo/sublime-text-trello.git Trello

## Known issues

[Curl](http://curl.haxx.se/) is required for Linux users (it should be on:
`/usr/local/sbin`, `/sbin`,  `/usr/sbin`, `/usr/local/bin`, `/usr/bin`, or `/bin`).


## Roadmap

* Labels
* Checklists
* Port to ST2?
* The rest of the [Trello API](https://trello.com/docs/index.html)?
* ~~Don't cache requests~~
* ~~Go back option~~
* ~~Card description~~
* ~~Create Card from List~~
* ~~Create List from Board~~
* ~~Create Board~~
* ~~Print the comment somewhere when it's selected from the list of Card comments~~ (ouput panel)

## Any idea?

* Pull requests are more than welcome, you can run the tests using the [AAAPT Package](https://github.com/guillermooo/AAAPT) or in the terminal (for example: `cd path/to/Trello && python3 -m tests.test_output`).

* Another way would be adding an [issue](https://github.com/NicoSantangelo/sublime-text-trello/issues) with your feature request.

## Thanks to
* The [Trollop](https://bitbucket.org/btubbs/trollop) Python Library
* The [Sublime Github](https://github.com/bgreenlee/sublime-github) package for the awesome workaround for httplib

## Copyright

Copyright &copy; 2013+ Nicolás Santángelo. 

See LICENSE for details.

  [1]: https://github.com/NicoSantangelo/sublime-text-trello#shortcut-keys
  [2]: https://github.com/NicoSantangelo/sublime-text-trello#roadmap
  [3]: https://github.com/NicoSantangelo/sublime-text-trello#settings-location

# Sublime Trello

This is a package for [Sublime Text 3](http://www.sublimetext.com/3) that provides a number of useful commands for interacting with Trello (using the [Trello API](https://trello.com/docs/index.html)).

## Usage

Because it's still early in development, the interaction is kind of rough right now, but the idea it's to navigate across your Trello data like the [File Navigator](https://github.com/Chris---/SublimeText-File-Navigator) package.

If you [run][1] the navigate command, you'll see your boards, and from there you can go into the Trello element structure `(Board -> List -> Card -> Actions)`.

## Generating Your Keys
By default the package uses a Trello app generated only to be used here. If the `token` isn't present the package will pop up a message telling you how to get it.

Basically because of the way Trello authentication works, you'll need to copy a url in your browser and copy-pase back the result given in the `token` property of the options, for example:

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

If you don't want to use the default app, you can change it by adding your own key and secret to the json settings. You can get them from [here](https://trello.com/1/appKey/generate) (it doesn't event require a click).

Also, if you want to enable only some access to your account, you can modify the scope of the url, for example from `&scope=read,write` to `&scope=read` 

## Shortcut Keys

**Windows and Linux:**

 * Navigate: `ctrl+alt+t`

**OSX**

 * Navigate: `super+alt+t`

## Instalation

The package is nowhere near production ready yet, but if you're feeling adventurous you can download the repo in your `/Packages` (*Preferences -> Browse Packages...*) folder and start using/hacking it.

## Known issues

[Curl](http://curl.haxx.se/) is required for Linux users (it should be on:
`/usr/local/sbin`, `/sbin`,  `/usr/sbin`, `/usr/local/bin`, `/usr/bin`, or `/bin`).

## Roadmap for release
* Don't cache requests 
* Go back option
* Card description
* Create Card from List
* Create List from Board
* Create Board
* Print the comment somewhere when it's selected from the list of Card comments

## Thanks to
* The [Trollop](https://bitbucket.org/btubbs/trollop) Python Library
* The [Sublime Github](https://github.com/bgreenlee/sublime-github) package for the awesome workaround for httplib

## Copyright

Copyright &copy; 2013+ Nicolás Santángelo. 

See LICENSE for details.

  [1]: https://github.com/NicoSantangelo/sublime-text-trello#shortcut-keys
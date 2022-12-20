# Screenshot

A python tool to take screenshots of web pages from list of urls.

## How to install it

You need to clone the repository on your computer. Then, in your shell, type:

 ```make deps```

You also need to have `chrome` installed on your computer.

## Available commands

```
usage: python -m screenshot.cli [-h] [--version] {authenticate,take} ...

positional arguments:
  {authenticate,take}
    authenticate       authenticate in a browser and save browser info in a authenticate_folder
    take               take screenshot

optional arguments:
  -h, --help           show this help message and exit
  --version            show program's version number and exit
```

## Take

For now, with the option `--authenticate`, this command works with a headed browser. To create an `authenticate_folder`, you can use the `authenticate` command (documentation below).

```
usage: python -m screenshot.cli take [-h] [--output OUTPUT] [--authenticate AUTHENTICATE] [--cookies] [--throttle] column [file] directory

positional arguments:
  column                column where the urls are or a single url
  file                  file where the urls are. Defaults to None
  directory             name of the directory where we should put the screenshots

optional arguments:
  -h, --help            show this help message and exit
  --output OUTPUT, -o OUTPUT
                        output file with the files name
  --authenticate AUTHENTICATE, -a AUTHENTICATE
                        authenticate_folder where the browser info are (useful for Facebook, Twitter...). Not compatible with
                        'cookies'
  --cookies, -c         get cookies from chrome (won't work for Facebook, Twitter). Not compatible with 'authenticate'
  --throttle THROTTLE, -t THROTTLE
                        time to wait between accessing to an other URL. Defaults to 0
```

## Authenticate

This command is useful if you want to use the `--authenticate` argument of the `take` command. It will open a browser where you'll be able to log into some plateform you want to take screenshot of. This command is here as a result of experimentations, if you want to be connected to some accounts, we advise you to connect in your browser and use the `--cookies` option of the `take` command.

```
usage: python -m screenshot.cli authenticate [-h] folder

positional arguments:
  folder      folder name where the browser info must be saved

optional arguments:
  -h, --help  show this help message and exit
```

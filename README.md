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

## Authenticate

This command is useful if you want to use the `--authenticate-folder` argument of the `take` command. It will open a browser where you'll be able to log into some plateform you want to take screenshot of. Particularly, you need to do so for Facebook and Twitter.

```
usage: python -m screenshot.cli authenticate [-h] folder

positional arguments:
  folder      folder name where the browser info must be saved

optional arguments:
  -h, --help  show this help message and exit
```

## Take

For now, with the option --authenticate, this command works with a headed browser.

```
usage: python -m screenshot.cli take [-h] [--output OUTPUT] [--authenticate_folder AUTHENTICATE_FOLDER] [--cookies] [--throttle] column [file] output_dir

positional arguments:
  column                column where the urls are or a single url
  file                  file where the urls are. Defaults to None
  output_dir            name of the directory where we should put the screenshots

optional arguments:
  -h, --help            show this help message and exit
  --output OUTPUT, -o OUTPUT
                        output file with the files name
  --authenticate_folder AUTHENTICATE_FOLDER, -a AUTHENTICATE_FOLDER
                        authenticate_folder where the browser info are (useful for Facebook, Twitter...). Not compatible with
                        'cookie'
  --cookies, -c         get cookies from chrome (won't work for Facebook, Twitter). Not compatible with 'authenticate_folder'
  --throttle THROTTLE, -t THROTTLE
                        time to wait between accessing to an other URL. Defaults to 0
```

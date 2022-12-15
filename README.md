# Screenshot

A python tool to take screenshots of web pages from list of urls.

## How to install it

You need to clone the repository on your computer. Then, in your shell, type:

 ```make deps```

You also need to have `chrome` installed on your computer.

## How to use it

If you want to get the screenshot of a single url, you can use it this way:

```python -m screenshot.cli URL OUTPUT-DIR```

If you need to use it with an input file:

```python -m screenshot.cli COLUMN --file INPUT-FILE OUTPUT-DIR```

To add an output file:

```python -m screenshot.cli URL OUTPUT-DIR --output OUTPUT-FILE```
[![Build Status](https://github.com/MiguelLaura/screenshot/workflows/Tests/badge.svg)](https://github.com/MiguelLaura/screenshot/actions)

# Screenshot

A python tool to take screenshots of web pages from list of urls.

## How to use it

You need to clone the repository on your computer. Then, use it this way:

```python -m screenshot.cli URL OUTPUT-DIR```

If you need to use it with an input file:

```python -m screenshot.cli COLUMN --file INPUT-FILE OUTPUT-DIR```

To add an output file:

```python -m screenshot.cli URL OUTPUT-DIR --output OUTPUT-FILE```
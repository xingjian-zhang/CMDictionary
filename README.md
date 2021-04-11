# CMDictionary

_Author: Xingjian Zhang_

This is a **light**, **cute** and **convenient** commandline-like dictionary that helps you to memorize words.

![demo_help](asset/demo_help.jpg)

## Note

1. You need to use [Windows Terminal](https://github.com/microsoft/terminal) to see the emojis.
2. The program will download a set of words from NLTK if your path does not contain it. This may takes a few seconds.
3. You need internet connection to get the meanings of words.

## Install Dependency

```
pip install -r requirements.txt
```

## Run

```
python -u main.py
```

## TODO List
- [ ] Add cache to reduce requests.
- [ ] Add command to toggle emoji output.

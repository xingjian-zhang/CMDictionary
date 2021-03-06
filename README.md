# CMDictionary

A **light**, **pure** and **convenient** commandline dictionary that helps you focus on memorizing words.

## Features

### Detailed Help Information
![demo_help](asset/demo_help.jpg)

### Detailed Explanations and Examples
![demo_query](asset/demo_query.jpg)

### Track Your Recently-Memorized Words
![demo_list](asset/demo_list.jpg)

### Auto-Completion (Experiment)
![demo_auto](asset/demo_auto.jpg)
**Note**: The suggestions are ranked by word frequencies. Unfortunately, windows system is not compatible with python `tab` completion. See details [here](https://stackoverflow.com/questions/1081405/python-tab-completion-in-windows).

## Note

1. You may need to use [Windows Terminal](https://github.com/microsoft/terminal) to see the emojis.
2. You need internet connection to get the meanings of words at the first time.

## OS
1. Linux
2. Windows
3. MacOS
## Install

```
python setup.py install
```

**Note**: Do **NOT** use `pip install cmdict` because there is a package called `cmdict` written by others in the pip repo. By doing this you will download the wrong package. I am still looking for workaround for this.

## Run

```
python -m cmdict
```

## Customize Your Vocab List
Just replace `cmdict/data/words.txt` with your own vocab list. The default one is [derekchuank/high-frequency-vocabulary](https://github.com/derekchuank/high-frequency-vocabulary/blob/master/20k.txt)

## TODO List
- [x] Add cache to reduce requests.
- [ ] Add args to toggle emoji output.
- [x] Add vocabulary auto-completion support.
- [x] Release python module.
- [ ] Give a prompt to enforce saving OOV words. e.g. `xxxxx seems not an English word. Do you want to save xxxxx ? y/[n]`

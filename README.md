 <p align="center"> 
    <img src="./logo.png" alt="logo">
 </p>

# 木 (Ki)

> Easily remember japanese pronounciation with english words you already know!

  Remembering kanji (japanese writing) is hard but sometimes pronounciation can be too.

  Luckily remembering kanji can be tackled using [RtK](https://en.wikipedia.org/wiki/Remembering_the_Kanji_and_Remembering_the_Hanzi) and by building stories about the parts making up the kanji!
  Ki does this but for pronounciation.

  This works by decomposing the sounds of the original japanese word into english words.

  Now you can easily build stories and mnemonics with these new words!
- Check out the online version here (COMING SOON)
- ...or keep reading to use it locally

---


## Installation

Ki is built using Python (backend with flask and core algorithm) and JS (frontend with Vuejs). The online version should be a breeze to use but if you want something local, there is also a small python interface you can run yourself.

You can find the online version here (COMING SOON)

### Clone

- Clone this repo to your local machine using `git clone https://github.com/ThisCakeIsALie/ki.git`
### Setup

> Install all necessary packages from pip and build the C dependencies.

```shell
$ cd ki/backend
$ pip install -r requirements.txt
$ python setup.py install
```

> And start using it!

```shell
$ python main.py 私
```

![Gif showcase](/usage.gif)

---

## How it works

- As input we get kanji and possibly hiragana or katakana
- We translate it all into hiragana and separate it into syllables
- Now we do two approximations. First the syntactic...
  - We partition the syllables
  - For each partition we find words that are syntactically similar to the romanji of the partition parts
  - We assign a cost to each possible partition based on some simple Heuristics
  - And pick the best partition
- And the phonetic approximation...
  - Once again we partition the syllables into groups
  - Instead of finding syntactically similar words we find words whose phonetic (pronounced) prefix matches with that of the group
  - For this, the CMU pronouncing dictionary is used
  - We evaluate each partition based on unnecessary unused syllables and amount of words used
  - There is also a greedy mode which uses a simple length heuristic to find a word faster at the cost of missing out on a possibly better match (This is used in the online version)
- The online version uses a lot of caching and the greedy mode to speedup response time
- If you are interested in details just check out the code! The meat of it is in `approximate.py`

## FAQ

- **Why are there weird words I don't know?**
    Internally this usesthe CMU pronouncing dictionary which has over 100k words. Naturally there will sometimes be weird words. The "looks like" approximation on the other hand only uses the 10k most common english words, so the situation there might be better. Shortening the CMU is on the roadmap though!

---

## License

[![License](http://img.shields.io/:license-gpl_v3-blue.svg?style=flat-square)](http://badges.mit-license.org)

- **[GPL v3.0 License]()**
- Readme adapted from  <a href="https://gist.github.com/fvcproductions/1bfc2d4aecb01a834b46" target="_blank">FVCproductions</a>.
Icons made by <a href="https://www.flaticon.com/authors/freepik" title="Freepik">Freepik</a> from <a href="https://www.flaticon.com/" title="Flaticon"> www.flaticon.com</a>

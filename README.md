![The logo. I suck at that ;)](doc/source/_static/logo.svg)

# GOTO publication

*Citation-based URL/DOI searches*, by [Pierre Beaujean](https://pierrebeaujean.net).
Desktop app version of [that website](https://github.com/pierre-24/goto-publication-old/).

Because the journal, the volume and the page should be enough to find an article (for which, of course, you don't have the DOI, otherwise this is stupid).

**Note:** Since I have a (quantum) chemistry background, I will limit this project to the journals that are in the chemistry and physics fields.
Feel free to fork the project if you want something else :)

## Installation and usage

First, [clone the repository](https://help.github.com/en/articles/cloning-a-repository).

Then, install the requirements you need at least [python 3.6](https://www.python.org/) and the traditional virtualenv

```
python3 -m venv venv
source venv/bin/activate
```

Finally, the [Makefile](./Makefile) contains the install commands:

```bash
make init # install backend and dependancies
```


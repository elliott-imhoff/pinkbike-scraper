# pinkbike-scraper

``pinkbike``: A web scraper for the pinkbike buy/sell page

## Installation 
   
#### Linux/Mac

1) Install [pyenv](https://github.com/pyenv/pyenv)

    1) Make sure you install the [build dependencies](https://github.com/pyenv/pyenv/wiki/Common-build-problems#prerequisites) 
for your system.

    2) Run

            curl https://pyenv.run | bash

    3) Restart your shell so the path changes take effect.

            exec $SHELL
            
2) Install [poetry](https://python-poetry.org/docs/#installation)
3) Install package

        pyenv install $(cat .python-version)
        poetry install
        
## Usage

Within the correct poetry/conda shell, run ``pinkbike --help`` to view available CLI commands.

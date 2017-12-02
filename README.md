# pokreate

A project to "open" and "close" a subreddit by setting it to restricted or 
public mode. It was specifically made for /r/PokemonCreate, so its 
application will be fairly narrow. The other half of what it does is replace 
a specific link text in the sidebar.

## Installation

```commandline
git clone https://github.com/jarhill0/pokreate.git
```

## Requirements

- praw

## Setup

1. Install the requirements (using `pip` or `easy_install` or your method of 
choice).
2. Copy `EXAMPLE_config.py` to `config.py` and fill in the values. Subreddit 
and Username are mandatory. The other three may be left blank if you have a 
[praw.ini](http://praw.readthedocs.io/en/latest/getting_started/configuration/prawini.html#defining-additional-sites)
configured. If you do, set `username` equal to the "site name" of your 
configuration.


## Usage

Invoke the script at a basic level with the command `python` or the command 
`python3` followed by a path to `main.py`. For example, if the script is in 
your current working directory, you can run it with `python3 main.py`. You 
can also call it with a relative or absolute path, same as any other file on 
the command line. 

The script has mandatory options:

- Provide exactly one of `--open` or `--close` (can be shortened to `-o` or 
`-c`, respectively)
- Provide new button text, **surrounded by quotes**

**Example usage**:

```commandline
python3 main.py -o "Submit your request"
python ~/pokreate/main.py --close "Closed for the week"
python3 /home/pi/pokreate/main.py --open "Welcome back!"
```

If you wish to run the script on a specific schedule, look into the UNIX 
utility `crontab`, which can be set up to run commands on a recurring basis.
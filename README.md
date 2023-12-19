# workshop

Toy code and proof-of-concepts, not for production

---------------------------

### Introduction

This repo must never see the light of day. The code may move to production, but this repo will never go public!

#### So there's a chance this repo might go public?

There is no chance this repo will ever go public.

### Notes 

There are no protections on any branches, be kind, rewind.

Please work on different tasks in different branches and be descriptive so we know where to find which toys.

-----------------------------

# Set up tutorials

> ## HUGE SUGGESTION:
> Do these things in this order, I had a whale of a time jumping around between them, they're best done in order
> to reduce unnecessary finagling 

## Using the Python virtual environment

> Reference: https://docs.python.org/3/tutorial/venv.html

This process first initializes a Python virtual environment in a directory specially titled for it, then activates
that environment in your shell. Once you're "in" the venv, you will install all the dependencies that are outlined 
in the requirements.txt file.

Going forward, you may want to remember step 2, or define a run configuration that uses it. That will be the "version"
of python that the project will be required to work with.

Process (Windows):
1. (cd to workshop)                 `$ python -m venv .venv`
2. (should have created /.venv)     `$ .venv\Scripts\activate`
3. (you are now using the venv)     `$ python -m pip install -r requirements.txt`

Process (Unix):
1. (cd to workshop)                 `$ python -m venv .venv`
2. (should have created /.venv)     `$ source .venv/bin/activate`
3. (you are now using the venv)     `$ python -m pip install -r requirements.txt`

## Using Doxygen and doxypypy

### Installing Doxygen

Doxygen is not a Python module and must be installed by a package manager or directly from their site.
See https://www.doxygen.nl/manual/install.html for their tutorials on installation. I would **HIGHLY** recommend
using a package manager as I will be guiding through in the following section, it is far more portable and easy.

#### Installing Doxygen with scoop (Windows)

> This section assumes that you have the scoop package manager installed, see https://scoop.sh/ if you do not 
have scoop installed yet. Big ups, very easy to use.

Process (Windows):
1. $ `scoop install doxygen`

_yes, it is seriously that easy_

#### Installing Doxygen with homebrew (Unix)

> This section assumes that you have the homebrew package manager installed, see https://brew.sh/ if you do not 
have homebrew installed yet. Big ups, very easy to use.

Process (Unix):
1. $ `brew install doxygen`

_yes, it is seriously that easy_

#### Using doxypypy with Doxygen

> Doxypypy is a python module, and it was included in the venv installation, so you don't need to install it. What you
_do_ need to do is put a script that connects the two tools onto your PATH so that Doxygen knows where to find it.

Doxypypy will "filter" our Python docstrings into Java docstrings so that Doxygen can make effective use of it. This
is done via the scripts in the /docs folder (py_filter and py_filter.bat), so we need Doxygen to be able to find them.

##### On Windows... 

this is a little annoying, but this should get you through it pain-free. WARNING: When editing your 
system variables, be pretty careful as it can introduce some annoying issues. For this reason, there is a step in
this walkthrough that backs up your PATH to a file, you can skip this if you are confident.

This next step refers to the "/docs" directory, this is in your local workshop repo (something like "~/workshop/docs")

Process (Windows):
0. (back up your path before starting)      `$ echo $Env:PATH > path_backup.txt`
1. (copy the path to the /docs directory)   `$ $Env:PATH = "$($Env:PATH);<docs directory>"`

If anything is broken or you just want that undone, use this script to restore your backup

Process (Windows):
1. `$ $Env:PATH = Get-Content -Path <path_to_backup> -Raw`

##### On Unix systems...

this _feels_ far less annoying, maybe just because Unix just feels nicer in the terminal? It's essentially the same
process as on Windows, so I'll include the steps for backup.

Process (Unix):
0. (back up your path before starting)      `$ printf $PATH > path_backup.txt`
1. (copy the path to the /docs directory)   `$ export PATH=$PATH:"<docs directory>"`

If anything is broken or you just want that undone, use this script to restore your backup

Process (Unix):
1. `$ export PATH=$(cat <path_to_backup>)`

#### Generating documentation with Doxygen + doxypypy

Now that the stage is set, you should be able to call the following script which will generate documentation at this
location: [docs/output/html/index.html](docs/output/html/index.html) (hint: open in browser to see it displayed). This process is identical
on Windows or Unix.

> You'll need to call this function any time you want the documentation to update, it does NOT do so dynamically.

Process (Windows/Unix):
1. `$ Doxygen docs/Doxyfile`

## Linting with BLACK

> BLACK will already be installed via the virtual environment, so this is a super simple step

BLACK will reformat code to follow a common format standard, this may change the appearance of your code significantly.
This is a feature, not a bug! You can feel free to code however you like, use what ever format you want, and then
BLACK will magically make it look like code written by some of the leading developers (Django, SQLAlchemy, Facebook, 
Mozilla, the list goes on https://github.com/psf/black).

Process (Windows/Unix):
1. `$ black src`

NOTE: You can replace the argument `src` with any directory if you'd like to change the target.

## Testing with pytest

> pytest will already be installed via the virtual environment, so this is a super simple step'

Pytest automatically discovers tests that have been written and included in the /tests directory, these files MUST
be titled like `test_very_descriptive_name_of_the_tests_within.py` with the `test_` part being most vital for 
discovery, and the rest of the long ass name being vital for knowing what tests are failing, because the name of the
file is what is first reflected when running the tests.

Process (Windows/Unix):
1. `$ pytest`

NOTE: This will run all the discoverable tests.

## Using ConfigMaker.py

> This is the standard method of configuring your local settings, this way we are all on the same page

This script will generate all the necessary .ini files for FHIRType to work, you can make changes to these files
as you need/wish and they will not affect any other contributor's environment. Make sure you navigate to ~/workshop.

First you should make a copy of each of the files 
[config/default_endpoints.txt](src/fhirtypepkg/config/default_endpoints.txt) and
[config/default_localdb.txt](src/fhirtypepkg/config/default_localdb.txt) and name them `local_endpoints.txt` and 
`local_endpoints.txt` respectively. These are where you can make changes to set up your configuration persistently 
for now.   

Process (Windows/Unix):
1. `$ python src/configMaker.py -endpoints Endpoints src/fhirtypepkg/config/local_endpoints.txt -database LocalDatabase src/fhirtypepkg/config/local_localdb.txt -logger Logging blank`

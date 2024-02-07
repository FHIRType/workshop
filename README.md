FHIRType
========

The FHIRType API serves consistently formatted healthcare provider data from numerous
FHIR Standard endpoints.

Try out the API at http://localhost/hello-world

### Example request
`GET /practitioner?name=dr.seuss`
```
{"Endpoint":"Endpoint_data",
"Date Retrieved":"Date Retrieved_data",
"FullName":"FullName_data",
"NPI":"NPI_data",
"FirstName":"FirstName_data",
"LastName":"LastName_data",
"Gender":"Gender_data",
"Taxonomy":"Taxonomy_data",
"GroupName":"GroupName_data",
"ADD1":"ADD1_data",
"ADD2":"ADD2_data",
"City":"City_data",
"State":"State_data",
"Zip":"Zip_data",
"Phone":"Phone_data",
"Fax":"Fax_data",
"Email":"Email_data",
"lat":"lat_data",
"lng":"lng_data",
"LastPracUpdate":"LastPracUpdate_data",
"LastPracRoleUpdate":"LastPracRoleUpdate_data",
"LastLocationUpdate":"LastLocationUpdate_data",
"AccuracyScore": "acc_score_data"}
}
```

---------------------------

# Table of Contents

1. [Introduction](#introduction)
2. [How-To Guides](#how-to-guides)
   1. [Set Up Guides](#set-up-guides)
      1. [Python Virtual Environment (venv)](#using-the-python-virtual-environment)
      2. [Doxygen and doxypypy Documentation](#using-doxygen-and-doxypypy)
         1. [Documentation Output](#link-to-documentation-rending)   
      3. [Linting with BLACK](#linting-with-black)
      4. [Testing with Pytest](#testing-with-pytest)
      5. [Generating Config Files (ConfigMaker.py)](#using-configmakerpy)
      6. [Setting up glcoud to Access VM (Google Cloud Services)](#setting-up-gcloud)
   2. [Usage Guides](#usage-guides)
      1. [Accessing the Virtual Machine](#accessing-the-virtual-machine)
      2. [(DRAFT) Running the Docker Image ](#draft-running-docker-image)

---------------------------

## Introduction

This README is meant mostly for the development team's reference while under initial development,
it will need to be re-written for production.

FHIRType is the name of this project as well as the name of the group of students developing it
under Oregon State University's Computer Science Bachelor's Capstone Project.

Q: Is there a chance this repo might go public?
: A: There is almost no chance this repo will ever go public, it would need to undergo some extensive commit revisions.

Q: How should I name my branches/commits?
: A: Refer to the [current SDP](https://docs.google.com/document/d/1_WIITrlvQwmHt3foUDXqfedzsbw-d8mtc-FADkaNIOk/edit?usp=drive_link).

~~This repo must never see the light of day. The code may move to production, but this repo will never go public!~~

-----------------------------

## How-To Guides

These guides are written for the development team and very few if any actually describe
how to use the API.

### Set up guides

> #### HUGE SUGGESTION:
> Do these things in this order, I had a whale of a time jumping around between them, they're best done in order
> to reduce unnecessary finagling 

#### Using the Python virtual environment

> Reference: https://docs.python.org/3/tutorial/venv.html

This process first initializes a Python virtual environment in a directory specially titled for it, then activates
that environment in your shell. Once you're "in" the venv, you will install all the dependencies that are outlined 
in the requirements.txt file.

Going forward, you may want to remember step 2, or define a run configuration that uses it. That will be the "version"
of python that the project will be required to work with.

Process (Windows):
1. (cd to workshop)                 `python -m venv .venv`
2. (should have created /.venv)     `.venv\Scripts\activate`
3. (you are now using the venv)     `python -m pip install -r requirements.txt`

Process (Unix):
1. (cd to workshop)                 `python -m venv .venv`
2. (should have created /.venv)     `source .venv/bin/activate`
3. (you are now using the venv)     `python -m pip install -r requirements.txt`

#### Using Doxygen and doxypypy

##### Link to documentation rending

[Doxygen HTML Output](docs/output/html/index.html)

##### Installing Doxygen

Doxygen is not a Python module and must be installed by a package manager or directly from their site.
See https://www.doxygen.nl/manual/install.html for their tutorials on installation. I would **HIGHLY** recommend
using a package manager as I will be guiding through in the following section, it is far more portable and easy.

###### Installing Doxygen with scoop (Windows)

> This section assumes that you have the scoop package manager installed, see https://scoop.sh/ if you do not 
have scoop installed yet. Big ups, very easy to use.

Process (Windows):
1. `scoop install doxygen`

_yes, it is seriously that easy_

###### Installing Doxygen with homebrew (Unix)

> This section assumes that you have the homebrew package manager installed, see https://brew.sh/ if you do not 
have homebrew installed yet. Big ups, very easy to use.

Process (Unix):
1. `brew install doxygen`

_yes, it is seriously that easy_

###### Using doxypypy with Doxygen

> Doxypypy is a python module, and it was included in the venv installation, so you don't need to install it. What you
_do_ need to do is put a script that connects the two tools onto your PATH so that Doxygen knows where to find it.

Doxypypy will "filter" our Python docstrings into Java docstrings so that Doxygen can make effective use of it. This
is done via the scripts in the /docs folder (py_filter and py_filter.bat), so we need Doxygen to be able to find them.

###### On Windows... 

this is a little annoying, but this should get you through it pain-free. WARNING: When editing your 
system variables, be pretty careful as it can introduce some annoying issues. For this reason, there is a step in
this walkthrough that backs up your PATH to a file, you can skip this if you are confident.

This next step refers to the "/docs" directory, this is in your local workshop repo (something like "~/workshop/docs")

Process (Windows):
0. (back up your path before starting)      `echo $Env:PATH > path_backup.txt`
1. (copy the path to the /docs directory)   `$Env:PATH = "$($Env:PATH);<docs directory>"`

If anything is broken or you just want that undone, use this script to restore your backup

Process (Windows):
1. `$Env:PATH = Get-Content -Path <path_to_backup> -Raw`

###### On Unix systems...

this _feels_ far less annoying, maybe just because Unix just feels nicer in the terminal? It's essentially the same
process as on Windows, so I'll include the steps for backup.

Process (Unix):
0. (back up your path before starting)      `printf $PATH > path_backup.txt`
1. (copy the path to the /docs directory)   `export PATH=$PATH:"<docs directory>"`

If anything is broken or you just want that undone, use this script to restore your backup

Process (Unix):
1. `export PATH=$(cat <path_to_backup>)`

###### Generating documentation with Doxygen + doxypypy

Now that the stage is set, you should be able to call the following script which will generate documentation at this
location: [docs/output/html/index.html](docs/output/html/index.html) (hint: open in browser to see it displayed). This process is identical
on Windows or Unix.

> You'll need to call this function any time you want the documentation to update, it does NOT do so dynamically.

Process (Windows/Unix):
1. `Doxygen docs/Doxyfile`

#### Linting with BLACK

> BLACK will already be installed via the virtual environment, so this is a super simple step

BLACK will reformat code to follow a common format standard, this may change the appearance of your code significantly.
This is a feature, not a bug! You can feel free to code however you like, use what ever format you want, and then
BLACK will magically make it look like code written by some of the leading developers (Django, SQLAlchemy, Facebook, 
Mozilla, the list goes on https://github.com/psf/black).

Process (Windows/Unix):
1. `black FhirCapstoneProject`

NOTE: You can replace the argument `FhirCapstoneProject` with any directory/file if you'd like to change the target.

#### Testing with pytest

> pytest will already be installed via the virtual environment, so this is a super simple step

Pytest automatically discovers tests that have been written and included in the /tests directory, these files MUST
be titled like `test_very_descriptive_name_of_the_tests_within.py` with the `test_` part being most vital for 
discovery, and the rest of the long ass name being vital for knowing what tests are failing, because the name of the
file is what is first reflected when running the tests.

Process (Windows/Unix):
1. `pytest`

NOTE: This will run all the discoverable tests.

#### Using ConfigMaker.py

> This is the standard method of configuring your local settings, this way we are all on the same page

This script will generate all the necessary .ini files for FHIRType to work, you can make changes to these files
as you need/wish, and they will not affect any other contributor's environment. Make sure you navigate to ~/workshop.

First you should make a copy of each of the files 
[config/default_endpoints.txt](FhirCapstoneProject/fhirtypepkg/config/default_endpoints.txt) and
[config/default_localdb.txt](FhirCapstoneProject/fhirtypepkg/config/default_localdb.txt) and name them `local_endpoints.txt` and 
`local_endpoints.txt` respectively. These are where you can make changes to set up your configuration persistently 
for now.   

Process (Windows/Unix):
```
python FhirCapstoneProject/configMaker.py \
   -endpoints Endpoints FhirCapstoneProject/fhirtypepkg/config/default_endpoints.txt \
   -logger Logging blank
```
(Single line option): `python FhirCapstoneProject/configMaker.py -endpoints Endpoints FhirCapstoneProject/fhirtypepkg/config/default_endpoints.txt -logger Logging blank`


#### Setting up gcloud

> This step is a prerequisite to SSH (virtual console) into the remote virtual machine

Process (Windows):
1. `scoop install gcloud`
2. `gcloud init`
3. Enter `y` to authenticate your gmail account, MAKE SURE YOU USE THE ONE ATTACHED TO THE PROJECT
4. Select the cloud project `fhirtype-osu-cs`
5. Enter `y` to set a default region and zone
6. Set a default region and zone to `us-central1-a`

Process (OSX):
1. `brew install --cask google-cloud-sdk`
2. `gcloud init`
3. Enter `y` to authenticate your gmail account, MAKE SURE YOU USE THE ONE ATTACHED TO THE PROJECT
4. Select the cloud project `fhirtype-osu-cs`
5. Enter `y` to set a default region and zone
6. Set a default region and zone to `us-central1-a`

--------------------

### Usage Guides

#### Accessing the Virtual Machine

> You can do this a couple of ways, included are two options tested on Trenton's PC.

> ###### NOTE
> 
> If you can't connect, it could be that the VM has stopped due to a number of problems (overuse, time out, etc. 
> because we use the free tier).
> Log into the Google Cloud Services dashboard and start the VM with the three-dot menu.

> ###### NOTE
> 
> You need to pair an SSH key with GitHub to your user in the virtual machine in order to use GitHub on the VM 
> 
> https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent

##### SSH From Google Cloud Webapp

1. Go to: https://console.cloud.google.com/compute/instances?hl=en&project=fhirtype-osu-cs
2. Under VM instances, on the far right, click `SSH`
 [![SSH Option highlighted](https://i.postimg.cc/Z5t7QTpB/image.png)](https://postimg.cc/6ycf2xHt)
3. This will prompt you to authorize SSH, then open a remote terminal in a browser window.

##### SSH From PuTTY (With PyCharm run configuration)

> This option allows you to open a terminal from PyCharm with one click

1. Edit the run configuration associated with `/scripts/ssh-fhirtype-osu-cs.sh` > More Run/Debug > Modify Run Configuration...
2. Enter `-u [your ONID username]` into the _Script Options_
3. Uncheck "Execute in Terminal" if you're on Windows
4. Trenton has set up a user for you manually, there's no integration with OSU (refer to Discord for your password).
5. In the _Interpreter Path_ field, navigate to and select the git-bash.exe from your local Git installation

If this all succeeds, when you run that configuration a git-bash terminal will open, which MAY then open a PuTTY terminal,
weirdly you have to keep them both open.

###### Accessing the shared directory

> The directory `/home/public` is accessible by all users, there is a clone of the workshop in there

#### [DRAFT] Running Docker Image

after init'ing

`sudo docker compose up --build -d`
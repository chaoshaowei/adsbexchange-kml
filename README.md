# ADS-B Exchange 2 KML

A download tool for downloading [ADS-B Exchange](https://globe.adsbexchange.com/)(ADS-B Tracking Map) tracks, and export to KML/GPX formats.

## Table of content

- [ADS-B Exchange 2 KML](#ads-b-exchange-2-kml)
  - [Table of content](#table-of-content)
  - [Getting the tool](#getting-the-tool)
    - [Presrequisites](#presrequisites)
    - [Installation](#installation)
  - [Using the tool](#using-the-tool)
  - [Notice](#notice)

## Getting the tool

### Presrequisites

This tool uses [python3](https://www.python.org/) and [requests module](https://pypi.org/project/requests/) of python3.

Download and install python3 from [here](https://www.python.org/downloads/), and install `requests` using:

```
pip3 install requests
```

### Installation

You can either use `git` to install the tool, or just download the whole tool in `.zip` format from github

Install:
```
git clone https://github.com/chaoshaowei/adsbexchange-kml.git
```

Update:
```
git pull https://github.com/chaoshaowei/adsbexchange-kml.git
```

## Using the tool

Simply edit the reg and the date in `download.py`, then run the python script.

Currently, the option of using the code requires you to modify the `download.py` file, and change the reg and/or the date.

Maybe there will be graphical interface to get tracks in the future.

## Notice

This tool is only provided for personal, non-profit research, or non-profit education use only, as per [it's legal and privacy](https://www.adsbexchange.com/legal-and-privacy/).

Use the tool on your own responsibility.

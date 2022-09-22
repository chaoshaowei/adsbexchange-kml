# ADS-B Exchange 2 KML

A download tool for downloading [ADS-B Exchange](https://globe.adsbexchange.com/)(ADS-B Tracking Map) tracks, and export to KML/GPX formats.

## Table of content

- [ADS-B Exchange 2 KML](#ads-b-exchange-2-kml)
  - [Table of content](#table-of-content)
  - [Getting the tool](#getting-the-tool)
    - [Presrequisites](#presrequisites)
    - [Installation](#installation)
  - [Using the tool](#using-the-tool)
    - [Parameters](#parameters)
  - [Limitations](#limitations)
  - [Notice](#notice)

## Getting the tool

### Presrequisites

This tool uses [python3](https://www.python.org/) and [requests module](https://pypi.org/project/requests/) of python3.

Download and install python3 from [here](https://www.python.org/downloads/), and install `requests` using:

```
pip3 install requests
```

### Installation

You can either use `git` to install the tool, or just download the whole tool in `.zip` format from [github](https://github.com/chaoshaowei/adsbexchange-kml/archive/refs/heads/master.zip)

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

The output file will be renamed based on the plane's registration, and the requested date. If [`DIVIDE_LEG`] option is selected, divided legs will be renamed based on the time of the last point of the leg, localized into timezone described in [`OUTPUT_TZ`].

Currently, the option of using the code requires you to modify the `download.py` file, and change the reg and/or the date.

Maybe there will be graphical interface to get tracks in the future.

### Parameters

Tool Options:

* `DEBUG` = [`True`/`False`]: Display debug messages
* `FORCE_SEARCH` = [`True`/`False`]: For future use
* `SAVE_RESPONSE` = [`True`/`False`]: Save the RAW responses from adsbexchange.com
* `DIVIDE_LEG` = [`True`/`False`]: Divide the 24 hours period into legs, if the airplane hasn't been moving for [`DIVISOR_SECOND`] seconds
* `DIVISOR_SECOND` = [`Number`]: Prescribed as above
* `OUTPUT_TZ_NUM` = [`Number`]: How many hours will the output format of divided legs be varied from GMT
* `OUTPUT_KML` = [`True`/`False`]: Export `KML` Format
* `OUTPUT_GPX` = [`True`/`False`]: Export `GPX` Format

Requesting tracks:

* `REG_ID` = [`String`]: The requested registration
* `Y/M/D` = [`Number`]: The requested GMT date

## Limitations

This tool relies on the Transponder Mode-S code of the airplane, and can only download 24 hour period of a GMT day of an airplane once a time.

Currently, there are only Mode-s code of planes owned by EVA Flight training academy, but I will implement the ability to lookup Mode-S code in the future.

## Notice

This tool is only provided for personal, non-profit research, or non-profit education use only, as per [it's legal and privacy](https://www.adsbexchange.com/legal-and-privacy/).

Use the tool on your own responsibility.

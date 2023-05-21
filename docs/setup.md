# Setup

!!! warning "Deprecated Note"

    Originally this note read:

    > Make sure you have enough storage space for the data archives. The amount of storage required will vary based on how much data you download and how far back you want to go, but I recommend a minimum of 100GB. The full uncompressed archive of comments and submissions is somewhere around ~14TB, though the exact value is uncertain.

    However, the pushshift archives are down now. Accordingly this package no longer contains the functionality to download them. You will have to find them on your own. You can visit the [data access](data.md) page to check you meet the requirements for the cleaned datasets/service I maintain.

!!! info "Device"
    This package has only been tested on MacOS. If you run into a bug it may be attributable to this.

!!! bug "Support"
    If you run into a bug, please submit a GitHub Issue. I will try to address it time permitting.

## Dependencies

!!! info "Software: Prerequisites"
    Recommended installation before continuing.

    - [miniconda](https://docs.conda.io/en/latest/miniconda.html)

??? info "Software: Automated"
    Installed via included CLI during the setup process. You can install separately if you prefer.

    - [elasticsearch](https://www.elastic.co/downloads/elasticsearch)

??? info "Python Packages"
    These are installed automatically. Package dependencies vary based on whether you install the package as a developer or a user. For the former, check the [requirements.txt](https://github.com/harttraveller/psarch/blob/main/requirements.txt) file. For the latter, check the [setup.py](https://github.com/harttraveller/psarch/blob/main/setup.py) file. The developer dependencies are a superset of the user dependencies.

## Installation

### User Installation

First, install the psarch package using pip.

```bash
pip install psarch
```

When you install the package, it creates a hidden folder in your home directory: `.psarch`. This is where the elasticsearch instance is stored. If you would like to change the location data is cached, you can use the CLI command.

```bash
psarch location update
```

Download elasticsearch. You can do this with the following command. If you have set your cache directory, elasticsearch v8.7.0 will be downloaded in the `<cache>/elasticsearch-8.7.0` directory.

??? note "Using Docker"
    You can also use docker to set up elasticsearch, as documented [here](https://dylancastillo.co/elasticsearch-python/). The caveat with this is that (as I understand) the docker container will operate in memory while active, and thus the amount of data you can handle will be restricted to a fraction of the RAM available on your system.

??? note "Supported Systems"
    At the moment I've only implemented the download wizard for elasticsearch for MacOS. If you are on a different system, you can download it manually [here](https://www.elastic.co/downloads/elasticsearch) and move the unpacked folder into your cache directory. There may still be issues, but if you submit them on GitHub I will try to address them when I have time.

```bash
psarch elastic download
```

Once the elasticsearch download is complete, run the following command to test it and ensure it is working properly.

```bash
psarch elastic test
```

If it is not working properly, then running the following command and changing the security policy to false may fix the issue, though it also disables security features in elasticsearch. This should not be an issue if you are only running this locally.

```bash
psarch elastic security
```

After changing the security policy, attempt the test again. If it works, continue, if it does not work please submit a GitHub issue.

The next step involves actually downloading the data. To reduce the stress on the pushshift servers, I've processed the data and uploaded normalized and filtered datasets to kaggle. These datasets are smaller, however there is information loss. If you would like to download the original data, and parse it with a custom data ingestion pipeline, interfaces are available - details on which are included on the advanced usage page.

```bash
psarch download
```

You will have to select the years for which you want to download the data.


Finally, when you have finished downloading the data, you can start the elasticsearch instance and ingest the data into the instance.

```bash
psarch ingest
```


### Developer Installation


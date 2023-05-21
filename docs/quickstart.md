# Quickstart

??? warning "Deprecated Note"

    Originally this note read:

    > Make sure you have enough storage space for the data archives. The amount of storage required will vary based on how much data you download and how far back you want to go, but I recommend a minimum of 100GB. The full uncompressed archive of comments and submissions is somewhere around ~14TB, though the exact value is uncertain.

    However, the pushshift archives are down now. Accordingly this package no longer contains the functionality to download them. You will have to find them on your own, or visit the [data access](data.md) page to check you meet the requirements for the cleaned datasets/service I maintain.


## Installation

First, install the psarch package using pip.

```bash
pip install psarch
```



### Setup

Set your working cache directory. This is where the raw data, as well as the elasticsearch instance will be cached. You can do this with the following CLI command. Note that due to the size of the datasets involved, it may be prudent to use an external drive.

```bash
psarch cache update
```

Download elasticsearch. You can do this with the following command. If you have set your cache directory, elasticsearch v8.7.0 will be downloaded in the `<cache>/elasticsearch-8.7.0` directory.

??? Note "Using Docker"
    You can also use docker to set up elasticsearch, as documented [here](https://dylancastillo.co/elasticsearch-python/). The caveat with this is that (as I understand) the docker container will operate in memory while active, and thus the amount of data you can handle will be restricted to a fraction of the RAM available on your system.

??? Note "Supported Systems"
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







view|open|update



!!! Note
    The setup wizard process will take anywhere from a few minutes to a few days, depending on the following factors:

    1. Your internet speed.
    2. The processing power of your computer.
    3. The read/write speed of the disk your working directory is stored on.

    You can leave the process running in the background.


### Usage

At the moment, you will need to start two independent processes in order to use the interface.


## Details

### Elasticsearch



https://www.elastic.co/downloads/elasticsearch

Note that at the moment you must disable the security features in the `config/elasticsearch.yml` file. I don't expect this should be an issue, as this is purely meant to be a locally hosted instance.

```yaml
# Enable security features
xpack.security.enabled: false
```

While I have not tested it, I do not expect that using docker would work in this case, unless you have hundreds of GB of RAM. If you do

### Storage


Also, you will need to have a storage drive with sufficient capacity to store the archive. The original pushshift archive of comments and submissions is ~2TB when compressed, and ~14TB uncompressed. The archive size has been reduced



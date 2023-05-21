


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



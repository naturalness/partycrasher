# Partycrasher
Automated scalable crash bucketing!

Partycrasher is a framework for automatically gruping crash
reports based on the contents of stacktraces and other
data available at the time of a crash. You can read the [paper about it](https://peerj.com/preprints/1705/).

# Current Status

Partycrasher does not yet have a interface. To use it, import
the bucketer that you prefer.

# Use

Partycrasher requires [Elastic (ElasticSearch)](https://www.elastic.co/).

# Licensing

Assume that Partycrasher is licensed under the [GPL3+](LICENSE) unless otherwise
specified.

# Citation

If you use this code we would appreciate if you cited the paper!

~~~
@article{10.7287/peerj.preprints.1705v1,
 title = {The unreasonable effectiveness of traditional information retrieval in crash report deduplication},
 author = {Campbell, Joshua Charles and Santos, Eddie Antonio and Hindle, Abram},
 year = {2016},
 month = {2},
 volume = {4},
 pages = {e1705v1},
 journal = {PeerJ PrePrints},
 issn = {2167-9843},
 url = {https://dx.doi.org/10.7287/peerj.preprints.1705v1},
 doi = {10.7287/peerj.preprints.1705v1}
}
~~~

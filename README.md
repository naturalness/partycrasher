# PartyCrasher

[![Build Status](https://travis-ci.org/naturalness/partycrasher.svg?branch=master)](https://travis-ci.org/naturalness/partycrasher)

PartyCrasher is a framework for automatically grouping crash reports
based on the contents of stack traces and other
data available at the time of a crash. You can read the [paper about it](https://peerj.com/preprints/1705/).

# Install

> Note that the provided `Dockerfile` creates a container that performs
> all of the following steps for you.

PartyCrasher requires [Elastic (ElasticSearch)](https://www.elastic.co/).

To install the PartyCrasher REST client, install ElasticSearch; then
install the Python dependencies (you may want to install these within
a [virtualenv](http://docs.python-guide.org/en/latest/dev/virtualenvs/)
if that's your taste).

```sh
pip install -r requirements.txt
```

To install the UI, you must have NPM and Bower.

```sh
npm install -g bower
cd partycrasher/ngapp
bower install
```

# Usage

Run the REST service:

```sh
python partycrasher/rest_service.py
```

The HTTP service will now be listening on port 5000. Refer to the [API
Docs][] for further usage.

[API Docs]: http://partycrasher.readthedocs.io/en/latest/rest-api.html

# Licensing

Assume that PartyCrasher is licensed under the [GPL3+](LICENSE) unless otherwise
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

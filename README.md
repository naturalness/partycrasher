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

# Uploading Test Data

> **Note**: This will delete *all* data in the existing PartyCrasher
> instance.

To download test data and upload it to PartyCrasher, simply type:

```sh
$ make buckettest
```

# Licensing

Assume that PartyCrasher is licensed under the [GPL3+](LICENSE) unless otherwise
specified.

# Citation

If you use this code we would appreciate if you cited the paper!

~~~
@inproceedings{Campbell:2016:UET:2901739.2901766,
   author = {Campbell, Joshua Charles and Santos, Eddie Antonio and Hindle, Abram},
   title = {The Unreasonable Effectiveness of Traditional Information Retrieval in Crash Report Deduplication},
   booktitle = {Proceedings of the 13th International Workshop on Mining Software Repositories},
   series = {MSR '16},
   year = {2016},
   isbn = {978-1-4503-4186-8},
   location = {Austin, Texas},
   pages = {269--280},
   numpages = {12},
   url = {http://doi.acm.org/10.1145/2901739.2901766},
   doi = {10.1145/2901739.2901766},
   acmid = {2901766},
   publisher = {ACM},
   address = {New York, NY, USA},
   keywords = {automatic crash reporting, call stack trace, contextual information, deduplication, duplicate bug reports, duplicate crash report, free/open source software, information retrieval, software engineering},
}
~~~

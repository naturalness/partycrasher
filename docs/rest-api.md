API 0.0.2
=========

Overview
--------

 - Like the GitHub API, this contains full-qualified URLs to resources (based on the User-Agent facing host).
 - Like BugParty, all paths are prefixed with `/partycrasher/:project/`
 - There are three entities:
   - Buckets
   - Reports
   - Projects (maintained mostly for psychological acceptability, and compatibility with  BugParty)

Accept new crash
-----

> `POST /partycrasher/:project/reports`

```http
HTTP/1.1 201 Created
Location: https://domain.tld/partycrasher/<project>/report/<report id>/

{
    "id": <report-id>,
    "bucket_id": <bucket-id>,
    "bucket_url": "https://domain.tld/partycrasher/<project>/buckets/<T=[default]>/<bucket-id>"
}
```

### Possible errors

When an _identical_ (not just duplicate) crash is posted:

```http
HTTP/1.1 303 See Other
Location: https://domain.tld/partycrasher/<project>/report/<report id>/
````

Categorize crash (dry-run)
------

> `POST /partycrasher/:project/reports/dry-run`

```http
HTTP/1.1 202 Accepted

{
    "bucket_id": <bucket-id>,
    "bucket_url": "https://domain.tld/partycrasher/<project>/buckets/<T=[default]>/<bucket-id>"
}
```

Accept multiple reports
-----

> `POST /partycrasher/:project/reports`

```http
HTTP/1.1 201 Created

[
    {
        "id": <report-id 1>,
        "bucket_id": <bucket-id 1>,
        "bucket_url": "https://domain.tld/partycrasher/<project>/buckets/<T=[default]>/<bucket-id 1>"
    },
    {
        "id": <report-id 2>,
        "bucket_id": <bucket-id 2>,
        "bucket_url": "https://domain.tld/partycrasher/<project>/buckets/<T=[default]>/<bucket-id 2>"
    },
    ...
]
```


Get information on a crash
--------------------------

> `GET /partycrasher/:project/reports/:report_id`

```http
HTTP/1.1 200 OK
Link: <https://domain.tld/partycrasher/<project>/buckets/<T=[default]>/<bucket-id>; rel="related",

{
    "id": <report-id>,
    "buckets": {
        "3.5": {
            "id": <bucket-id, T=3.5>,
            "url": "https://domain.tld/partycrasher/<project>/buckets/3.5/<bucket-id>"
        },
        "4.0": {
            "id": <bucket-id, T=4.0>,
            "url": "https://domain.tld/partycrasher/<project>/buckets/4.0/<bucket-id>"
        },
        "4.5": {
            "id": <bucket-id, T=3.5>,
            "url": "https://domain.tld/partycrasher/<project>/buckets/4.5/<bucket-id>"
        },
        ...
    },
    "threads": [
        {
            "stacktrace": [...],
        },
        ...
    ],
    "comment": {
    },
    "os": <os>,
    "platform: <x86/arm, etc.>
}
```

Override bucket assignment
-----

> `PATCH /partycrasher/:project/reports`

### Data 

```json
{
    "buckets: {
        "<T=[default]>": <new bucket-id>
    }
}
```

```http
HTTP/1.1 200 OK
Link: <https://domain.tld/partycrasher/<project>/buckets/<T=[default]>/<bucket-id>; rel="related",

{
    "id": <report-id>,
    "bucket_id": <bucket-id>,
    "bucket_url": "https://domain.tld/partycrasher/<project>/buckets/<T=[default]>/<bucket-id>"
}
```


Remove report
-----

> `DELETE /partycrasher/:project/reports/:report_id`


```http
HTTP/1.1 204 No Content
```

Get summary about a bucket
-------------------------

> `GET /partycrasher/:project/buckets/:threshold/:bucket_id`

```http
HTTP/1.1 200 OK

{
    "id": <bucket-id>,
    "num-reports": <number-of-crashes>,
    "top-reports": [
        "https://domain.tld/partycrasher/<project>/reports/<report-id 1>",
        "https://domain.tld/partycrasher/<project>/reports/<report-id 2>"
    ]
}
```

Get summary for all buckets
-----------------------------

`GET /partycrasher/:project/buckets/<threshold>?since=<date>`

```http
HTTP/1.1 200 OK

{
    "since": <Date>,
    "top-buckets": [
        {
            "id": <bucket-id 1>,
            "url": "https://domain.tld/partycrasher/<project>/buckets/3.5/<bucket-id>",
            "num-reports-in-period": <num crashes>,
            "num-reports-total": <num reports>
        }
    ]
}
```

Viewing per-project configuration
----

> `GET /partycrasher/:project/config`

```http
HTTP/1.1 200 OK

{
    "default-threshold": <float>
}
```

Setting per-project configuration
---------------------------------

> `PATCH /partycrasher/:project/config`

### Data

```json
{
    "default-threshold": <float>
}
```

```http
HTTP/1.1 200 OK

{
    "default-threshold": <float>
}
```

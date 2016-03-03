# https://hub.docker.com/_/python/
FROM python:2-onbuild

# To build:
# docker build -t partycrasher .

# To run:
# docker run -it --rm --name partycrasher partycrasher

# PartyCrasher will be exposed on port 5000

MAINTAINER Eddie Antonio Santos <easantos@ualberta.ca>

CMD [ "python", "partycrasher/rest_service.py", "5000" ]

EXPOSE 5000

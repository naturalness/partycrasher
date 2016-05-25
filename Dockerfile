# https://hub.docker.com/_/python/
FROM python:2-onbuild

# To build:
# docker build -t partycrasher .

# To run:
# docker run -it --rm --name partycrasher partycrasher

# PartyCrasher will be exposed on port 5000

MAINTAINER Eddie Antonio Santos <easantos@ualberta.ca>

EXPOSE 5000

# Set up NPM AND Bower for some dumb reason... :S
RUN cd /usr/src/app/partycrasher/ngapp && \
    curl -sL https://deb.nodesource.com/setup_4.x | bash - && \
    apt-get install -y nodejs && \
    npm install -g bower && \
    bower --allow-root --force-latest install

CMD [ "python", "partycrasher/rest_service.py", "5000" ]

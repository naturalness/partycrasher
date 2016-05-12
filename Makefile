# Does common Docker tasks

IMAGE_NAME = partycrasher:latest
EXTERNAL_PORT = 5000

.PHONY: build
build:
	docker build --tag $(IMAGE_NAME) .

.PHONY: run
run:
	docker run -d -p $(EXTERNAL_PORT):5000/tcp --name partycrasher $(IMAGE_NAME)

.PHONY: kill
kill:
	docker rm -f partycrasher

.PHONY: test
test: kill build
	docker run -t -i --name partycrasher $(IMAGE_NAME) python setup.py test

.PHONY: reset
reset: build kill run

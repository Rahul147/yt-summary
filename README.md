# YT Summary FastAPI Service

## Overview
YT Summary is a FastAPI service designed to fetch and stream YouTube video captions. This service utilizes Docker for ease of deployment and scalability, providing a straightforward API endpoint to retrieve captions efficiently.

## Features
- YouTube video summarization with local execution on Mistral 7B
- Segments captions based on time markers and employs LangChain for a condensed summary through MapReduce chains

## Getting Started

These instructions will cover usage information and for the docker container 

### Prerequisities

In order to run this container you'll need docker installed.

* [Windows](https://docs.docker.com/windows/started)
* [OS X](https://docs.docker.com/mac/started/)
* [Linux](https://docs.docker.com/linux/started/)

### Usage

#### Container Parameters

Building the image:
```shell
docker build -t yt_summary .
```

Run the container with:

```shell
docker run -d -p 8000:8000 --name yt_summary yt_summary
```

#### API

cURL
```shell
curl "http://localhost:8000/download_captions/?youtube_url=https://www.youtube.com/watch?v=YOUR_VIDEO_ID"
```



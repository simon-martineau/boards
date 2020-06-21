# Boards

> A forum-like backend api designed to have a web app built in front of it.

[![Build Status](https://travis-ci.com/simon-martineau/boards.svg?branch=master)](https://travis-ci.com/simon-martineau/boards)
[![codecov](https://codecov.io/gh/simon-martineau/boards/branch/master/graph/badge.svg)](https://codecov.io/gh/simon-martineau/boards)

## Installation
### Requirements

- docker ([installation](https://docs.docker.com/get-docker/))
- docker-compose ([installation](https://docs.docker.com/compose/install/))

### Clone
Clone this repository using:
```bash
git clone https://github.com/simon-martineau/boards.git
```

### Setup
Perform these steps to quickly get started

**Note:** ports 8000 and 5444 need to be available
```bash
cd boards
docker-compose -f /home/simon/Dev/boards/docker-compose.dev.yml up -d
```
And that's all you need!
The api should be available at http://localhost:8000

You can always use the following command to stop execution:
```bash
docker-compose -f /home/simon/Dev/boards/docker-compose.dev.yml down
```

### Tests
Use this command to run tests:
```bash
docker-compose -f docker-compose.dev.yml run backend sh -c "python manage.py test"
```
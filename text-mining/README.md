![](https://img.shields.io/travis/anthonymonori/text-mining.svg?style=flat-square)
![](https://img.shields.io/github/issues/anthonymonori/text-mining.svg?style=flat-square)
![](https://img.shields.io/github/forks/anthonymonori/text-mining.svg?style=flat-square)
![](https://img.shields.io/github/stars/anthonymonori/text-mining.svg?style=square)
![](https://img.shields.io/badge/license-BSD-blue.svg?style=square)
![](https://img.shields.io/twitter/url/https/github.com/anthonymonori/text-mining.svg?style=social)

# text-mining
A simple tool for text-mining tweets using the official Twitter Streaming API and written in Python for Big Data analysis. Read more about the API [here](https://dev.twitter.com/streaming/overview).

## Requirements
- Python 2.7.6
- [Tweepy](https://github.com/tweepy/tweepy)
- [PyMongo 3.0.3+](https://api.mongodb.org/python/current/)
- [mongoDB 3.0.5](https://www.mongodb.org/downloads)
- Your very own Twitter app - register one [here](https://apps.twitter.com)

_Note: please follow the installation instruction found on the official Tweepy repo before continuing. Also make sure you have all the required software installed and set up before proceeding._

## Installation
- ``` git clone https://github.com/anthonymonori/text-mining.git ./text-mining ```
- ``` cd ./text-mining ```
- ``` sudo pip install requirements.txt ```
- ``` open _conf.ini ```
- ``` mv _conf.ini conf.ini ```

## Usage
``` python text-mining.py hashtag1 hashtag2 ... ```

_Note: Currently saves the tweets into a collection called tweets in a mongodb database called test._

## Use cases
- Data mining of tweets for Big Data analysis
- Dumping data into a database a.k.a. collecting
- Parse the stream into a live-feed of tweets
- Any other ideas? Let me know

## Todo
- [x] Add mongoDB integration using PyMongo driver
- [ ] Add database settings into the global conf file
- [ ] Change database and collection naming
- [ ] Put the project on Travis CI
- [ ] Better wrapper; possibly extend it to a command-line tool

## License
Copyright (c) 2015, Antal János Monori
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

* Redistributions of source code must retain the above copyright notice, this
  list of conditions and the following disclaimer.

* Redistributions in binary form must reproduce the above copyright notice,
  this list of conditions and the following disclaimer in the documentation
  and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

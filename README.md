# ProjectX Music

A Music Recommendation System made using Flutter and backed by FastAPI.

## Introduction

ProjectX Music is an online mobile application that acts similarly to its alternatives, like Spotify, LastFM, etc. It
consists of mobile application ( both for Android and iOS ) backed by an online hosted server written entirely using
Python3.

It solely uses the vast musical library of LastFM as its music catalog, so you may find the same catalog of music as in
the LastFM app itself. We are thankful to LastFM as it provides us with an efficient technique to access their music
library, which contains a lot of useful data necessary for our use case. It is to be noted that, no user data is sent
back to LastFM from ProjectX Music, for any audio scrobbling activity.

## Requirements

- Python ( check version info from `runtime.txt` )

## How to deploy the Backend

1. To install all the necessary **python** libraries:
   
   ```commandline
   python3 -m pip install -r requirements.txt
   ```
   
2. Not run the `startServer.py` file stored in the root of the project.
   
   ```commandline
   python3 startServer.py
   ```

## Who are we ?

We are a group of students interested to explore different technologies extending from Machine Learning to Mobile
Applications, and more.

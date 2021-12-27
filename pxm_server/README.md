# PXM Server Library

## Introduction

This libray contains the implementations of the server classes for all Operating System.

It automatically detects the type of operating system available and its specs, and then configures the suitable server
implementation with suitable parameters.

### List of Operating Systems and Its General Specs [may change]:

- Unix Based OS
    - **Gunicorn** (with Uvicorn Workers)
    - No. of Workers: approx. _2*N+1_ where _N_ is the number of physical core available.
- Non-Unix Based OS
    - Purely **Uvicorn**
    - No. of Workers: 1

## Depends On

- It may not have any **non-third-party** dependency
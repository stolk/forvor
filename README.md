# forvor

Fortune's Voronoi generator

![Voronoi diagram of 2,3-Halton](images/testrun.png "Voronoi diagram of 2,3-Halton")

## Introduction

This is a copy of the Public Domain [Voronoi](http://en.wikipedia.org/wiki/Voronoi_diagram) code by [Steven Fortune](http://ect.bell-labs.com/who/sjf/).
The algorithm is known as [Fortune's algorithm](http://en.wikipedia.org/wiki/Fortune%27s_algorithm).

This repository started as a direct copy of the original C source code.
It containst the following improvements:
* Fixes for the memory leaks.
* Python tool that parses the voronoi diagram output, clips edges, and generates polygon. Outputs as SVG.

## To do
* Port the edge-clipping and polygon-generation from Python to C code.

## License

The original source code by Fortune is in the Public Domain.
So this version will also be in the public domain.

## Authors

Original source code by [Steven Fortune](http://ect.bell-labs.com/who/sjf/).
Enhancements by [Bram Stolk](http://stolk.org).


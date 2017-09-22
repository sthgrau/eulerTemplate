Someone suggested to me that I should do the Euler Project problems from https://projecteuler.net/ in order to keep my python knowledge fresh.

I wanted to make aprogram to grab the problem descriptions and create files with the problem description as a comment. Right now, I have only done python, but other languages shouldn't be a problem.

To use:

* clone this repository
* create solutions/python subdirectory
* run the get_problems.py script

NOTE: I changed the location of the solutions to allow users to create git repositories of all of their solutions

I added make functionality to be able to run the tests. Right now, only made for python, but can be adapter for other languages.
Just run "make python" in the 'solutions' directory. Any scripts modified after the last report will be run and its result and performance stats gathered together in json format.

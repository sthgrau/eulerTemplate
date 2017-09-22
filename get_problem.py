#!/usr/bin/env python
from HTMLParser import HTMLParser
import urllib2
import sys
import re
import os
import time
from os import listdir
from os import path

class myParser(HTMLParser):
  inProblem=False
  problemDepth=0
  problemData=""
  def handle_data(self, data):
    if self.inProblem:
      self.problemData += data
  def handle_endtag(self, tag):
    if tag == "div":
      if self.inProblem:
        self.problemDepth -= 1
      if self.problemDepth == 0:
        self.inProblem=False
  def handle_startendtag(self, tag,attrs):
    if tag == "br" and self.inProblem:
      self.problemData += " \n"
  def handle_starttag(self, tag, attrs):
    stuff = "<%s " % (tag)
    for myattr,myval in attrs:
      stuff += "%s='%s' " % (myattr,myval)
    stuff += ">"
    if tag == "div":
      if self.inProblem:
        self.problemDepth += 1
      for myattr,myval in attrs:
        if myattr == "class" and myval == "problem_content":
          self.inProblem=True
          self.problemDepth += 1
    if tag == "span" and self.inProblem:
      self.problemData += stuff
    if tag == "sup" and self.inProblem:
      self.problemData += "**"
    if tag == "br" and self.inProblem:
      self.problemData += "\n"
    if tag == "a" and self.inProblem:
      self.problemData += stuff.replace("href='","href='https://projecteuler.net/")
    if tag == "img" and self.inProblem:
      self.problemData += stuff.replace("src='","src='https://projecteuler.net/")
        

URLTEMPLATE="https://projecteuler.net/problem="
DEBUG0=False
PROBLEMDIR="../problem_descriptions"
SOLUTIONDIR="solutions"

def getProblemDescription(problemId):
    try:
        if not path.isfile("%s/%s.txt" % (PROBLEMDIR,problemId)):
            f = urllib2.urlopen("%s%s" % (URLTEMPLATE,problemId))
        
            fs = f.read()
            f.close()
            p = myParser()
            p.feed(fs)
            myresult = p.problemData 
            myfile = open("%s/%s.txt" % (PROBLEMDIR,problemId),"w")
            myfile.write(myresult)
            myfile.close()
            return True
    except:
        e = sys.exc_info()[0]
        if DEBUG0: print "error = %s" % (e)
        return False

def getProblems(max=700):
    ps = sorted([int(re.search("([0-9]*).txt",x).group(1)) for x in listdir(PROBLEMDIR)])
    if len(ps) > 0:
        last=ps[-1]
    else:
        last=0
    next=last + 1
    while ( next < max ) and getProblemDescription(next):
        time.sleep(2)
        next=next + 1
    problemId=1
    if path.isdir("python"):
        while path.isfile("%s/%s.txt" % (PROBLEMDIR,problemId)):
            dst="python/%s.py" % (problemId)
            src="%s/%s.txt" % (PROBLEMDIR,problemId)
            if not path.isfile(dst):
                y = open(src,"r")
                ys = y.read()
                y.close()
                x = open(dst, "w")
                x.write("""#!/usr/bin/env python
# -*- coding: UTF-8 -*-
\"\"\"
%s
\"\"\"

import sys
if __name__ == '__main__':
    sys.exit(0)
""" %(ys))

                x.close()
            problemId+=1


if __name__ == '__main__':
    os.chdir(SOLUTIONDIR)
    if len(sys.argv) > 1:
        max=int(sys.argv[1])
    else:
        max=20
    getProblems(max)
    sys.exit(0)

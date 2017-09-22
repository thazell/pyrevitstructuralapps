"""


Copyright (c) 2014-2017 Timon Hazell

You can redistribute this file and/or modify
it under the terms of the GNU General Public License version 3, as published by
the Free Software Foundation.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

"""
import os
import csv
from subprocess import Popen

from scriptutils.userinput import SelectFromList
from scriptutils import logger, this_script

import clr
import glob, os

packagesused = []

def checkFunction (filename):
    searchterm = "Dynamo.Nodes.Function"
    key1 = "nickname"
    #print filename
    #lineno = 0
    for line in open(filename):
        # try:
            #lineno +=1
            if searchterm in line:
                #print "found a function" + line
                parts = line.split("\" ")
                # print lineno
                for part in parts:
                    if key1 in part:
                        #print part
                        part = part.replace('"', '')
                        subparts = part.split("=")
                        packageandfile = [subparts[1], filename]
                        #print packageandfile
                        #if not packageandfile in packagesused:
                        packagesused.append(packageandfile)

def checkAssembly (filename):
    searchterm = "assembly"
    print filename
    #lineno = 0
    for line in open(filename):
        # try:
            #lineno +=1
            if searchterm in line:
                parts = line.split(" ")
                # print lineno
                for part in parts:
                    if searchterm in part:
                        part = part.replace('"', '')
                        subparts = part.split("=")
                        packageandfile = [subparts[1], filename]
                        print packageandfile
                        packagesused.append(packageandfile)
                            
#specify path of directory to search
path = "N:\\Revit\\Revit Development\\Dynamo\\Scripts\\"
#path = "C:\\Users\\hazell\\Dropbox\\Speaking\\BILT\\_RTCNA2016_23\\boston\\"
#path = "C:\\Users\\hazell\\Dropbox\\Speaking\\"
for root, dirs, files in os.walk(path):
    for name in files:
        if name.endswith(".dyn"):
            relDir = os.path.relpath(root, "N:\\")
            relDir = os.path.join("N:\\", relDir)
            os.chdir(relDir)
            relFile = os.path.join(relDir, name)
            #print "checking file"
            #print relFile
            checkFunction(name)
            checkAssembly(name)
            #print "done checking file"

#export to csv
    
file_path = "c:\Temp\CustomNodesList.csv"
directory = os.path.dirname(file_path)
print packagesused

try:
    os.stat(directory)
except:
    os.mkdir(directory)  
with open(file_path, 'wb') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
    fieldnames = ['Package', 'FileName']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for item in packagesused:
        writer.writerow({'Package': item[0], 'FileName': item[1]})
p = Popen(file_path, shell=True)
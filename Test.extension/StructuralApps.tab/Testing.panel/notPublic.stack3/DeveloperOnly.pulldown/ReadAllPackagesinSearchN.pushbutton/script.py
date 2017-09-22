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

import clr
import glob, os

packagesused = []

# try to find all pacakages

dyfs = []

path = "N:\\Revit\\Revit Development\\Dynamo\\Nodes\\"
driveletter = path[0:3]
for root, dirs, files in os.walk(path):
    for name in files:
        if name.endswith(".dyf"):
            relDir = os.path.relpath(root, driveletter)
            relDir = os.path.join(driveletter, relDir)
            os.chdir(relDir)
            relFile = os.path.join(relDir, name)
            folder = relDir.replace("\\dyf", "")
            folder = folder[folder.rindex("\\")+1:]

            dyfs.append([name,relDir, folder])
            #print name + "   " + relDir
file_path = "c:\\Temp\\pacakges.csv"
directory = os.path.dirname(file_path)

try:
    os.stat(directory)
except:
    os.mkdir(directory)  
with open(file_path, 'wb') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
    fieldnames = ['Custom Node', 'Location', 'Package']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for item in dyfs:
        writer.writerow({'Custom Node': item[0], 'Location': item[1], 'Package': item[2]})
p = Popen(file_path, shell=True)
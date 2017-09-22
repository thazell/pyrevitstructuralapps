"""
Copyright Silman 2017
Heavily influenced by work from 

Copyright (c) 2014-2016 Gui Talarico @ WeWork
github.com/gtalarico

pyRevit is a free set of scripts for Autodesk Revit: you can redistribute it and/or modify
it under the terms of the GNU General Public License version 3, as published by
the Free Software Foundation.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

See this link for a copy of the GNU General Public License protecting this package.
https://github.com/eirannejad/pyRevit/blob/master/LICENSE
"""

__doc__ = 'Generate an Email with the Sheet List Included'
import os
import sys
import subprocess
import time

import rpw
from rpw import doc, uidoc, DB, UI

import sys
from Autodesk.Revit.UI import *
from Autodesk.Revit.DB import *
from System.Collections.Generic import List

from scriptutils.userinput import SelectFromList
from scriptutils import logger, this_script

uidoc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document


EXCELPATHS_FILENAME = 'OpenInExcel_UserPaths.txt'
EXCELPATHS_FILEPATH = os.path.join(os.path.dirname(__file__), EXCELPATHS_FILENAME)
# Export Settings
temp_folder = os.path.expandvars('%temp%\\')
export_options = DB.ViewScheduleExportOptions()

# Get Saved Excelp Paths
if not os.path.exists(EXCELPATHS_FILEPATH):
    UI.TaskDialog.Show('OpenInExcel', 'Could not find the File: \n'
                       '{} in:\n {}'.format(
                       EXCELPATHS_FILENAME, os.path.dirname(__file__)))
    sys.exit()

with open(EXCELPATHS_FILEPATH) as fp:
    excel_paths = fp.read().split('\n')

for excel_path in excel_paths:
    if os.path.exists(excel_path):
        break
else:
    UI.TaskDialog.Show('OpenInExcel', 'Could not find Excel Path \n'
                       'Please add your Excel path to OpenInExcel_UserPaths.txt'
                       'and try again.')
    os.system('start notepad \"{path}\"'.format(path=saved_paths))
    sys.exit()



def getNames(z_element):
	z_elementname = []
	for e in z_element:
		z_elementname.append(e.SheetNumber + " - " + e.Name)
	return z_elementname

cl_sheets = FilteredElementCollector(doc)
allsheets = cl_sheets.OfCategory(BuiltInCategory.OST_Sheets).WhereElementIsNotElementType().ToElements()

sheetsexport = []
ids = []
#get visually pretty names for lookup
options = sorted(getNames(allsheets))

if options:
    sheetsexportpretty = SelectFromList.show(options, "Select Relevant Sheets:")
    logger.debug('Selected sheets are: {}'.format(sheetsexportpretty))
else:
    TaskDialog.Show('pyRevit', 'You must select one item')
    sys.exit()

#find the ones you wanted from the list above
for sheet in allsheets:
    for sheetprettyprint in sheetsexportpretty:
        if getNames([sheet])[0] in sheetprettyprint:
            sheetsexport.append([sheet.SheetNumber, sheet.Name])
            sheetsexport = sorted(sheetsexport, key=lambda tup: tup[0])
if not os.path.exists("c:\\temp\\"):
    os.mkdir("c:\\temp\\")

try:
    import csv
    fullfilepath = "c:\\temp\\SheetList.csv"
    with open(fullfilepath, 'wb') as f:
        writer = csv.writer(f)
        print sheetsexport
        for i in sheetsexport:
            print i
            writer.writerow(i)
        
        #writer.writerow(sheetsexport)
        os.system('start excel \"{path}\"'.format(path=fullfilepath))
        
except Exception as e:
    print('Sorry, something failed:')
    print(e)

__window__.Close()


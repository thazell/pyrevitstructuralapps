"""
Copyright Silman 2017
Heavily based on work by Gui Talarico and Ehsan Irannejad with Pyrevit.

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


__context__ = 'zerodoc'
__doc__ = 'Exports All Text Elements to Excel'
import os

import csv
from subprocess import Popen

import sys
from Autodesk.Revit.UI import *
from System.Collections.Generic import List

doclocations = []
#list of document locations
doclocations.append("C:\\Temp\\WILS-S.rvt")
doclocations.append("C:\\Temp\\WILS-S - Copy (2).rvt")
doclocations.append("C:\\Temp\\WILS-S - Copy (3).rvt")
doclocations.append("C:\\Temp\\WILS-S - Copy.rvt")

#random testing file should be open before starting (although eventually this should just read the active model so it's more flexible
placeholderFile = "C:\\Temp\\openandclosescripttest\\placeholder.rvt"
docprevious = __revit__.ActiveUIDocument.Document
file = docprevious.PathName
i = 0
for doclocation in doclocations:
    i = i+1
    docnext = __revit__.OpenAndActivateDocument(doclocation)
    docprevious.Close(False)
    docprevious = __revit__.ActiveUIDocument.Document
    #uidoc = __revit__.OpenAndActivateDocument(file)
    #docprevious.Document.Close(False)
    uidoc = __revit__.ActiveUIDocument
    doc = __revit__.ActiveUIDocument.Document

    import clr
    clr.AddReference('RevitAPI') 
    clr.AddReference('RevitAPIUI') 
    from Autodesk.Revit.DB import * 

    dialog = TaskDialog("Decision");
    dialog.MainContent = "Export all text elements from the model?";
    dialog.CommonButtons = TaskDialogCommonButtons.Yes | TaskDialogCommonButtons.No;


    result = TaskDialog.Show(dialog)

    if result == TaskDialogResult.Yes:
        textnotes = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_TextNotes).WhereElementIsNotElementType().ToElementIds()
    else:
        curview = uidoc.ActiveGraphicalView
        textnotes = FilteredElementCollector(doc, curview.Id).OfCategory(BuiltInCategory.OST_TextNotes).WhereElementIsNotElementType().ToElementIds()

    file_path = "c:\Temp\export" + str(i) + ".csv"
    directory = os.path.dirname(file_path)

    try:
        os.stat(directory)
    except:
        os.mkdir(directory)  
        
    with open(file_path, 'wb') as csvfile:
            spamwriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            fieldnames = ['TextNoteID', 'View', 'Text']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for t in textnotes:
                try:    
                    writer.writerow({'TextNoteID': t.ToString(), 'Text': doc.GetElement(t).Text, 'View':doc.GetElement(doc.GetElement(t).OwnerViewId).Name  })
                except:
                    writer.writerow({'TextNoteID': t.ToString(), 'Text': "---Text did not export: the text note contains unsupported characters---", 'View':doc.GetElement(doc.GetElement(t).OwnerViewId).Name  })
                    pass
    p = Popen(file_path, shell=True)

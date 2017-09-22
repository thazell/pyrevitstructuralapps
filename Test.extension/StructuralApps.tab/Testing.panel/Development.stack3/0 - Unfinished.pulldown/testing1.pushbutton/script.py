"""
Copyright Silman 2017

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

__doc__ = 'Exports All Text Elements to Excel'
import os
import csv
from subprocess import Popen
import sys
from Autodesk.Revit.UI import *
from System.Collections.Generic import List
doclocations = []
doclocations.append("C:\\Temp\\WILS-S.rvt")
doclocations.append("C:\\Temp\\WILS-S - Copy (2).rvt")
doclocations.append("C:\\Temp\\WILS-S - Copy (3).rvt")
doclocations.append("C:\\Temp\\WILS-S - Copy.rvt")

print "ok"
"""
def ProcessWindow(hwnd):
    ID_OK = 1
    IntPtr hwndOk = Win32.Functions.GetDlgItem(hwnd, ID_OK)
    if (hwndOk != IntPtr.Zero):
        Win32.Functions.SendMessage(hwndOk, (uint)Win32.Messages.WM_LBUTTONDOWN, (int)Win32.KeyStates.MK_LBUTTON, 0)
        Win32.Functions.SendMessage(hwndOk, (uint)Win32.Messages.WM_LBUTTONUP, (int)Win32.KeyStates.MK_LBUTTON, 0)
#warning hook start
Process process = Process.GetCurrentProcess()

IntPtr hwnd = process.MainWindowHandle

App._windowsInterceptor = new WindowInterceptor(hwnd, ProcessWindow )


print "test"
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

#warning hook close
App._windowsInterceptor.Stop()
"""

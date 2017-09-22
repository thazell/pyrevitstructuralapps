"""
Copyright (c) 2014-2017 Timon Hazell
Python scripts for Autodesk Revit
TESTED API: 2015 | 2016

pyRevit is a free set of scripts for Autodesk Revit: you can redistribute it and/or modify
it under the terms of the GNU General Public License version 3, as published by
the Free Software Foundation.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
"""

from Autodesk.Revit.UI import TaskDialog

from scriptutils.userinput import SelectFromList
from scriptutils import logger, this_script
import sys
import clr

clr.AddReference("RevitServices")
import RevitServices
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager

from System.Collections.Generic import *

clr.AddReference("RevitAPI")
import Autodesk
from Autodesk.Revit.DB import *

doc = DocumentManager.Instance.CurrentDBDocument
uiapp = DocumentManager.Instance.CurrentUIApplication

doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument

views = []

#TaskDialog.Show("Original View",baseview.Name)

collector = FilteredElementCollector(doc)
allviews = collector.OfClass(View).ToElements()

# only check sheeted views

draftingtemplatelist = []
draftingviewlist = []
sectiontemplatelist = []
sectionviewlist = []
for view in allviews:
    if (view.IsTemplate):
        if view.ViewType == ViewType.Detail:
            sectiontemplatelist.append(view)
        elif view.ViewType == ViewType.Section:
            sectiontemplatelist.append(view)
        elif view.ViewType == ViewType.DraftingView:
            draftingtemplatelist.append(view)
        else:
            continue
    elif view.ViewType == ViewType.Detail:
        sectionviewlist.append(view)
    elif view.ViewType == ViewType.Section:
        sectionviewlist.append(view)
    elif view.ViewType == ViewType.DraftingView:
        draftingviewlist.append(view)
    else:
        continue
#filter out elevation template which is a section in silman's tempalte:
sectiontemplatelist = filter(lambda x: ("Elevation" not in x.Name),sectiontemplatelist)

        
#sort the templates just in case a user makes a custom template... the defaults will be assigned.
sectiontemplatelist.sort(key=lambda x: ("Elevation" not in x.Name and x.Id.IntegerValue))
draftingtemplatelist.sort(key=lambda x: x.Id.IntegerValue)

ids = []

#only look at views that are on a sheet and do not have a template assigned.  I had to add a check for elevation in the string name because our elevation view template was based on a section
sheetedsectionviews = filter(lambda x: (x.ViewTemplateId == ElementId.InvalidElementId and x.get_Parameter(BuiltInParameter.VIEWPORT_SHEET_NUMBER).HasValue),allviews)
sheeteddraftingviews = filter(lambda x: (x.ViewTemplateId == ElementId.InvalidElementId and x.get_Parameter(BuiltInParameter.VIEWPORT_SHEET_NUMBER).HasValue),allviews)

trans = Transaction(doc,"Assign View Templates by Scale")

trans.Start();

print "Drafting Views Modified:"
i = 0
for v in sheeteddraftingviews:
    param = v.get_Parameter(BuiltInParameter.VIEW_SCALE)
    vscale = Autodesk.Revit.Elements.InternalUtilities.ElementUtils.GetParameterValue(param)
    for t in draftingtemplatelist:
        #chck to see if the view scale = the tempalte scale:
        # print t.Name
        # print Revit.Elements.InternalUtilities.ElementUtils.GetParameterValue(t.get_Parameter(BuiltInParameter.VIEW_SCALE))
        # print v.Name
        # print vscale
        if Revit.Elements.InternalUtilities.ElementUtils.GetParameterValue(t.get_Parameter(BuiltInParameter.VIEW_SCALE)) == vscale:
            print v.Name + " at 1:" + str(vscale) + ".\n\tAssigned Template: " + t.Name
            # print t.Name
            # print Revit.Elements.InternalUtilities.ElementUtils.GetParameterValue(t.get_Parameter(BuiltInParameter.VIEW_SCALE))
            # print v.Name
            # print vscale
            # print v.ViewTemplateId.IntegerValue
            v.ViewTemplateId = t.Id
            # print v.ViewTemplateId.IntegerValue
            i +=1
            break
            
    else:
      # will be called if the previous loop did not end with a `break` 
        continue
if i == 0: print "None"
if i !=0: print "Total Drafting Views Modified: " +  str(i)
print "\n\n\nReal Sections/Details Modified:"
ii = 0
for v in sheetedsectionviews:
    param = v.get_Parameter(BuiltInParameter.VIEW_SCALE)
    vscale = Revit.Elements.InternalUtilities.ElementUtils.GetParameterValue(param)
    for t in sectiontemplatelist:
        #chck to see if the view scale = the tempalte scale:
        # print t.Name
        # print Revit.Elements.InternalUtilities.ElementUtils.GetParameterValue(t.get_Parameter(BuiltInParameter.VIEW_SCALE))
        # print v.Name
        # print vscale
        if Revit.Elements.InternalUtilities.ElementUtils.GetParameterValue(t.get_Parameter(BuiltInParameter.VIEW_SCALE)) == vscale:
            print v.Name + " at 1:" + str(vscale) + ".\n\tAssigned Template: " + t.Name
            # print Revit.Elements.InternalUtilities.ElementUtils.GetParameterValue(t.get_Parameter(BuiltInParameter.VIEW_SCALE))
            # print v.Name
            # print vscale
            # print v.ViewTemplateId.IntegerValue
            # v.ViewTemplateId = t.Id
            # print v.ViewTemplateId.IntegerValue
            ii += 1
            break
            
    else:
      # will be called if the previous loop did not end with a `break` 
      continue
if ii == 0: print "None"
if ii !=0: print "Total Details/Sections Modified: " + str(i)

if i == ii == 0:
    __window__.Close()
    trans.RollBack()
    TaskDialog.Show("You are amazing!  None of the Drafting Views or Sections on sheets were missing templates. You should celebrate.")
    sys.exit() 
# Get the application and document from external command data.
# app = commandData.Application.Application;
# activeDoc = commandData.Application.ActiveUIDocument.Document;

# Creates a Revit task dialog to communicate information to the user.
mainDialog = TaskDialog("SilmanApps")
mainDialog.MainInstruction = "I recommend reviewing the results before keeping them."
mainDialog.MainContent = "Click on the Revit icon on the taskbar and switch windows to view."

# Add commmandLink options to task dialog
mainDialog.AddCommandLink(Autodesk.Revit.UI.TaskDialogCommandLinkId.CommandLink1,"Undo changes?")
mainDialog.AddCommandLink(Autodesk.Revit.UI.TaskDialogCommandLinkId.CommandLink2,"Keep Changes")

# Set footer text. Footer text is usually used to link to the help document.
mainDialog.FooterText = " "

tResult = mainDialog.Show()


# If the user clicks the second command link, a simple Task Dialog 
# created by static method shows information about the active document
if Autodesk.Revit.UI.TaskDialogResult.CommandLink2 == tResult:
    trans.Commit()
else:
    trans.RollBack()
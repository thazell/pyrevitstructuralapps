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

__doc__ = 'Searches Project for Overriden Dimensions'
import os

import sys
from Autodesk.Revit.UI import *
from System.Collections.Generic import List
from Autodesk.Revit.DB import Transaction, Dimension

from scriptutils.userinput import SelectFromList
from scriptutils import logger, this_script

uidoc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document


import clr
clr.AddReference('RevitAPI') 
clr.AddReference('RevitAPIUI') 
from Autodesk.Revit.DB import * 

from urllib import quote
import webbrowser

z_alloverrides = []

def getValues(z_element):
    alloverrides = []
    alloverrideelements = []
    for e in z_element:
        if len(list(e.Segments)) > 0:
            for seg in e.Segments:
                # if seg.Below != "" or seg.Above != "" or seg.Prefix != '' or seg.Suffix != '' or seg.ValueOverride != '' or seg.Below != '' seg.ValueOverride !=  '':
                if not any(x is None for x in [seg.ValueOverride, seg.Below, seg.Above, seg.Prefix, seg.Suffix]):
                    curoverride = (seg.Above + seg.Prefix + seg.ValueOverride + seg.Suffix  + seg.Below)
                    if len(curoverride) > 0:
                        if curoverride not in alloverrides:
                            alloverrides.append(curoverride)
                            alloverrideelements.append(seg)
        # else:
            # #make the element the only segment value
            # seg = e
            # if seg.Below != "" or seg.Above != "" or seg.Prefix != '' or seg.Suffix = '' or seg.ValueOverride != '' or seg.Below != '' seg.ValueOverride !=  '':
                # seg.Below = ''
                # seg.Above = ''
                # seg.Prefix = ''
                # seg.Suffix = ''
                # seg.ValueOverride = ''
                # seg.Below = 'LAP SPLICE'
                # seg.ValueOverride =  'CLASS B TENSION'
        # z_elementname.append(e.SheetNumber + " - " + e.Name)
    
    # returnlist = [alloverrides, z_element]
    #Filter out blank ones:
    alloverrides = filter(None, alloverrides) # fastest
    # print returnlist
    # returnlist = [x for x in returnlist if not x[0] is None]
    # print (len(x) for x in returnlist)
    # Filter for unique items:
    # filteredresults = set(alloverrides)
    # filteredresults = list(filteredresults)
    return [alloverrides, alloverrideelements]

cl_dims = FilteredElementCollector(doc)
alldims = cl_dims.OfCategory(BuiltInCategory.OST_Dimensions).WhereElementIsNotElementType().ToElements()

selectedoverride = []
ids = []
getValueResults = getValues(alldims)
options = sorted(getValueResults[0])
referenceelements = getValueResults[1]

if options:
    selectedoverride = SelectFromList.show(options, "Select Override to Apply:")
    if len(selectedoverride) == 1:
        #paste selected overrides
        print getValueResults[1]
        print selectedoverride
        #get full overrides for dimension that was selected:
        referenceelement = referenceelements[getValueResults[0].index(selectedoverride[0])]
        
else:
    TaskDialog.Show('pyRevit', 'You must select one override only')
    sys.exit()
    

print referenceelement.Below + referenceelement.Above + referenceelement.Prefix +  referenceelement.Suffix + referenceelement.ValueOverride
    
    
t = Transaction(doc, 'Dimension "Class B Lap Splice"')
t.Start()

for elId in uidoc.Selection.GetElementIds():
    el = doc.GetElement(elId)
    if isinstance(el, Dimension):
        if len(list(el.Segments)) > 0:
            for seg in el.Segments:
                seg.Below = referenceelement.Below
                seg.Above = referenceelement.Above
                seg.Prefix = referenceelement.Prefix
                seg.Suffix = referenceelement.Suffix
                seg.ValueOverride = referenceelement.ValueOverride
        else:
            #make the element the only segment value
            seg = el
            seg.Below = referenceelement.Below
            seg.Above = referenceelement.Above
            seg.Prefix = referenceelement.Prefix
            seg.Suffix = referenceelement.Suffix
            seg.ValueOverride = referenceelement.ValueOverride

t.Commit()

__window__.Close()
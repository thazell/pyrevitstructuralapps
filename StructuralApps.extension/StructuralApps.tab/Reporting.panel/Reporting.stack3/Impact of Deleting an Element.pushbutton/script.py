"""
MODIFIED BY SILMAN
Copyright (c) 2014-2016 Ehsan Iran-Nejad
Python scripts for Autodesk Revit

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

__doc__ = 'This tool will help you identify the impact of deleting an element (specifically useful when deleting levels.)'
import sys
from Autodesk.Revit.DB import Transaction, Dimension, ElementId
from Autodesk.Revit.UI import TaskDialog
from System.Collections.Generic import List
from collections import Counter

uidoc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document
selectedElement = uidoc.Selection.GetElementIds()
countreal = 0
el = []
deleteids = []
delcategories = []
delel = []
try:
    
    if len(selectedElement) == 1:
        t = Transaction(doc, 'Fake')
        t.Start()
        for s in selectedElement:
            el = doc.GetElement(s)
            deleteids = doc.Delete(s)
        t.RollBack()
        
        for id in deleteids:
            # TaskDialog.Show("type(id)",id.ToString())
            delel = doc.GetElement(id)
        for i in deleteids:
            delel = doc.GetElement(i)
            if not delel is None:
                #TaskDialog.Show("type(id)",id.ToString())
                countreal = countreal + 1 
                if not delel.Category is None:
                    delcategories.append(delel.Category.Name)
                    # TaskDialog.Show("Element that will be deleted",delel.Category.Name)
        c = Counter(delcategories)
        delcategoriesstring = ''
        for q, a in zip(list(c),c.values()):
            spaces = ' ' * 2 * (4-len(str(a)))
            delcategoriesstring+=('{1} {2}{0}'.format (q,a,spaces)) + "\n"
        #TaskDialog.Show("Element that will be deleted",c)
        s = Transaction(doc, 'Select Elements')
        s.Start()
        if countreal == 1:
            TaskDialog.Show("Deleted Elements", "If you delete this " + el.Category.Name  + ", no other elements will be deleted.")
        else:
            TaskDialog.Show("Deleted Elements", "If you delete this " + el.Category.Name  + ", " + str(countreal) + " elements will be deleted. They have been selected. \n\n" + delcategoriesstring + "\n(This selection may include non-physical elements.)")
            # elements_to_hide = collector.WhereElementIsNotElementType().Excluding(element_collection).ToElements()
        uidoc.Selection.SetElementIds(deleteids)
        
        s.Commit()
    elif len(selectedElement) > 1:
        TaskDialog.Show ("Invalid Selection", "Only one element can be selected. Please select the element you want to delete before running the impact test.")
    else:
        TaskDialog.Show ("Invalid Selection", "No elements were selected. Select an element first then run the command.")


        

except OSError as err:
    print("OS error: {0}".format(err))
except ValueError:
    print("Could not convert data to an integer.")
except:
    print("Unexpected error:", sys.exc_info()[0])
    raise
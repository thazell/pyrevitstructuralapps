#original code from dp-stuff
# see: http://dp-stuff.org/find-and-delete-empty-tags-with-revit-python-shell/

#adapted and copyright by Timon Hazell
#developed and adapted for Silman


import clr
import math
clr.AddReference('RevitAPI')
clr.AddReference('RevitAPIUI')
from Autodesk.Revit.DB import *
from Autodesk.Revit.UI import *
 
clr.AddReference("System")
from System.Collections.Generic import List
 
app = __revit__.Application
doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument
activeView = doc.ActiveView
#this script looks at tags only in the active view
collector1 = FilteredElementCollector(doc,activeView.Id)
#If you want to run it on the whole document - comment the line above and uncomment the line below
#collector1 = FilteredElementCollector(doc)
collector1.WhereElementIsNotElementType().OfClass(clr.GetClrType(IndependentTag))
elSet1 = collector1.ToElements()
print len(elSet1)
 
actDelete = True
elSet1 = uidoc.Selection.GetElementIds()
for elid in elSet1:
    el = doc.GetElement(elid)
    print el.ToString()
    print el.TagText
print len(elSet1)
knSet = list()
for el in elSet1:
    if el.IsValidObject:
        if not el.IsHidden:
            if el.TagText:
                if el.TagText=='20k':
                    knSet.append(el)
                    print el.TagText  + '   <-- Should be 20k'
    else:
        print "invalid"
        el.ToString()
ct = len(knSet)
print 'Tags Found: ' +str(ct)
 
"""
if actDelete:
	t = Transaction(doc, 'Tag Deleted')
 
	t.Start()
	for el in knSet:
		doc.Delete(el)
 
	t.Commit()
print str(ct) + ' empty tags removed'

uidoc.Selection.SetElementIds(List[ElementId](knSet))
"""
"""
MODIFIED BY SILMAN
Copyright (c) 2014-2016 Ehsan Iran-Nejad
Python scripts for Autodesk Revit

This file is part of pyRevit repository at https://github.com/eirannejad/pyRevit

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

__doc__ = 'Adds "TYP." to the suffix of selected dimensions.'

__window__.Close()
from Autodesk.Revit.DB import Transaction, Dimension

uidoc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document

t = Transaction(doc, 'Dimension TYP suffix')
t.Start()

for elId in uidoc.Selection.GetElementIds():
    el = doc.GetElement(elId)
    if isinstance(el, Dimension):
        if len(list(el.Segments)) > 0:
            for seg in el.Segments:
                if not seg.Suffix is None:
                    seg.Suffix += 'TYP.'
                else:
                    seg.Suffix = 'TYP.'
        else:
            seg = el
            if not seg.Suffix is None:
                seg.Suffix += 'TYP.'
            else:
                seg.Suffix = 'TYP.'
t.Commit()

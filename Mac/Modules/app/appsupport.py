# This script generates a Python interface for an Apple Macintosh Manager.
# It uses the "bgen" package to generate C code.
# The function specifications are generated by scanning the mamager's header file,
# using the "scantools" package (customized for this particular manager).

import string

# Declarations that change for each manager
MACHEADERFILE = 'Appearance.h'		# The Apple header file
MODNAME = '_App'				# The name of the module
OBJECTNAME = 'ThemeDrawingState'			# The basic name of the objects used here
KIND = ''				# Usually 'Ptr' or 'Handle'

# The following is *usually* unchanged but may still require tuning
MODPREFIX = 'App'			# The prefix for module-wide routines
OBJECTTYPE = OBJECTNAME + KIND		# The C type used to represent them
OBJECTPREFIX = OBJECTNAME + 'Obj'	# The prefix for object methods
INPUTFILE = string.lower(MODPREFIX) + 'gen.py' # The file generated by the scanner
OUTPUTFILE = MODNAME + "module.c"	# The file generated by this program

from macsupport import *

# Create the type objects
#MenuRef = OpaqueByValueType("MenuRef", "MenuObj")


#WindowPeek = OpaqueByValueType("WindowPeek", OBJECTPREFIX)

RgnHandle = FakeType("(RgnHandle)0")
NULL = FakeType("NULL")

# XXXX Should be next, but this will break a lot of code...
# RgnHandle = OpaqueByValueType("RgnHandle", "OptResObj")

#KeyMap = ArrayOutputBufferType("KeyMap")
#MacOSEventKind = Type("MacOSEventKind", "h") # Old-style
#MacOSEventMask = Type("MacOSEventMask", "h") # Old-style
#EventMask = Type("EventMask", "h")
#EventKind = Type("EventKind", "h")
ThemeBrush = Type("ThemeBrush", "h")
ThemeColor = Type("ThemeColor", "h")
ThemeTextColor = Type("ThemeTextColor", "h")
ThemeMenuBarState = Type("ThemeMenuBarState", "H")
ThemeMenuState = Type("ThemeMenuState", "H")
ThemeMenuType = Type("ThemeMenuType", "H")
ThemeMenuItemType = Type("ThemeMenuItemType", "H")
ThemeFontID = Type("ThemeFontID", "H")
ThemeTabStyle = Type("ThemeTabStyle", "H")
ThemeTabDirection = Type("ThemeTabDirection", "H")
ThemeDrawState = Type("ThemeDrawState", "l")
ThemeCursor = Type("ThemeCursor", "l")
ThemeCheckBoxStyle = Type("ThemeCheckBoxStyle", "H")
ThemeScrollBarArrowStyle = Type("ThemeScrollBarArrowStyle", "H")
ThemeScrollBarThumbStyle = Type("ThemeScrollBarThumbStyle", "H")
CTabHandle = OpaqueByValueType("CTabHandle", "ResObj")
ThemeTrackEnableState = Type("ThemeTrackEnableState", "b")
ThemeTrackPressState = Type("ThemeTrackPressState", "b")
ThemeThumbDirection = Type("ThemeThumbDirection", "b")
ThemeTrackAttributes = Type("ThemeTrackAttributes", "H")
ControlPartCode = Type("ControlPartCode", "h")
ThemeWindowAttributes = Type("ThemeWindowAttributes", "l")
ThemeWindowType = Type("ThemeWindowType", "H")
ThemeTitleBarWidget = Type("ThemeTitleBarWidget", "H")
ThemeArrowOrientation = Type("ThemeArrowOrientation", "H")
ThemePopupArrowSize = Type("ThemePopupArrowSize", "H")
ThemeGrowDirection = Type("ThemeGrowDirection", "H")
ThemeSoundKind = OSTypeType("ThemeSoundKind")
ThemeDragSoundKind = OSTypeType("ThemeDragSoundKind")
ThemeBackgroundKind = Type("ThemeBackgroundKind", "l")
ThemeMetric = Type("ThemeMetric", "l")
RGBColor = OpaqueType("RGBColor", "QdRGB")
TruncCode = Type("TruncCode", "h")


ThemeButtonKind = UInt16
ThemeButtonDrawInfo_ptr = OpaqueType("ThemeButtonDrawInfo", "ThemeButtonDrawInfo")
ThemeEraseUPP = FakeType("NULL")
ThemeButtonDrawUPP = FakeType("NULL")


includestuff = includestuff + """
#ifdef WITHOUT_FRAMEWORKS
#include <Appearance.h>
#else
#include <Carbon/Carbon.h>
#endif



int ThemeButtonDrawInfo_Convert(PyObject *v, ThemeButtonDrawInfo *p_itself)
{
	return PyArg_Parse(v, "(iHH)", &p_itself->state, &p_itself->value, &p_itself->adornment);
}

"""

class MyObjectDefinition(PEP253Mixin, GlobalObjectDefinition):
	pass
## 	def outputCheckNewArg(self):
## 		Output("if (itself == NULL) return PyMac_Error(resNotFound);")
## 	def outputCheckConvertArg(self):
## 		OutLbrace("if (DlgObj_Check(v))")
## 		Output("*p_itself = ((WindowObject *)v)->ob_itself;")
## 		Output("return 1;")
## 		OutRbrace()
## 		Out("""
## 		if (v == Py_None) { *p_itself = NULL; return 1; }
## 		if (PyInt_Check(v)) { *p_itself = (WindowPtr)PyInt_AsLong(v); return 1; }
## 		""")

# From here on it's basically all boiler plate...

# Create the generator groups and link them
module = MacModule(MODNAME, MODPREFIX, includestuff, finalstuff, initstuff)
object = MyObjectDefinition(OBJECTNAME, OBJECTPREFIX, OBJECTTYPE)
module.addobject(object)

ThemeDrawingState = OpaqueByValueType("ThemeDrawingState", "ThemeDrawingStateObj")
Method = WeakLinkMethodGenerator


# Create the generator classes used to populate the lists
Function = OSErrWeakLinkFunctionGenerator
##Method = OSErrWeakLinkMethodGenerator

# Create and populate the lists
functions = []
methods = []
execfile(INPUTFILE)

# add the populated lists to the generator groups
# (in a different wordl the scan program would generate this)
for f in functions: module.add(f)
for f in methods: object.add(f)

# generate output (open the output file as late as possible)
SetOutputFileName(OUTPUTFILE)
module.generate()

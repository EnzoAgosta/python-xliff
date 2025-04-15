from dataclasses import dataclass
from enum import Enum


class COUNTTYPE(Enum):
    NUM_USAGE = "num-usages"
    REPETITION = "repetition"
    TOTAL = "total"


class UNIT(Enum):
    WORD = "word"
    PAGE = "page"
    TRANSUNIT = "trans-unit"
    BINUNIT = "binunit"
    GLYPH = "glyph"
    ITEM = "item"
    INSTANCE = "instance"
    CHARACTER = "character"
    LINE = "line"
    SENTENCE = "sentence"
    PARAGRAPH = "paragraph"
    SEGMENT = "segment"
    PLACEABLE = "placeable"


class CONTEXTTYPE(Enum):
    DATABASE = "database"
    ELEMENT = "element"
    ELEMENTTITLE = "elementtitle"
    LINENUMBER = "linenumber"
    NUMPARAMS = "numparams"
    PARAMNOTES = "paramnotes"
    RECORD = "record"
    RECORDTITLE = "recordtitle"
    SOURCEFIL = "sourcefil"


class PURPOSE(Enum):
    INFORMATION = "information"
    LOCATION = "location"
    MATCH = "match"


class DATACLASS(Enum):
    ASP = "asp"
    C = "c"
    CDF = "cdf"
    CFM = "cfm"
    CPP = "cpp"
    CSHARP = "csharp"
    CSTRING = "cstring"
    CSV = "csv"
    DATABASE = "database"
    DOCUMENTFOOTER = "documentfooter"
    DOCUMENTHEADER = "documentheader"
    FILEDIALOG = "filedialog"
    FORM = "form"
    HTML = "html"
    HTMLBODY = "htmlbody"
    INI = "ini"
    INTERLEAF = "interleaf"
    JAVACLASS = "javaclass"
    JAVAPROPERTYRESOURCEBUNDLE = "javapropertyresourcebundle"
    JAVALISTRESOURCEBUNDLE = "javalistresourcebundle"
    JAVASCRIPT = "javascript"
    JSCRIPT = "jscript"
    LAYOUT = "layout"
    LISP = "lisp"
    MARGIN = "margin"
    MENUFILE = "menufile"
    MESSAGEFILE = "messagefile"
    MIF = "mif"
    MIMETYPE = "mimetype"
    MO = "mo"
    MSGLIB = "msglib"
    PAGEFOOTER = "pagefooter"
    PAGEHEADER = "pageheader"
    PARAMETERS = "parameters"
    PASCAL = "pascal"
    PHP = "php"
    PLAINTEXT = "plaintext"
    PO = "po"
    REPORT = "report"
    RESOURCES = "resources"
    RESX = "resx"
    RTF = "rtf"
    SGML = "sgml"
    SGMLDTD = "sgmldtd"
    SVG = "svg"
    VBSCRIPT = "vbscript"
    WARNING = "warning"
    WINRES = "winres"
    XHTML = "xhtml"
    XML = "xml"
    XMLDTD = "xmldtd"
    XSL = "xsl"
    XUL = "xul"


class RESTYPE(Enum):
    AUTO3STATE = "auto3state"
    AUTOCHECKBOX = "autocheckbox"
    AUTORADIOBUTTON = "autoradiobutton"
    BEDIT = "bedit"
    BITMAP = "bitmap"
    BUTTON = "button"
    CAPTION = "caption"
    CELL = "cell"
    CHECKBOX = "checkbox"
    CHECKBOXMENUITEM = "checkboxmenuitem"
    CHECKEDLISTBOX = "checkedlistbox"
    COLORCHOOSER = "colorchooser"
    COMBOBOX = "combobox"
    COMBOBOXEXITEM = "comboboxexitem"
    COMBOBOXITEM = "comboboxitem"
    COMPONENT = "component"
    CONTEXTMENU = "contextmenu"
    CTEXT = "ctext"
    CURSOR = "cursor"
    DATETIMEPICKER = "datetimepicker"
    DEFPUSHBUTTON = "defpushbutton"
    DIALOG = "dialog"
    DLGINIT = "dlginit"
    EDIT = "edit"
    FILE = "file"
    FILECHOOSER = "filechooser"
    FN = "fn"
    FONT = "font"
    FOOTER = "footer"
    FRAME = "frame"
    GRID = "grid"
    GROUPBOX = "groupbox"
    HEADER = "header"
    HEADING = "heading"
    HEDIT = "hedit"
    HSCROLLBAR = "hscrollbar"
    ICON = "icon"
    IEDIT = "iedit"
    KEYWORDS = "keywords"
    LABEL = "label"
    LINKLABEL = "linklabel"
    LIST = "list"
    LISTBOX = "listbox"
    LISTITEM = "listitem"
    LTEXT = "ltext"
    MENU = "menu"
    MENUBAR = "menubar"
    MENUITEM = "menuitem"
    MENUSEPARATOR = "menuseparator"
    MESSAGE = "message"
    MONTHCALENDAR = "monthcalendar"
    NUMERICUPDOWN = "numericupdown"
    PANEL = "panel"
    POPUPMENU = "popupmenu"
    PUSHBOX = "pushbox"
    PUSHBUTTON = "pushbutton"
    RADIO = "radio"
    RADIOBUTTONMENUITEM = "radiobuttonmenuitem"
    RCDATA = "rcdata"
    ROW = "row"
    RTEXT = "rtext"
    SCROLLPANE = "scrollpane"
    SEPARATOR = "separator"
    SHORTCUT = "shortcut"
    SPINNER = "spinner"
    SPLITTER = "splitter"
    STATE3 = "state3"
    STATUSBAR = "statusbar"
    STRING = "string"
    TABCONTROL = "tabcontrol"
    TABLE = "table"
    TEXTBOX = "textbox"
    TOGGLEBUTTON = "togglebutton"
    TOOLBAR = "toolbar"
    TOOLTIP = "tooltip"
    TRACKBAR = "trackbar"
    TREE = "tree"
    URI = "uri"
    USERBUTTON = "userbutton"
    USERCONTROL = "usercontrol"
    VAR = "var"
    VERSIONINFO = "versioninfo"
    VSCROLLBAR = "vscrollbar"
    WINDOW = "window"


@dataclass
class Coord:
    x: float | int | None = None
    y: float | int | None = None
    cx: float | int | None = None
    cy: float | int | None = None

    def __str__(self) -> str:
        return ";".join(
            str(i) if i else "#" for i in (self.x, self.y, self.cx, self.cy)
        )


@dataclass
class Font:
    name: str
    size: str | None = None
    weight: str | None = None
    style: str | None = None

    def __str__(self) -> str:
        return ";".join(
            str(i) if i else "#"
            for i in (self.name, self.size, self.weight, self.style)
        )


class SIZEUNIT(Enum):
    BYTE = "byte"
    CHAR = "char"
    COL = "col"
    CM = "cm"
    DLGUNIT = "dlgunit"
    EM = "em"
    EX = "ex"
    GLYPH = "glyph"
    IN = "in"
    MM = "mm"
    PERCENT = "percent"
    PIXEL = "pixel"
    POINT = "point"
    ROW = "row"

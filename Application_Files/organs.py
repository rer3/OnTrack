#!/usr/bin/env python2.7
"""
This module contains common tools used by other application modules.
----------
These tools consist of standard QFont objects, custom QWidget subclasses, and
helper functions that analyze objects.
----------
Fonts: all QFont objects used by the GUI and dialogs.
    arial_huge: Arial, 40 pt, 75 wt
    arial_large: Arial, 24 pt, 75 wt
    arial_medium: Arial, 13 pt, 75 wt
    arial_small: Arial, 9 pt, 75 wt
    tahoma_large: Tahoma 10 pt, 75 wt
    tahoma_medium: Tahoma 9 pt
    tahoma_small: Tahoma 8 pt

Custom QWidget Wrappers: QWidget subclasses with custom attributes and methods.
These classes allow properties to be passed as args to QWidget constructors
rather than to be explicitly set following instantiation. These convenience
subclasses enable brevity in GUI component setup.
    BuildViewer: QTreeWidget subclass to create the Build Viewer tree
    DataProcessor: QThread subclass to process data and return results
    EasyButtonBox: QDialogButtonBox subclass with easy constructor
    EasyComboBox: QComboBox subclass with easy constructor
    EasyDateEdit: QDateEdit subclass with easy constructor
    EasyDateTimeEdit: QDateTimeEdit subclass with easy constructor
    EasyDialog: QDialog subclass with easy constructor
    EasyFileDialog: QFileDialog subclass with easy constructor
    EasyFrame: QFrame subclass with easy constructor
    EasyIcon: QIcon subclass with easy constructor
    EasyLabel: QLabel subclass with easy constructor
    EasyLineEdit: QLineEdit subclass with easy constructor
    EasyTableWidget: QTableWidget subclass with easy constructor
    EasyTimeEdit: QTimeEdit subclass with easy constructor
    EasyToolButton: QToolButton subclass with easy constructor
    MessageDialog: EasyDialog subclass to display a persistent message
    OutlineFrame: QFrame subclass to display an outline frame in a dialog
    TipBox: QPlainTextEdit subclass to display guidelines and instructions
    ViewItemDialog: EasyDialog subclass to show inventory item properties

Helper Functions: functions that analyze objects and return new objects or
values based on the analyses.
    consecutive_dict: function to return a dictionary whose source dict has had
        all keys within a specified numeric range reassigned so that all keys
        in that range are now consecutive, starting with the minimum key in the
        range and incrementing by 1, with the original values remapped to the
        new keys and out of range key-value pairs kept intact
    eval_fraction: function to return the float value of a valid fraction or,
        if the fraction is invalid, None
    is_decimal: function to identify numeric strings that can be parsed as
        floats rather than integers
    maxed_dicts: function to return a merged dictionary wherein each key found
        in more than one constituent dict is mapped to the maximum of all
        constituent dict values mapped to that key
    max_key: function to return the largest key, relative to the other keys and
        within a specified key range, from a dictionary
    min_key: function to return the smallest key, relative to the other keys
        and within a specified key range, from a dictionary
    numeric_value: function to return the int or float (rounded to three
        decimal places) value of a string, or None if it is not a number
    process_item_counts: return all references to an inventory item in the
        current build and applicable template and record inventories
    summed_dicts: function to return a merged dictionary wherein each key found
        in more than one constituent dict is mapped to the sum of all
        constituent dict values mapped to that key
    unique_keys: function to return all unique keys at a given depth in a
        dictionary of nested dictionaries
"""


import datetime

from PyQt4 import QtCore
from PyQt4 import QtGui

import album
import dna


# -----------------------------------------------------------------------------
# Fonts -----------------------------------------------------------------------

arial_huge = QtGui.QFont()
arial_huge.setFamily("Arial")
arial_huge.setPointSize(40)
arial_huge.setWeight(75)

arial_large = QtGui.QFont()
arial_large.setFamily("Arial")
arial_large.setPointSize(24)
arial_large.setWeight(75)

arial_medium = QtGui.QFont()
arial_medium.setFamily("Arial")
arial_medium.setPointSize(13)
arial_medium.setWeight(75)

arial_small = QtGui.QFont()
arial_small.setFamily("Arial")
arial_small.setPointSize(9)
arial_small.setWeight(75)

tahoma_large = QtGui.QFont()
tahoma_large.setFamily("Tahoma")
tahoma_large.setPointSize(10)
tahoma_large.setWeight(75)

tahoma_medium = QtGui.QFont()
tahoma_medium.setFamily("Tahoma")
tahoma_medium.setPointSize(9)

tahoma_small = QtGui.QFont()
tahoma_small.setFamily("Tahoma")
tahoma_small.setPointSize(8)


# -----------------------------------------------------------------------------
# Custom QWidget Wrappers -----------------------------------------------------

class BuildViewer(QtGui.QTreeWidget):
    """
    QTreeWidget subclass to create the Build Viewer.

    BuildViewer is used to create the Build Viewer, a QTreeWidget with custom
    properties. The parent QMainWindow and dimensions are passed to its
    constructor. It inherits all attributes and methods from its superclass.
    Additional methods are implemented to set and remove its Build Parent.
    """

    def __init__(self, parent, geom):
        """
        Initialize a BuildViewer object.

        :param parent: Parent QMainWindow
        :type: parent QMainWindow
        :param geom: List with [xpos, ypos, width, height] to set geometry
        :type geom: list
        """
        QtGui.QTreeWidget.__init__(self, parent)
        self.setGeometry(*geom)
        self.setStyleSheet(dna.STYLE_TREE)
        self.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.setColumnCount(1)
        self.header().setResizeMode(QtGui.QHeaderView.ResizeToContents)
        self.header().setStretchLastSection(False)
        self.headerItem().setText(0, "Build Viewer")

    def buildparent(self):
        """Return the Build Parent."""
        build_parent = self.topLevelItem(0)
        if build_parent == 0:
            return None
        return build_parent

    def clear_buildparent(self):
        """Clear the Build Viewer of its current Build Parent."""
        self.blockSignals(True)
        self.headerItem().setText(0, "Build Viewer")
        self.takeTopLevelItem(0)
        self.blockSignals(False)

    def set_buildparent(self, new_buildparent):
        """
        Set the Build Parent of the Build Viewer.

        :param new_buildparent: The new Build Parent object
        :type new_buildparent: Recipe, Meal, Diet, Workout, Cycle, Program
        """
        cid = new_buildparent.cid()
        header = "Your " + dna.BUILD_ELEMENTS[cid][0]
        self.headerItem().setText(0, header)
        self.blockSignals(True)
        self.addTopLevelItem(new_buildparent)
        self.setCurrentItem(new_buildparent)
        self.blockSignals(False)


class DataProcessor(QtCore.QThread):
    """
    QThread subclass to process large data sets and return the result.

    DataProcessor is used to process data sets without freezing the GUI. It
    inherits from the QThread superclass and overrides the run method. A
    processing function and all its kwargs are passed to this class when it is
    instantiated. The overriding run method executes this function on the
    kwargs and emits the data_processed signal, which carries with it the
    resulting data set. The function and kwargs are stored in instance
    attributes. Methods are implemented to assign new values to these
    attributes after a DataProcessor object has been constructed.
    """

    data_processed = QtCore.pyqtSignal(object)

    def __init__(self, parent, func=None, **kwargs):
        """
        Initialize a DataProcessor object.

        :param parent: Parent QWidget
        :type parent: QWidget
        :param func: A data processing function
        :type func: function
        :param kwargs: Keyword args to pass to the data processing function
        :type kwargs: dict
        """
        QtCore.QThread.__init__(self, parent)
        self._func = func
        self._kwargs = kwargs

    def set_func(self, func):
        """
        Assign a function to the _func attribute.

        :param func: A data processing function
        :type func: function
        """
        self._func = func

    def set_kwargs(self, **kwargs):
        """
        Assign keyword args to the _kwargs attribute.

        :param kwargs: Keyword args
        :type kwargs: dict
        """
        self._kwargs = kwargs

    def run(self):
        """Run processing function with kwargs and emit resulting data set."""
        result = self._func(**self._kwargs)
        self.data_processed.emit(result)


class EasyButtonBox(QtGui.QDialogButtonBox):
    """
    Class for constructing a customized QDialogButtonBox object.

    EasyButtonBox is used to create a standardized QDialogButtonBox by passing
    the parent QDialog object to its constructor. It inherits all attributes
    and methods from its superclass. Its size is constant and its position is
    dependent on the dimensions of its parent. The 'Ok' and 'Cancel' buttons
    are centered.
    """

    def __init__(self, parent):
        """
        Initialize an EasyButtonBox object.

        :param parent: Parent QDialog
        :type parent: QDialog
        """
        QtGui.QDialogButtonBox.__init__(self, parent)
        width = parent.geometry().width()
        height = parent.geometry().height()
        self.setGeometry((width / 2) - 100, height - 40, 200, 28)
        self.setStandardButtons(
            QtGui.QDialogButtonBox.Ok | QtGui.QDialogButtonBox.Cancel)
        self.setCenterButtons(True)


class EasyComboBox(QtGui.QComboBox):
    """
    Class for constructing a customized QComboBox object.

    EasyComboBox is used to create a standardized QComboBox by passing custom
    kwargs to its constructor. It inherits all attributes and methods from its
    superclass. The parent and geom args must be passed to the constructor when
    an EasyComboBox object is instantiated. Optional args can be passed to the
    constructor to set its properties.
    """

    def __init__(self, parent, geom, fixed_size=False, first_item=None,
                 items=None, max_visible=None, style_sheet=None,
                 status_tip=None, tool_tip=None):
        """
        Initialize an EasyComboBox object.

        :param parent: Parent QWidget
        :type parent: QWidget
        :param geom: List with [xpos, ypos, width, height] to set geometry
        :type geom: list
        :param fixed_size: Bool to determine if its size is fixed
        :type fixed_size: bool
        :param first_item: Item to add to the item list first
        :type first_time: str, None
        :param items: All items to add to the item list after the first item
        :type items: list, None
        :param max_visible: Maximum number of visible items
        :type max_visible: int, None
        :param style_sheet: Style sheet
        :type style_sheet: str
        :param status_tip: Status tip text
        :type status_tip: str
        :param tool_tip: Tool tip text
        :type tool_tip: str
        """
        QtGui.QComboBox.__init__(self, parent)
        self.setGeometry(*geom)
        if fixed_size:
            self.setFixedSize(geom[2], geom[3])
        if first_item is not None:
            self.addItem(first_item)
        if items is not None:
            self.addItems(items)
        if max_visible is not None:
            self.setMaxVisibleItems(max_visible)
        if style_sheet is not None:
            self.setStyleSheet(style_sheet)
        if status_tip is not None:
            self.setStatusTip(status_tip)
        if tool_tip is not None:
            self.setToolTip(tool_tip)


class EasyDateEdit(QtGui.QDateEdit):
    """
    Class for constructing a customized QDateEdit object.

    EasyDateEdit is used to create a standardized QDateEdit by passing custom
    kwargs to its constructor. It inherits all attributes and methods from its
    superclass. The parent and geom args must be passed to the constructor when
    an EasyDateEdit object is instantiated. Optional args can be passed to the
    constructor to set its properties.
    """

    def __init__(self, parent, geom, fixed_size=False, display_format=None,
                 date=None, minimum_date=None, maximum_date=None,
                 calendar_on=False):
        """
        Initialize an EasyDateEdit object.

        :param parent: Parent QWidget
        :type parent: QWidget
        :param geom: List with [xpos, ypos, width, height] to set geometry
        :type geom: list
        :param fixed_size: Bool to determine if its size is fixed
        :type fixed_size: bool
        :param display_format: Date display format
        :type display_format: str
        :param date: List with [year, month, day] to set date value
        :type date: list
        :param minimum_date: List with [year, month, day] to set minimum date
        :type minimum_date: list
        :param maximum_date: List with [year, month, day] to set maximum date
        :type maximum_date: list
        :param calendar_on: Bool to determine if calendar tool is available
        :type calendar_on: bool
        """
        QtGui.QDateEdit.__init__(self, parent)
        self.setGeometry(*geom)
        # Set minimum date year to greater than 1900 to avoid strftime errors.
        # The year 2000 is used as the default minimum year value.
        self.setMinimumDate(QtCore.QDate(2000, 1, 1))
        if fixed_size:
            self.setFixedSize(geom[2], geom[3])
        if display_format is not None:
            self.setDisplayFormat(display_format)
        if date is not None:
            self.setDate(QtCore.QDate(date[0], date[1], date[2]))
        if minimum_date is not None:
            year = 2000 if minimum_date[0] < 2000 else minimum_date[0]
            self.setMinimumDate(QtCore.QDate(
                year, minimum_date[1], minimum_date[2]))
        if maximum_date is not None:
            self.setMaximumDate(QtCore.QDate(
                maximum_date[0], maximum_date[1], maximum_date[2]))
        if calendar_on:
            self.setCalendarPopup(True)


class EasyDateTimeEdit(QtGui.QDateTimeEdit):
    """
    Class for constructing a customized QDateTimeEdit object.

    EasyDateTimeEdit is used to create a standardized QDateTimeEdit by passing
    custom kwargs to its constructor. It inherits all attributes and methods
    from its superclass. The parent and geom args must be passed to the
    constructor when an EasyDateTimeEdit object is instantiated. Optional args
    can be passed to the constructor to set its properties.
    """

    def __init__(self, parent, geom, display_format=None, date_time=None,
                 calendar_on=False):
        """
        Initialize an EasyDateTimeEdit object.

        :param parent: Parent QWidget
        :type parent: QWidget
        :param geom: List with [xpos, ypos, width, height] to set geometry
        :type geom: list
        :param display_format: Date display format
        :type display_format: str
        :param date_time: List with [year, month, day, hour, minute] to set
            datetime value
        :type date_time: list
        :param calendar_on: Bool to determine if calendar tool is available
        :type calendar_on: bool
        """
        QtGui.QDateTimeEdit.__init__(self, parent)
        self.setGeometry(*geom)
        # Set minimum date year to greater than 1900 to avoid strftime errors.
        # The year 2000 is used as the default minimum year value.
        self.setMinimumDateTime(
            QtCore.QDateTime(QtCore.QDate(2000, 1, 1), QtCore.QTime(0, 0)))
        if display_format is not None:
            self.setDisplayFormat(display_format)
        if date_time is not None:
            self.setDateTime(
                QtCore.QDateTime(
                    QtCore.QDate(date_time[0], date_time[1], date_time[2]),
                    QtCore.QTime(date_time[3], date_time[4])))
        if calendar_on:
            self.setCalendarPopup(True)


class EasyDialog(QtGui.QDialog):
    """
    Class for constructing a customized QDialog object.

    EasyDialog is used to create a standardized QDialog by passing the parent
    QWidget object to its constructor. It inherits all attributes and methods
    from its superclass. It implements a center method.
    """

    def __init__(self, parent):
        """
        Initialize an EasyDialog object.

        :param parent: Parent QWidget
        :type parent: QWidget
        """
        QtGui.QDialog.__init__(self, parent)

    def center(self):
        """Center the dialog."""
        screen = QtGui.QDesktopWidget().availableGeometry().center()
        x = screen.x() - (self.width() / 2)
        y = screen.y() - (self.height() / 2)
        self.move(x, y)


class EasyFileDialog(QtGui.QFileDialog):
    """
    Class for constructing a customized QFileDialog object.

    EasyFileDialog is used to create a standardized QFileDialog by passing
    custom kwargs to its constructor. It inherits all attributes and methods
    from its superclass. The parent and dialog_type args must be passed to the
    constructor when an EasyFileDialog object is instantiated.
    """

    def __init__(self, parent, dialog_type, file_name=None):
        """
        Initialize an EasyFileDialog object.

        :param parent: Parent QMainWindow
        :type parent: QMainWindow
        :param dialog_type: The type of file dialog: 'healthdiary' for
            selecting the directory in which to save the Health Diary as a
            spreadsheet, 'loadcapsule' for selecting data capsule files to
            load, or 'savecapsule' for selecting a directory in which to save
            data capsules
        :type dialog_type: str
        :param file_name: The file name to display in the applicable field
        :type file_name: str
        """
        QtGui.QFileDialog.__init__(self, parent)
        if dialog_type == "healthdiary":
            self.setWindowTitle("Save Health Diary")
            self.selectFile(file_name)
            self.setAcceptMode(QtGui.QFileDialog.AcceptSave)
            self.setNameFilter("Excel files (*.json)")
        elif dialog_type == "loadcapsule":
            self.setWindowTitle("Select All Data Capsule")
            self.setFileMode(QtGui.QFileDialog.ExistingFiles)
            self.setNameFilter("Data Capsule (*.json)")
        elif dialog_type == "savecapsule":
            self.setWindowTitle("Save Data Capsule")
            self.selectFile(file_name)
            self.setAcceptMode(QtGui.QFileDialog.AcceptSave)
            self.setNameFilter("Data Capsule (*.json)")


class EasyFrame(QtGui.QFrame):
    """
    Class for constructing a customized QFrame object.

    EasyFrame is used to create a standardized QFrame by passing custom kwargs
    to its constructor. It inherits all attributes and methods from its
    superclass. The parent and geom args must be passed to the constructor
    when an EasyFrame object is instantiated. Optional args can be passed to
    the constructor to set its properties.
    """

    def __init__(self, parent, geom, object_name=None, style_sheet=None,
                 frame_shadow=None, frame_shape=None, main=False, login=False,
                 profile=False):
        """
        Initialize an EasyFrame object.

        :param parent: Parent QWidget
        :type parent: QWidget
        :param geom: List with [xpos, ypos, width, height] to set geometry
        :type geom: list
        :param object_name: Name of object, used for style sheet id selector
        :type object_name: str
        :param style_sheet: Style sheet
        :type style_sheet: str
        :param frame_shadow: Frame shadow
        :type frame_shadow: QtGui.QFrame.Shadow
        :param frame_shape: Frame shape
        :type frame_shape: QtGui.QFrame.Shape
        :param main: True to set up Main Menu properties, else False
        :type main: bool
        :param login: True to set up Login Menu properties, else False
        :type login: bool
        :param profile: True to set up Profile frame properties, else False
        :type profile: bool
        """
        QtGui.QFrame.__init__(self, parent)
        self.setGeometry(*geom)
        if object_name is not None:
            self.setObjectName(object_name)
        if style_sheet is not None:
            self.setStyleSheet(style_sheet)
        if frame_shadow is not None:
            self.setFrameShadow(frame_shadow)
        if frame_shape is not None:
            self.setFrameShape(frame_shape)
        if main:
            self.setStyleSheet(dna.STYLE_MAINFRAME)
            self.setFrameShadow(QtGui.QFrame.Sunken)
            self.setFrameShape(QtGui.QFrame.StyledPanel)
        if login:
            self.setObjectName("login")
            self.setStyleSheet(dna.STYLE_LOGINFRAME)
        if profile:
            self.setObjectName("profile")
            self.setStyleSheet(dna.STYLE_PROFILEFRAME)


class EasyIcon(QtGui.QIcon):
    """
    Class for constructing a customized QIcon object.

    EasyIcon is used to create a standardized QIcon by passing the icon name
    to its constructor. It inherits all attributes and methods from its
    superclass. Its pixmap is created for the applicable icon name located in
    the resource data.
    """

    def __init__(self, icon_name):
        """
        Initialize an EasyIcon object.

        :param icon_name: Name of icon in resource data
        :type icon_name: str
        """
        QtGui.QIcon.__init__(self)
        self.addPixmap(
            QtGui.QPixmap(":/icons/" + icon_name + ".png"),
            QtGui.QIcon.Normal, QtGui.QIcon.Off)


class EasyLabel(QtGui.QLabel):
    """
    Class for constructing a customized QLabel object.

    EasyLabel is used to create a standardized QLabel by passing custom kwargs
    to its constructor. It inherits all attributes and methods from its
    superclass. The parent and geom args must be passed to the constructor when
    an EasyLabel object is instantiated. Optional args can be passed to the
    constructor to set its properties. Label text is center-aligned by default.
    """

    def __init__(self, parent, geom, fixed_size=False, text=None, font=None,
                 alignment=None, style_sheet=None):
        """
        Initialize an EasyLabel object.

        :param parent: Parent QWidget
        :type parent: QWidget
        :param geom: List with [xpos, ypos, width, height] to set geometry
        :type geom: list
        :param fixed_size: Bool to determine if its size is fixed
        :type fixed_size: bool
        :param text: Text to display on the label
        :type text: str
        :param font: Font of the label text
        :type font: QFont
        :param alignment: Alignment of the label text
        :type alignment: QtCore.Qt.Alignment
        :param style_sheet: Style sheet
        :type style_sheet: str
        """
        QtGui.QLabel.__init__(self, parent)
        self.setGeometry(*geom)
        self.setAlignment(QtCore.Qt.AlignCenter)
        if fixed_size:
            self.setFixedSize(geom[2], geom[3])
        if text is not None:
            self.setText(text)
        if font is not None:
            self.setFont(font)
        if alignment is not None:
            self.setAlignment(alignment)
        if style_sheet is not None:
            self.setStyleSheet(style_sheet)


class EasyLineEdit(QtGui.QLineEdit):
    """
    Class for constructing a customized QLineEdit object.

    EasyLineEdit is used to create a standardized QLineEdit by passing custom
    kwargs to its constructor. It inherits all attributes and methods from its
    superclass. The parent and geom args must be passed to the constructor
    when an EasyLineEdit object is instantiated. Optional args can be passed to
    the constructor to set its properties.
    """

    def __init__(self, parent, geom, text=None, max_length=None,
                 placeholder_text=None):
        """
        Initialize an EasyLineEdit object.

        :param parent: Parent QWidget
        :type parent: QWidget
        :param geom: List with [xpos, ypos, width, height] to set geometry
        :type geom: list
        :param text: Line text value
        :type text: str
        :param max_length: Maximum character length of line text
        :type max_length: int
        :param placeholder_text: Placeholder text for an empty line
        :type placeholder_text: str
        """
        QtGui.QLineEdit.__init__(self, parent)
        self.setGeometry(*geom)
        if text is not None:
            self.setText(text)
        if max_length is not None:
            self.setMaxLength(max_length)
        if placeholder_text is not None:
            self.setPlaceholderText(placeholder_text)


class EasyTableWidget(QtGui.QTableWidget):
    """
    Class for constructing a customized QTableWidget object.

    EasyTableWidget is used to create a standardized QTableWidget by passing
    custom kwargs to its constructor. It inherits all attributes and methods
    from its superclass. The parent and geom args must be passed to the
    constructor when an EasyTableWidget object is instantiated. Optional args
    can be passed to the constructor to set its properties. An added benefit
    of the EasyTableWidget constructor is that empty QTableWidgetItems are
    constructed and added to the table when a list of dimensions are assigned
    to the dims parameter. Horizontal scrolling is set to scroll per pixel by
    default.
    """

    def __init__(self, parent, geom, dims=None, center_text=False,
                 column_labels=None, column_width=None, column_widths=None,
                 column_header_hidden=False, row_labels=None,
                 row_label_alignment=None, row_height=None,
                 row_header_width=None, row_header_hidden=False,
                 row_alternating_colors=False, edit_off=False, grid_off=False,
                 resize_off=False, resize_cols_off=False,
                 resize_rows_off=False, select_rows=False,
                 single_selection=False, sorting=False,
                 stretch_last_section=False):
        """
        Initialize an EasyTableWidget object.

        :param parent: Parent QWidget
        :type parent: QWidget
        :param geom: List with [xpos, ypos, width, height] to set geometry
        :type geom: list
        :param dims: List with [col count, row count] to set dimensions and
            populate empty table with QTableWidgetItem objects
        :type dims: list
        :param center_text: Bool to center QTableWidgetItem text by default
            (applies to EasyTableWidget with nonzero dimensions)
        :type center_text: bool
        :param column_labels: List of horizontal header labels
        :type column_labels: list
        :param column_width: Default column width for all columns
        :type column_width: int
        :param column widths: List of individual column widths
        :type column_widths: list
        :param column_header_hidden: Bool to hide column header
        :type column_header_hidden: bool
        :param row_labels: List of vertical header labels
        :type row_labels: list
        :param row_label_alignment: Alignment of vertical header labels
        :type row_label_alignment: QtCore.Qt.Alignment
        :param row_height: Default row height for all rows
        :type row_height: int
        :param row_header_width: Fixed vertical header width
        :type row_header_width: int
        :param row_header_hidden: Bool to hide row header
        :type row_header_hidden: bool
        :param row_alternating_colors: Bool to alternate row background colors
        :type row_alternating_colors: bool
        :param edit_off: Bool to disable editing of table items
        :type edit_off: bool
        :param grid_off: Bool to disable table grid
        :type grid_off: bool
        :param resize_off: Bool to disable resizing of table rows and columns
        :type resize_off: bool
        :param resize_cols_off: Bool to disable resizing table columns
        :type resize_cols_off: bool
        :param resize_rows_off: Bool to disable resizing table rows
        :type resize_rows_off: bool
        :param select_rows: Bool to enable row selection
        :type select_rows: bool
        :param single_selection: Bool to enable single item selection
        :type single_selection: bool
        :param sorting: Bool to enable column sorting
        :type sorting: bool
        :param stretch_last_section: Bool to stretch last column width
        :type stretch_last_section: bool
        """
        QtGui.QTableWidget.__init__(self, parent)
        self.setGeometry(*geom)
        self.setHorizontalScrollMode(QtGui.QAbstractItemView.ScrollPerPixel)
        if dims is not None:
            self.setColumnCount(dims[0])
            self.setRowCount(dims[1])
            for col in range(dims[0]):
                for row in range(dims[1]):
                    item = QtGui.QTableWidgetItem()
                    if center_text:
                        item.setTextAlignment(QtCore.Qt.AlignCenter)
                    self.setItem(row, col, item)
        if column_labels is not None:
            self.setHorizontalHeaderLabels(column_labels)
        if column_width is not None:
            self.horizontalHeader().setDefaultSectionSize(column_width)
        if column_widths is not None:
            for idx in range(len(column_widths)):
                width = column_widths[idx]
                self.setColumnWidth(idx, width)
        if column_header_hidden:
            self.horizontalHeader().hide()
        if row_labels is not None:
            self.setVerticalHeaderLabels(row_labels)
        if row_label_alignment is not None:
            self.verticalHeader().setDefaultAlignment(row_label_alignment)
        if row_height is not None:
            self.verticalHeader().setDefaultSectionSize(row_height)
        if row_header_width is not None:
            self.verticalHeader().setFixedWidth(row_header_width)
        if row_header_hidden:
            self.verticalHeader().hide()
        if row_alternating_colors:
            self.setAlternatingRowColors(True)
        if edit_off:
            self.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        if grid_off:
            self.setShowGrid(False)
        if resize_off:
            self.horizontalHeader().setResizeMode(QtGui.QHeaderView.Fixed)
            self.verticalHeader().setResizeMode(QtGui.QHeaderView.Fixed)
        if resize_cols_off:
            self.horizontalHeader().setResizeMode(QtGui.QHeaderView.Fixed)
        if resize_rows_off:
            self.verticalHeader().setResizeMode(QtGui.QHeaderView.Fixed)
        if select_rows:
            self.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        if single_selection:
            self.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        if sorting:
            self.setSortingEnabled(True)
        if stretch_last_section:
            self.horizontalHeader().setStretchLastSection(True)


class EasyTimeEdit(QtGui.QTimeEdit):
    """
    Class for constructing a customized QTimeEdit object.

    EasyTimeEdit is used to create a standardized QTimeEdit by passing custom
    kwargs to its constructor. It inherits all attributes and methods from its
    superclass. The parent and geom args must be passed to the constructor when
    an EasyTimeEdit object is instantiated. Optional args can be passed to the
    constructor to set its properties.
    """

    def __init__(self, parent, geom, display_format=None, time=None):
        """
        Initialize an EasyTimeEdit object.

        :param parent: Parent QWidget
        :type parent: QWidget
        :param geom: List with [xpos, ypos, width, height] to set geometry
        :type geom: list
        :param display_format: Date display format
        :type display_format: str
        :param time: List with [hour, minute] to set time value
        :type time: list
        """
        QtGui.QTimeEdit.__init__(self, parent)
        self.setGeometry(*geom)
        if display_format is not None:
            self.setDisplayFormat(display_format)
        if time is not None:
            self.setTime(QtCore.QTime(time[0], time[1]))


class EasyToolButton(QtGui.QToolButton):
    """
    Class for constructing a customized QToolButton object.

    EasyToolButton is used to create a standardized QToolButton by passing
    custom kwargs to its constructor. It inherits all attributes and methods
    from its superclass. The parent and geom args must be passed to the
    constructor when an EasyToolButton object is instantiated. Optional args
    can be passed to the constructor to set its properties.
    """

    def __init__(self, parent, geom, fixed_size=False, text=None, font=None,
                 icon_name=None, icon_size=None, toolbutton_style=None,
                 button_type=None, status_tip=None, tool_tip=None,
                 disable=False):
        """
        Initialize an EasyToolButton object.

        :param parent: Parent QWidget
        :type parent: QWidget
        :param geom: List with [xpos, ypos, width, height] to set geometry
        :type geom: list
        :param fixed_size: Bool to determine if its size is fixed
        :type fixed_size: bool
        :param text: Text to display on the button
        :type text: str
        :param icon_name: Name of the icon to display on the button
        :type icon_name: str
        :param icon_size: List with [width, height] to set icon size
        :type icon_size: list
        :param toolbutton_style: Style of toolbutton text and icon placement
        :type toolbutton_style: QtCore.Qt.ToolButtonStyle
        :param button_type: Designation of button type to set CSS and button
            attributes ("action", "main", "selection")
        :type button_type: str
        :param status_tip: Status tip text
        :type status_tip: str
        :param tool_tip: Tool tip text
        :type tool_tip: str
        :param disable: Bool to disable the button by default
        :type disable: bool
        """
        QtGui.QToolButton.__init__(self, parent)
        self.setGeometry(*geom)
        if fixed_size:
            self.setFixedSize(geom[2], geom[3])
        if text is not None:
            self.setText(text)
        if font is not None:
            self.setFont(font)
        if icon_name is not None:
            button_icon = EasyIcon(icon_name)
            self.setIcon(button_icon)
        if icon_size is not None:
            self.setIconSize(QtCore.QSize(*icon_size))
        if toolbutton_style is not None:
            self.setToolButtonStyle(toolbutton_style)
        if button_type is not None:
            if button_type == "action":
                self.setStyleSheet(dna.STYLE_ACTION)
            elif button_type == "main":
                self.setAutoExclusive(True)
                self.setCheckable(True)
                self.setFont(tahoma_medium)
                self.setIconSize(QtCore.QSize(30, 30))
                self.setStyleSheet(dna.STYLE_MAINFRAME)
                self.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
            elif button_type == "selection":
                self.setAutoExclusive(True)
                self.setCheckable(True)
                self.setStyleSheet(dna.STYLE_SELECTION)
        if status_tip is not None:
            self.setStatusTip(status_tip)
        if tool_tip is not None:
            self.setToolTip(tool_tip)
        if disable:
            self.setEnabled(False)


class MessageDialog(EasyDialog):
    """
    Class for displaying a persistent message when a background process runs.

    MessageDialog is used to create a standardized EasyDialog by passing custom
    kwargs to its constructor. It inherits all attributes and methods from its
    superclass. The parent, title, and message args must be passed to the
    constructor when a MessageDialog object is instantiated. An EasyLabel
    object centered on this dialog displays the message arg. The closeEvent
    method is overridden to prevent the user from manually closing the dialog
    window while the initiating process, typically a data processing thread, is
    still running. The  finished attribute and finish method are used to
    programmatically exit the dialog when the initiating process is completed.
    """

    def __init__(self, parent, title, message):
        """
        Initialize a MessageDialog object.

        :param parent: Parent QWidget
        :type parent: QWidget
        :param title: Dialog window title
        :type title: str
        :param message: Text to display in the dialog's label
        :type message: str
        """
        EasyDialog.__init__(self, parent)
        self.setFixedSize(300, 88)
        self.setWindowIcon(EasyIcon(dna.ICONS["information"]))
        self.setWindowTitle(title)
        self.msg_label = EasyLabel(
            self, [0, 30, 300, 26], text=message, font=arial_small,
            alignment=QtCore.Qt.AlignCenter)
        self.finished = False

    def closeEvent(self, event):
        """
        Close Event for this dialog.

        Overrides EasyDialog.closeEvent to prevent the user from closing
        the dialog by clicking the exit button ("X") in the upper right corner.
        """
        if self.finished:
            EasyDialog.closeEvent(self, event)
        else:
            event.ignore()

    def finish(self):
        """Close the dialog."""
        self.finished = True
        self.close()


class OutlineFrame(QtGui.QFrame):
    """
    Class for displaying an outline frame behind QWidget objects.

    OutlineFrame is used to create a standardized QFrame by passing custom
    kwargs to its constructor. It inherits all attributes and methods from its
    superclass. The parent and geom args must be passed to the constructor when
    an OutlineFrame object is instantiated. The frame shadow is set to Sunken
    and the frame shape is set to Box. These attributes create a simple outline
    inside of which related objects can be placed within a dialog.
    """

    def __init__(self, parent, geom):
        """
        Initialize an OutlineFrame object.

        :param parent: Parent QWidget
        :type parent: QWidget
        :param geom: List with [xpos, ypos, width, height] to set geometry
        :type geom: list
        """
        QtGui.QFrame.__init__(self, parent)
        self.setGeometry(*geom)
        self.setFrameShadow(QtGui.QFrame.Sunken)
        self.setFrameShape(QtGui.QFrame.Box)


class TipBox(QtGui.QPlainTextEdit):
    """
    Class for displaying a 'tip box' with guidelines and/or instructions.

    TipBox is used to create a standardized QPlainTextEdit by passing custom
    kwargs to its constructor. It inherits all attributes and methods from its
    superclass. The parent and geom args must be passed to the constructor when
    a TipBox object is instantiated. The optional text arg sets the text that
    is displayed inside of the QPlainTextEdit object, sets the style sheet,
    and prevents the user from interacting with the text.
    """

    def __init__(self, parent, geom, text=None, font=None, guide=False):
        """
        Initialize a TipBox object.

        :param parent: Parent QWidget
        :type parent: QWidget
        :param geom: List with [xpos, ypos, width, height] to set geometry
        :type geom: list
        :param text: Text displayed inside of the QPlainTextEdit object
        :type text: str
        :param font: Text font
        :type font: QFont
        :param guide: Boolean to set Guide Box attributes
        :type guide: bool
        """
        QtGui.QPlainTextEdit.__init__(self, parent)
        self.setGeometry(*geom)
        if text is not None:
            self.insertPlainText(text)
            self.moveCursor(QtGui.QTextCursor.Start)
            if not guide:
                self.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
                self.setStyleSheet(dna.STYLE_TIPBOX)
            else:
                self.setTextInteractionFlags(QtCore.Qt.TextSelectableByMouse)
        if font is not None:
            self.setFont(font)


# noinspection PyUnusedLocal
class ViewItemDialog(EasyDialog):
    """
    Class for displaying inventory item properties.

    ViewItemDialog is used to create an EasyDialog that displays inventory item
    properties. It inherits all attributes and methods from its superclass.
    The parent, item_element, inventory_id, and item_id args must be passed to
    the constructor when a ViewItem object is instantiated. Properties are
    displayed differently depending on the inventory type, as well as the item
    type within the inventory. These differences include window size, the data
    that are shown, and how the user can interact with those data.
    """

    def __init__(self, parent, item_element, inventory_id, item_id):
        """
        Initialize a ViewItemDialog object.

        :param parent: Parent QWidget
        :type parent: QWidget
        :param item_element: A build element object whose state has been set to
            that of a reference, template, or record inventory item
        :type item_element: Ingredient, Recipe, Meal, Diet, Activity, Workout,
            Cycle, Program
        :param inventory_id: The current inventory ID
        :type inventory_id: int
        :param item_id: The selected item ID
        :type item_id: str
        """
        EasyDialog.__init__(self, parent)
        self.item = item_element
        icon = "nutrition" if inventory_id in [0, 2, 3, 4, 8] else "fitness"
        if inventory_id == 0:
            width, height = 850, 365
            title = "Food Reference Item " + item_id
            # Description and food group table.
            food_viewer = EasyTableWidget(
                self, [5, 5, width - 10, 85], dims=[1, 2], row_height=30,
                column_header_hidden=True, edit_off=True, resize_off=True,
                row_labels=["DESCRIPTION", "FOOD GROUP"])
            food_viewer.item(0, 0).setText(self.item.description())
            food_viewer.item(1, 0).setText(
                dna.FOOD_GROUPS[self.item.groupid()])
            food_viewer.resizeColumnsToContents()
            # Unit sequences table.
            unitsequences_tag = EasyLabel(
                self, [5, 95, width - 10, 26], font=tahoma_medium,
                text="UNIT SEQUENCES: Click a unit sequence serving size " +
                "to see its nutrient content.",
                alignment=QtCore.Qt.AlignVCenter | QtCore.Qt.AlignLeft)
            unit_seqs = self.item.unitsequences()
            self.unitseq_viewer = EasyTableWidget(
                self, [5, 120, width - 10, 130], dims=[2, len(unit_seqs)],
                center_text=True, row_height=24, single_selection=True,
                column_labels=["Serving Size", "Gram Weight"], edit_off=True,
                column_widths=[650], row_header_hidden=True, select_rows=True,
                row_label_alignment=QtCore.Qt.AlignCenter,
                stretch_last_section=True)
            for idx in range(len(unit_seqs)):
                amt, uni, gwt = unit_seqs[idx]
                self.unitseq_viewer.item(idx, 0).setText(str(amt) + "  " + uni)
                self.unitseq_viewer.item(idx, 1).setText(str(gwt))
                self.unitseq_viewer.selectRow(0)
            self.unitseq_viewer.cellPressed.connect(self.update_nutrients)
            # Nutrient content table.
            col_labels = [dna.NUTRIENTS[nid][1] for nid in dna.GUI_NUTRIENTS]
            self.nutcont_viewer = EasyTableWidget(
                self, [5, 255, width - 10, 104], center_text=True,
                dims=[len(dna.GUI_NUTRIENTS), 2], column_labels=col_labels,
                column_width=74, row_labels=["VALUE", "UNIT"], row_height=24,
                row_label_alignment=QtCore.Qt.AlignCenter, edit_off=True,
                resize_rows_off=True)
            nutcont = self.item.nutrientcontent()
            gram_wt = unit_seqs[0][2]
            for nid in dna.GUI_NUTRIENTS:
                col = dna.GUI_NUTRIENTS.index(nid)
                if nid in nutcont:
                    value = str(
                        numeric_value((gram_wt / 100.0) * nutcont[nid]))
                else:
                    value = "0"
                self.nutcont_viewer.item(0, col).setText(value)
                self.nutcont_viewer.item(1, col).setText(dna.NUTRIENTS[nid][2])
                self.nutcont_viewer.horizontalHeaderItem(col).setToolTip(
                    dna.NUTRIENTS[nid][0])
            self.nutcont_viewer.resizeColumnsToContents()
        elif inventory_id == 1:
            width, height = 850, 190
            title = "Exercise Reference Item " + item_id
            # Properties table.
            row_labs = [
                "DESCRIPTION", "FOCUS MUSCLE", "EFFORT UNIT", "INTENSITY UNIT",
                "TAGS"]
            exercise_viewer = EasyTableWidget(
                self, [5, 5, width - 10, 179], dims=[1, 5], edit_off=True,
                column_header_hidden=True, row_labels=row_labs, row_height=30,
                resize_off=True, row_label_alignment=QtCore.Qt.AlignCenter)
            exercise_viewer.item(0, 0).setText(self.item.description())
            exercise_viewer.item(1, 0).setText(self.item.focusmuscle())
            exercise_viewer.item(2, 0).setText(self.item.units()[0])
            exercise_viewer.item(3, 0).setText(self.item.units()[1])
            tags_string = ", ".join(self.item.tags())
            exercise_viewer.item(4, 0).setText(tags_string)
            exercise_viewer.resizeColumnsToContents()
        elif inventory_id in range(2, 8):
            width, height = 600, 650
            title = dna.BUILD_ELEMENTS[self.item.cid()][0]
            title += " Template Item " + item_id
        elif inventory_id == 8:
            width, height = 600, 650
            title = "Diet Record For " + item_id
        else:
            width, height = 600, 650
            title = "Program Record Starting " + item_id
            # Fitness Info table.
            fit_viewer = EasyTableWidget(
                self, [5, 535, width - 10, 110], dims=[len(dna.MUSCLES), 2],
                center_text=True, column_labels=dna.MUSCLES, column_width=110,
                row_labels=["TOTAL EFFORT", "MAX INTENSITY"], edit_off=True,
                row_label_alignment=QtCore.Qt.AlignCenter, row_height=24,
                resize_rows_off=True)
            effs = self.item.performance_results("effort", "focusmuscle")
            ints = self.item.performance_results("intensity", "focusmuscle")
            # Aggregate effort and intensity values for all Workouts.
            agg_effs = {}
            agg_ints = {}
            for wo_began in effs:
                agg_effs = summed_dicts(agg_effs, effs[wo_began])
                agg_ints = maxed_dicts(agg_ints, ints[wo_began])
            white = [255, 255, 255]
            gray = [227, 229, 229]
            for col in range(fit_viewer.columnCount()):
                c_mus = dna.MUSCLES[col]
                eff_val = "" if c_mus not in agg_effs else str(agg_effs[c_mus])
                int_val = "" if c_mus not in agg_ints else str(agg_ints[c_mus])
                fit_viewer.item(0, col).setText(eff_val)
                fit_viewer.item(1, col).setText(int_val)
                eff_rgb = gray if eff_val == "" else white
                int_rgb = gray if int_val == "" else white
                fit_viewer.item(0, col).setBackground(QtGui.QColor(*eff_rgb))
                fit_viewer.item(1, col).setBackground(QtGui.QColor(*int_rgb))
            fit_viewer.resizeColumnsToContents()
        # Nutrition Info table if nutrition template or record.
        if inventory_id in [2, 3, 4, 8]:
            col_labs = [dna.NUTRIENTS[nid][1] for nid in dna.GUI_NUTRIENTS]
            nut_viewer = EasyTableWidget(
                self, [5, 535, width - 10, 110], center_text=True,
                dims=[len(dna.GUI_NUTRIENTS), 2], column_labels=col_labs,
                column_width=82, row_labels=["VALUE", "UNIT"], edit_off=True,
                row_label_alignment=QtCore.Qt.AlignCenter, row_height=24,
                resize_rows_off=True)
            nvals = {nid: self.item.nutrient_value(nid) for nid in
                     dna.GUI_NUTRIENTS}
            for nid in dna.GUI_NUTRIENTS:
                col = dna.GUI_NUTRIENTS.index(nid)
                nut_viewer.item(0, col).setText(str(round(nvals[nid], 3)))
                nut_viewer.item(1, col).setText(dna.NUTRIENTS[nid][2])
                nut_viewer.horizontalHeaderItem(col).setToolTip(
                    dna.NUTRIENTS[nid][0])
            nut_viewer.resizeColumnsToContents()
        # Build tree viewer if template or record.
        if inventory_id in range(2, 10):
            tree_viewer = QtGui.QTreeWidget(self)
            has_table = [2, 3, 4, 8, 9]
            tree_height = 525 if inventory_id in has_table else height - 10
            tree_viewer.setGeometry(5, 5, width - 10, tree_height)
            tree_viewer.setStyleSheet(dna.STYLE_TREE)
            tree_viewer.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
            tree_viewer.setColumnCount(1)
            # Set stretch last section to False in order to see descriptions
            # that are longer than the window width.
            tree_viewer.header().setStretchLastSection(False)
            h_text = "Double click an item or click its arrow pointer to "
            h_text += "expand or collapse its child elements"
            tree_viewer.headerItem().setText(0, h_text)
            tree_viewer.addTopLevelItem(self.item)
            tree_viewer.setCurrentItem(self.item)
            tree_viewer.expandItem(self.item)
            tree_viewer.header().setResizeMode(
                QtGui.QHeaderView.ResizeToContents)
        # Set window properties.
        self.setFixedSize(width, height)
        self.setWindowIcon(EasyIcon(dna.ICONS[icon]))
        self.setWindowTitle(title)

    def update_nutrients(self, row, col):
        """
        Update nutrient content table based on selected serving size.

        :param row: The row of the pressed cell
        :type row: int
        :param col: The col of the pressed cell (unused here but emitted)
        :type col: int
        """
        nut_cont = self.item.nutrientcontent()
        gram_wt = self.item.unitsequences()[row][2]
        for nid in dna.GUI_NUTRIENTS:
            col = dna.GUI_NUTRIENTS.index(nid)
            if nid in nut_cont:
                value = str(
                    numeric_value((gram_wt / 100.0) * nut_cont[nid], 3))
            else:
                value = "0"
            self.nutcont_viewer.item(0, col).setText(value)
            self.nutcont_viewer.item(1, col).setText(dna.NUTRIENTS[nid][2])
        self.nutcont_viewer.resizeColumnsToContents()


# -----------------------------------------------------------------------------
# Helper Functions ------------------------------------------------------------

def consecutive_dict(data_dict, start, end):
    """
    Return a dictionary with consecutive numeric keys in a specified range.

    Finds all keys in the data_dict arg that are within the numeric range
    specified by the start and end args (inclusive). Creates a new dictionary
    with the same number of keys as those found within the specified range,
    wherein the first key is the start arg and each additional key is the
    previous key's numeric value incremented by 1. These now-consecutive keys
    are mapped to the original values found in data_dict. The remaining
    key-value pairs outside of the specified range are then added to the new
    dict, unchanged.

    The keys in data_dict must be integers or integer strings of the same type
    as the start and end args, otherwise the returned dictionary may have
    inconsistent key-value pairs. If no keys are found within the specified
    range, or keys found within that range are already in order, the original
    data_dict is returned. If the start arg is not less than or equal to the
    end arg, or the keys are not integers or integer strings, None is returned.
    Currently, this function is used solely to reassign template inventory
    dictionary keys.

    :param data_dict: A dictionary with numeric keys
    :type data_dict: dict
    :param start: Minimum key in reassignment range
    :type start: int, str
    :param end: Maximum key in reassignment range
    :type end: int, str
    :return: Dictionary with reassigned keys, the original data_dict arg, or
        None if keys cannot be converted to integers
    :rtype: dict, None
    """
    try:
        # Return None if inconsistencies are found.
        if int(start) > int(end):
            return None
        if type(start) != type(end):
            return None
        # Find all keys in data_dict between and including start and end args.
        # Convert everything to ints for all comparisons--string comparisons
        # may return unwanted results (e.g. '100' < '20'). Collect out of range
        # keys in a separate list.
        inrange = []
        outrange = []
        start_int, end_int = int(start), int(end)
        for key in data_dict:
            int_key = int(key)
            if start_int <= int_key <= end_int:
                inrange.append(int_key)
            else:
                outrange.append(key)
        # Check if there are no inrange keys or if there is one key and its
        # int value is equal to the int-start value. If so, return data_dict.
        num_inrange = len(inrange)
        if num_inrange == 0 or (num_inrange == 1 and inrange[0] == start_int):
            return data_dict
        # Sort int-keys to find the correct order. Determine the expected last
        # int-key and check if it is equal to the last inrange int-key.
        inrange.sort()
        expected_last_int = inrange[0] + num_inrange - 1
        if inrange[0] == start_int and expected_last_int == inrange[-1]:
            return data_dict
        # Create a continuous range of new keys for the result dict, starting
        # with the int value of the start arg. Iterate over sorted inrange
        # int-keys, convert them back to strings if applicable, add them to
        # a result dict, and map the original values to them.
        consec_keys = range(start_int, start_int + num_inrange)
        result = {}
        for idx in range(num_inrange):
            if isinstance(start, str):
                new_key = str(consec_keys[idx])
                old_key = str(inrange[idx])
            else:
                new_key = consec_keys[idx]
                old_key = inrange[idx]
            result[new_key] = data_dict[old_key]
        # Update the result dict with out of range key-value pairs.
        for key in outrange:
            result[key] = data_dict[key]
        return result
    except (TypeError, ValueError):
        return None


def eval_fraction(string):
    """
    Return the float value of a valid fraction string or, if invalid, None.

    This function takes a string arg, verifies that it is a valid fraction, and
    returns the float value of that fraction or, if it is not a valid fraction,
    None. The returned value can be evaluated by the caller and handled
    accordingly. If None is returned, the string arg is not treated as a valid
    fraction by the caller, otherwise it is. A 'valid fraction' is considered
    to be a simple fraction of integers or floats that does not create black
    holes by trying to divide by zero.

    :param string: A string that might be a valid fraction
    :type string: str
    :return: True if the string is a valid fraction, otherwise False
    :rtype: bool, float
    """
    try:
        # Check for a forward slash character.
        if "/" not in string:
            return None
        # Split at the slash and check for one value on each side of it.
        split_string = string.split("/")
        if len(split_string) != 2:
            return None
        # Check that numerator and denominator can be converted to floats.
        num = float(split_string[0])
        den = float(split_string[1])
        return num / den
        # Return True if all checks have been passed.
    except (AttributeError, TypeError, ZeroDivisionError, ValueError):
        return None


def is_decimal(number):
    """
    Return True if a numeric value can be parsed as a float.

    This function takes a number arg that must be a float, int, or numeric
    string, confirms that a decimal place is present in the string value of the
    number arg, and then checks for at least one nonzero integer to the right
    of the decimal place. It returns True only if these conditions are met.
    Long numbers that are automatically converted to scientific notation format
    return True if the exponent is positive. If the number arg is not a float,
    int, or numeric string, an inaccurate result may be returned.

    :param number: A numeric value that might be parsed as a float
    :type number: float, int, str
    :return: True if the number has a decimal, else False
    :rtype: bool
    """
    try:
        # Convert the number arg to a string value for consistent analysis.
        num_string = str(number)
        # Check for scientific notation.
        if "e" in num_string:
            split_string = num_string.split("e")
            int(split_string[0])
            if int(split_string[1]) > 0:
                return False
            return True
        # Check for decimal.
        if "." not in num_string:
            return False
        # Split at the decimal and check for values to the right of it.
        split_string = num_string.split(".")
        if len(split_string) != 2:
            return False
        # Check for at least one non-zero value to the right of the decimal.
        if not split_string[1].count("0") < len(split_string[1]):
            return False
        # Check that both split strings can be converted to integers.
        if split_string[0] != "":
            int(split_string[0])
        int(split_string[1])
        # Return True if all checks have been passed.
        return True
    except ValueError:
        return False


def maxed_dicts(*data_dicts):
    """
    Maximize dictionary values with corresponding keys, return the merged dict.

    This function takes a data_dicts list arg that consists of one or more
    dictionaries whose values are floats or ints that can be compared to each
    other. Returns a merged dictionary wherein each key is mapped to the
    maximum of all constituent dict values mapped to that key. All dictionary
    keys must be of the same type to return a result dictionary with accurate
    values.

    :param data_dicts: Dictionaries to be merged
    :type data_dicts: list
    :return: A merged dictionary with keys mapped to maximum values from all
        constituent dictionaries in which those keys are found
    :rtype: dict
    """
    result = {}
    for dictionary in data_dicts:
        for key in dictionary:
            if key not in result:
                result[key] = dictionary[key]
            else:
                if dictionary[key] > result[key]:
                    result[key] = dictionary[key]
    return result


def max_key(data_dict, floor=None, ceiling=None):
    """
    Return the maximum key in a dict within a given key range.

    This function takes a data_dict arg with analogous keys (that should be
    of the same type and easily comparable to each other), finds all keys
    within a range designated by the floor and ceiling args, and returns the
    key with the highest relative value (note that 'value' does not refer to
    the value assigned to the key, but to the numeric or textual value of the
    key itself). The floor and ceiling args are included within the searchable
    range. Returns None if the data_dict is empty or a key is not found within
    the specified range. This functions works best when all keys are float, int
    or str type objects. Inaccurate results are returned when keys are
    numeric strings with different lengths (e.g. '100' < '20').

    :param data_dict: A dictionary with analogous key values
    :type data_dict: dict
    :param floor: Lowest key in search range or None
    :type floor: float, int, str, None
    :param ceiling: Highest key in search range or None
    :type ceiling: float, int, str, None
    """
    # Return None if the data_dict is empty and therefore no max key exists.
    if not data_dict:
        return None
    # Return None if floor is not less than or equal to ceiling.
    if floor > ceiling:
        return None
    max_found = None
    first_found = False
    if floor is None and ceiling is None:
        for key in data_dict:
            if first_found:
                max_found = max(key, max_found)
            else:
                max_found = key
                first_found = True
    elif ceiling is None:
        for key in data_dict:
            if first_found:
                max_found = max(key, max_found)
            else:
                if key >= floor:
                    max_found = key
                    first_found = True
    elif floor is None:
        for key in data_dict:
            if first_found:
                if ceiling >= key > max_found:
                    max_found = key
            else:
                if key <= ceiling:
                    max_found = key
                    first_found = True
    else:
        for key in data_dict:
            if first_found:
                if ceiling >= key > max_found:
                    max_found = key
            else:
                if floor <= key <= ceiling:
                    max_found = key
                    first_found = True
    return max_found


def min_key(data_dict, floor=None, ceiling=None):
    """
    Return the minimum key in a dict within a given key range.

    This function takes a data_dict arg with analogous keys (that should be
    of the same type and easily comparable to each other), finds all keys
    within a range designated by the floor and ceiling args, and returns the
    key with the lowest relative value (note that 'value' does not refer to
    the value assigned to the key, but to the numeric or textual value of the
    key itself). The floor and ceiling args are included within the searchable
    range. Returns None if the data_dict is empty or a key is not found within
    the specified range. This functions works best when all keys are float, int
    or str type objects. Inaccurate results are returned when keys are
    numeric strings with different lengths (e.g. '100' < '20').

    :param data_dict: A dictionary with analogous key values
    :type data_dict: dict
    :param floor: Lowest key in search range or None
    :type floor: float, int, str, None
    :param ceiling: Highest key in search range or None
    :type ceiling: float, int, str, None
    """
    # Return None if the data_dict is empty and therefore no min key exists.
    if not data_dict:
        return None
    # Return None if floor is not less than or equal to ceiling.
    if floor > ceiling:
        return None
    min_found = None
    first_found = False
    if floor is None and ceiling is None:
        for key in data_dict:
            if first_found:
                min_found = min(key, min_found)
            else:
                min_found = key
                first_found = True
    elif ceiling is None:
        for key in data_dict:
            if first_found:
                if floor <= key < min_found:
                    min_found = key
            else:
                if key >= floor:
                    min_found = key
                    first_found = True
    elif floor is None:
        for key in data_dict:
            if first_found:
                min_found = min(key, min_found)
            else:
                if key <= ceiling:
                    min_found = key
                    first_found = True
    else:
        for key in data_dict:
            if first_found:
                if floor <= key < min_found:
                    min_found = key
            else:
                if floor <= key <= ceiling:
                    min_found = key
                    first_found = True
    return min_found


def numeric_value(string, round_result=True, round_digits=3):
    """
    Return the numeric value of a string.

    Returns the numeric value of the string arg as an integer or a float
    rounded to three decimal places. If string does not have an equivalent
    numeric value, None is returned. This function's caller uniquely handles
    the string arg depending on what is returned. If the round_result arg is
    True, the returned result is rounded to the number of digits specified
    by the round_digits arg. The result is rounded to three decimal places
    by default if it is a decimal number.

    :param string: A string that may be numeric
    :type string: str
    :param round_result: True if the resulting float is rounded else False
    :type round_result: bool
    :param round_digits: Number of digits past decimal if result is rounded
    :type round_digits: int
    :return: Numeric value of the string as an integer or float rounded to
        three decimal places, or None if string is not a number
    :rtype: float, int, None
    """
    try:
        # Check if the string arg is evaluated as a fraction.
        frac_value = eval_fraction(string)
        string_value = string if frac_value is None else frac_value
        # Check if the fraction or non-fraction string is a decimal.
        if is_decimal(string_value):
            if round_result:
                rounded_value = round(float(string_value), round_digits)
                if is_decimal(rounded_value):
                    return rounded_value
                else:
                    return int(rounded_value)
            else:
                return float(string_value)
        else:
            return int(float(string_value))
    except (TypeError, ValueError):
        return None


def process_item_counts(user, ref_type, item_id, item_row, build_parent):
    """
    Return a data set indicating where an inventory item is used.

    Searches the user's Build Parent and applicable template and record
    inventories for all occurrences of the reference item specified by the
    item_id arg. The ref_type arg indicates which inventory is searched--'Food'
    items or 'Exercise' items. The item_row is the item's table row in the
    inventory. It is passed from the GUI's delete_item method to this function,
    and from here to its delete_reference method so that, if the item is
    deleted, the reloaded inventory can scroll down to item_row. The
    build_parent arg is the user's current Build Parent object or, if there is
    no Build Parent, None. The reference item's usage details are returned in a
    tuple with the format:

        (reference type, item ID, item row, in-buildparent bool, record count,
         template counts dict)

    The first three elements are the rec_type, item_id, and item_row args
    returned to the GUI so that the reference counts can be properly handled.
    The in-buildparent bool is True if the item is in the current Build Parent,
    otherwise it is False. The record count is the number of records in which
    the item is referenced. The template counts dict is a dictionary with
    nutrition or fitness template class IDs, each mapped to the number of
    corresponding templates in which the item is referenced.

    :param user: The current user's User object
    :type user: User
    :param ref_type: Reference item type: 'Food' or 'Exercise'
    :type ref_type: str
    :param item_id: Reference item ID
    :type item_id: str
    :param item_row: The Inventory Viewer table row in which the item is found
    :type item_row: int
    :param build_parent: The current Build Parent object
    :type build_parent: Recipe, Meal, Diet, Workout, Cycle, Program
    :return: Item count details in the format: (reference type, item ID, item
        row, in-buildparent bool, record count, template counts dict)
    :rtype: tuple
    """
    cids = ["R", "M", "D"] if ref_type == "Food" else ["W", "C", "P"]
    count_method = "unique_" + ref_type.lower() + "s"
    record_objects = user.record_objects(cids[2]).values()
    template_objects = {
        cid: user.template_objects(cid).values() for cid in cids}
    rec_count = 0
    tem_counts = {cid: 0 for cid in cids}
    # Find item ID count in all records.
    for record in record_objects:
        if item_id in getattr(record, count_method)():
            rec_count += 1
    # Find item ID count in all templates.
    for cid in tem_counts:
        for template in template_objects[cid]:
            if item_id in getattr(template, count_method)():
                tem_counts[cid] += 1
    # Find item ID in Build Parent.
    in_buildparent = False
    if build_parent is not None and build_parent.cid() in cids:
        if item_id in getattr(build_parent, count_method)():
            in_buildparent = True
    return ref_type, item_id, item_row, in_buildparent, rec_count, tem_counts


def summed_dicts(*data_dicts):
    """
    Sum dictionary values with corresponding keys and return the merged dict.

    This function takes a data_dicts list arg that consists of one or more
    dictionaries whose values are floats or ints that can be added to each
    other. Returns a merged dictionary wherein each key is mapped to the sum
    of all constituent dict values mapped to that key. An empty dictionary is
    returned if the values of shared keys cannot be added to each other.

    :param data_dicts: Dictionaries to be merged
    :type data_dicts: list
    :return: A merged dictionary with keys mapped to summed values from all
        constituent dictionaries in which those keys are found
    :rtype: dict
    """
    try:
        result = {}
        for dictionary in data_dicts:
            for key in dictionary:
                if key not in result:
                    result[key] = 0
                result[key] += dictionary[key]
        return result
    except (TypeError, ValueError):
        return {}


def unique_keys(data_dict, depth):
    """
    Return unique keys at a given depth within nested dictionaries.

    This function takes a data_dict arg, which is a dictionary with nested
    dictionaries, and returns a sorted list of all unique keys found in all
    nested dicts located at the layer specified by the depth arg. Recursive
    calls are made to this functions for all nested dicts until the depth arg
    is zero, at which point the keys method is called on the current data_dict
    arg and this list of keys is sorted and returned. If the object at the
    specified depth is not a dict, an empty list is returned. All dict keys
    at the specified depth must be strings, otherwise an empty list is
    returned. This restriction is necessary to sort keys in a preferable manner
    when upper-, lower-, and mixed-case string characters are found. As this
    function is only used to search dicts with str type keys, this restriction
    is tolerable.

    :param data_dict: A dictionary with nested dictionaries, the keys of which
         are all strings
    :type data_dict: dict
    :param depth: Depth at which to return all unique dict keys
    :type depth: int
    :return: A list of unique dictionary keys at a given depth, or an empty
        list if no keys are found
    :rtype: list
    """
    try:
        # Base: return an empty list if data_dict arg is not a dict object.
        if not isinstance(data_dict, dict):
            return []
        # Base: return data_dict keys when layer is at zero.
        if depth == 0:
            return sorted(data_dict.keys(), key=lambda string: string.lower())
        # Recursively step through data_dict.
        all_keys = []
        for nested_dict in data_dict.values():
            all_keys.extend(unique_keys(nested_dict, depth - 1))
        # Return sorted list of unique keys.
        return sorted(list(set(all_keys)), key=lambda string: string.lower())
    except AttributeError:
        return []

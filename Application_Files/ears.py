#!/usr/bin/env python2.7
"""
This module contains classes to prompt the user for data inputs.
----------
These classes display interactive dialogs which prompt the user to enter
profile data, select a Build Parent, edit build element properties, enter
edit reference items, and update app and user settings. Some dialogs directly
modify the objects passed to their constructors. All nutrients and focus
muscles, regardless of the user's settings, are displayed as options in the
applicable dialogs fields.
----------
Fonts: fonts used by this module's classes.
    FONT_ACTION: QFont object for action buttons
    FONT SELECTION: QFont object for selection buttons
    FONT_TAG: QFont object for field description tags
    FONT_HEADER: QFont object for dialog section headers

Profile Classes: classes to input user profile data.
    InputEntry: EasyDialog subclass to create a Health Diary entry
    InputTargets: EasyDialog subclass to create Nutrient Guide targets

Build Viewer Classes: classes to input build element properties.
    InputBuildParent: EasyDialog subclass to create a Build Parent
    InputBuildElement: EasyDialog subclass to edit a build element
    InputIngredient: EasyDialog subclass to edit an Ingredient's Quantities
    InputActivity: EasyDialog subclass to edit an Activity's Sessions

Inventory Manager Classes: classes to input reference item properties.
    InputFood: EasyDialog subclass to edit a Food reference item
    InputExercise: EasyDialog subclass to edit an Exercise reference item

Settings Class: class to input app and user settings.
    InputSettings: EasyDialog subclass to edit app and user settings
"""


import datetime

from PyQt4 import QtCore
from PyQt4 import QtGui

import album
import body
import dna
import organs


# -----------------------------------------------------------------------------
# Fonts -----------------------------------------------------------------------

FONT_ACTION = FONT_SELECTION = FONT_TAG = organs.arial_small
FONT_HEADER = organs.tahoma_medium


# -----------------------------------------------------------------------------
# Profile Classes -------------------------------------------------------------

# noinspection PyUnusedLocal
class InputEntry(organs.EasyDialog):
    """
    Class to create a Health Diary entry.

    InputEntry presents a dialog to the user with input fields for a new Health
    Diary entry. These fields are:

        Entry Date: A date from 2000-01-01 onward
        Metric Table: A table with all existing health metrics and a column in
            which to enter a numeric measurement value for each one
        New Metric: A new health metric between 1-40 characters

    InputEntry inherits all attributes and methods from its superclass. Its
    constructor is passed the parent GUI and the user's User object to build a
    dialog specific to the current user. It implements an entry attribute to
    store the completed entry in the format:

        {entry date: {health metric: input value, ...}}

    This entry attribute can be passed to the user's add_entry method to add it
    to the user's Health Diary. It has the entry date as a key mapped to a
    measurements dict. The measurements dict has as its keys all health metric
    strings mapped to the numeric values entered by the user. The existing
    Health Diary entry dates and health metrics are stored in the attributes
    existing_entry_dates and metrics.

    The inherited accept method is overridden to check that a value is entered
    for at least one metric, check that all values are valid numbers, prompt
    the user to confirm that an entry is to be overwritten if the input entry
    date exists in the Health Diary, build the entry dict and assign it to the
    entry attribute, and accept the dialog. A slot method is implemented to add
    a new health metric to the Metric Table.
    """

    def __init__(self, parent, user):
        """
        Initialize an InputEntry object.

        Assigns an empty dict to the entry attribute, a list of the user's
        Health Diary entry dates to the existing_entry_dates attribute, and a
        list of the user's existing health metrics to the metrics attribute. If
        no metrics exist, the default metric string 'Weight (lb)' is appended
        to the metrics list. Builds the dialog components and connects input
        field signals to slot methods.

        :param parent: Parent QMainWindow
        :type parent: QMainWindow
        :param user: The current user's User object
        :type user: User
        """
        organs.EasyDialog.__init__(self, parent)
        self.entry = {}
        self.existing_entry_dates = user.health_diary().keys()
        if self.existing_entry_dates:
            self.metrics = organs.unique_keys(user.health_diary(), 1)
        else:
            self.metrics = ["Weight (lb)"]
        # Window properties, button box, and outline frame.
        self.setWindowTitle("Health Diary Entry")
        self.setWindowIcon(organs.EasyIcon(dna.ICONS["diary"]))
        width, height = 660, 352
        self.setFixedSize(width, height)
        self.button_box = organs.EasyButtonBox(self)
        outline = organs.OutlineFrame(self, [5, 4, width - 9, 294])
        # Entry Date section.
        header_text = "".join([
            "ENTRY: Choose an entry date and enter health metric ",
            "measurements in the Value column."])
        header = organs.EasyLabel(
            self, [10, 4, width - 20, 26], text=header_text, font=FONT_HEADER,
            alignment=QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        date_tag = organs.EasyLabel(
            self, [10, 30, 84, 26], text="Entry Date:", font=FONT_TAG,
            alignment=QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        now = datetime.datetime.now()
        self.date_field = organs.EasyDateEdit(
            self, [94, 30, 100, 22], display_format="yyyy-MM-dd",
            date=[now.year, now.month, now.day], calendar_on=True)
        # Metric Table section.
        self.met_table = organs.EasyTableWidget(
            self, [10, 56, 400, 234], dims=[2, len(self.metrics)],
            column_labels=["Health Metric", "Value"], column_widths=[274, 102],
            row_height=22, row_header_hidden=True, stretch_last_section=True)
        for metric in self.metrics:
            row = self.metrics.index(metric)
            metric_item = self.met_table.item(row, 0)
            metric_item.setText(metric)
            # Prevent metric cell from being edited by the user and set its
            # text color to black (default for non-selectable is dim gray).
            metric_item.setFlags(QtCore.Qt.ItemIsSelectable)
            metric_item.setTextColor(QtGui.QColor(0, 0, 0))
            value_item = self.met_table.item(row, 1)
            value_item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.met_table.setCurrentCell(0, 1)
        self.met_table.edit(self.met_table.currentIndex())
        # New Metric section.
        new_metric_tag = organs.EasyLabel(
            self, [420, 56, 224, 26], text="New Health Metric", font=FONT_TAG)
        self.new_metric_field = organs.EasyLineEdit(
            self, [420, 78, 224, 22], max_length=40)
        self.add_metric_bn = organs.EasyToolButton(
            self, [420, 106, 224, 24], text="Add Metric", font=FONT_ACTION,
            button_type="action")
        # Tip box section.
        tip_text = "".join([
            "-" * 10, "TIPS", "-" * 10, "\n\n",
            "",
            "A health metric name can be up to 40 characters long.\n\n",
            "",
            "When entering the name of a new health metric, if it is not ",
            "clear by the name how that metric is measured, you should ",
            "include its measurement unit in parentheses.\n\n",
            "",
            "Example: 'Heart Rate (bpm)'"])
        tipbox = organs.TipBox(self, [420, 140, 224, 150], text=tip_text)
        # Connect signals to slots.
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)
        self.add_metric_bn.clicked.connect(self.add_metric)

    def accept(self):
        """Check for valid inputs and accept the dialog."""
        try:
            # Set focus on button box so that the input in the currently
            # selected field can be locked in prior to accepting the dialog.
            self.button_box.setFocus()
            measurements = {}
            # Convert date field QDate to datetime string. Note that result is
            # same as using date.strftime("%Y-%m-%d") and str(datetime.date).
            date_string = self.date_field.date().toPyDate().isoformat()
            # Collect all inputs from Metric Table. Skip any blank values.
            for row in range(self.met_table.rowCount()):
                val_text = str(self.met_table.item(row, 1).text()).strip()
                if val_text == "":
                    continue
                metric = str(self.metrics[row])
                # Eval value text. Do not round. Check for non-numeric value.
                value = organs.numeric_value(val_text, False)
                if value is None:
                    raise ValueError
                measurements[metric] = value
            # Check for at least one measurement input.
            if not measurements:
                QtGui.QMessageBox.warning(
                    self, "Missing Measurement",
                    "You must enter at least one health metric measurement!")
                return
            # Check for Entry Date existing in Health Diary.
            if date_string in self.existing_entry_dates:
                choice = QtGui.QMessageBox.warning(
                    self, "Confirm Overwrite Entry",
                    "Do you want to replace the existing entry for:\n\n" +
                    date_string, QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
                if choice == QtGui.QMessageBox.No:
                    return
            # Assign entry dict to entry attribute and accept the dialog.
            self.entry = {date_string: measurements}
            QtGui.QDialog.accept(self)
        except ValueError:
            QtGui.QMessageBox.warning(
                self, "Invalid Measurement(s)",
                "All measurements must be numeric values!")

    def add_metric(self):
        """Add a new health metric to the Metric Table."""
        new_metric_string = str(self.new_metric_field.text()).strip()
        # Check for a New Metric input.
        if new_metric_string == "":
            QtGui.QMessageBox.warning(
                self, "Missing Metric Name",
                "You must enter the name of the new health metric!")
            self.new_metric_field.setFocus()
            return
        # Check if New Metric already exists (convert all to lowercase).
        if new_metric_string.lower() in [met.lower() for met in self.metrics]:
            QtGui.QMessageBox.warning(
                self, "Existing Metric", "This health metric already exists!")
            self.new_metric_field.setFocus()
            self.new_metric_field.selectAll()
            return
        # Add new metric to metrics list and update Metric Table.
        self.metrics.append(new_metric_string)
        row_count = self.met_table.rowCount()
        self.met_table.setRowCount(row_count + 1)
        new_metric_item = QtGui.QTableWidgetItem()
        new_metric_item.setText(new_metric_string)
        new_metric_item.setFlags(QtCore.Qt.ItemIsSelectable)
        new_metric_item.setTextColor(QtGui.QColor(0, 0, 0))
        self.met_table.setItem(row_count, 0, new_metric_item)
        value_item = QtGui.QTableWidgetItem()
        value_item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.met_table.setItem(row_count, 1, value_item)
        # Scroll to new metric in Metric Table and clear New Metric field.
        self.new_metric_field.clear()
        self.met_table.scrollToItem(
            value_item, QtGui.QAbstractItemView.PositionAtTop)
        self.met_table.setCurrentCell(row_count, 1)
        self.met_table.edit(self.met_table.currentIndex())


# noinspection PyUnusedLocal
class InputTargets(organs.EasyDialog):
    """
    Class to create Nutrient Guide targets.

    InputTargets presents a dialog to the user with input fields for new
    Nutrient Guide targets. These fields are:

        Effective Date: A date from 2000-01-01 onward
        Target Table: A table with all nutrients and a column in which to enter
            numeric targets for each one

    InputTargets inherits all attributes and methods from its superclass. Its
    constructor is passed the parent GUI and the user's User object to build a
    dialog which displays all nutrients in a Target Table. The user can enter
    one or more nutrient targets in the table. The class implements a targets
    attribute to store the completed targets in the format:

        {effective date: {nutrient ID: input value, ...}}

    This targets attribute can be passed to the user's add_targets method to
    add it to the user's Nutrient Guide. It has the effective date as a key
    mapped to a target nutrient values dict. That dict has as its keys all
    nutrient IDs for which the user has input target values mapped to those
    numeric values. The existing Nutrient Guide effective dates are stored in
    the existing_effective_dates attribute. Target values for the latest date,
    if the Nutrient Guide is not empty, are populated into the Target Table
    when the dialog is constructed. This allows the user to review the most
    recent targets and reuse any that still apply.

    The inherited accept method is overwritten to check that a target is
    entered for at least one nutrient, check that all values are valid numbers,
    prompt the user to confirm that targets are to be overwritten if the input
    effective date exists in the Nutrient Guide, build the targets dict and
    assign it to the targets attribute, and accept the dialog. Slot methods are
    implemented to clear all nutrient values and populate the table with the
    recommended daily value for all applicable nutrients.
    """

    def __init__(self, parent, user):
        """
        Initialize an InputTargets object.

        Assigns an empty dict to the targets attribute and a list of the user's
        Nutrient Guide effective dates to the existing_effective_dates
        attribute. Builds the dialog components and connects input field
        signals to slot methods.

        :param parent: Parent QMainWindow
        :type parent: QMainWindow
        :param user: The current user's User object
        :type user: User
        """
        organs.EasyDialog.__init__(self, parent)
        self.targets = {}
        self.existing_effective_dates = user.nutrient_guide().keys()
        latest_date = organs.max_key(user.nutrient_guide())
        if latest_date is not None:
            latest_targets = user.nutrient_guide()[latest_date]
        else:
            latest_targets = {}
        # Window properties, button box, and outline frame.
        self.setWindowTitle("Nutrient Guide Targets")
        self.setWindowIcon(organs.EasyIcon(dna.ICONS["guide"]))
        width, height = 440, 630
        self.setFixedSize(width, height)
        self.button_box = organs.EasyButtonBox(self)
        outline = organs.OutlineFrame(self, [5, 4, width - 9, 572])
        # Effective Date section.
        header_text = "".join([
            "TARGETS: Enter targets and the date they go into effect."])
        header = organs.EasyLabel(
            self, [10, 4, width - 20, 26], text=header_text, font=FONT_HEADER,
            alignment=QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        date_tag = organs.EasyLabel(
            self, [20, 30, 110, 26], text="Effective Date:", font=FONT_TAG)
        now = datetime.datetime.now()
        self.date_field = organs.EasyDateEdit(
            self, [130, 30, 100, 22], display_format="yyyy-MM-dd",
            date=[now.year, now.month, now.day], calendar_on=True)
        # Target Table section.
        nut_names = [dna.NUTRIENTS[nid][0] for nid in dna.GUI_NUTRIENTS]
        self.tar_table = organs.EasyTableWidget(
            self, [20, 56, 400, 484], dims=[2, len(dna.GUI_NUTRIENTS)],
            center_text=True, column_labels=["Value", "Unit"],
            column_widths=[100, 66], row_labels=nut_names, row_height=28,
            row_header_width=210, resize_off=True, single_selection=True,
            stretch_last_section=True)
        for nid in dna.GUI_NUTRIENTS:
            row = dna.GUI_NUTRIENTS.index(nid)
            value_item = self.tar_table.item(row, 0)
            # Convert any floats to two decimals to save space.
            if nid in latest_targets:
                value_item.setText(str(latest_targets[nid]))
            # Add unit drop-down if nutrient has recommended daily value.
            if nid in dna.FDA_RDV:
                unit_drop = QtGui.QComboBox(self)
                unit_drop.addItem(dna.NUTRIENTS[nid][2])
                unit_drop.addItem("% DV")
                self.tar_table.setCellWidget(row, 1, unit_drop)
            else:
                unit_item = self.tar_table.item(row, 1)
                unit_item.setText(dna.NUTRIENTS[nid][2])
                # Set text color to black, as it will dim when not selectable.
                unit_item.setFlags(QtCore.Qt.ItemIsSelectable)
                unit_item.setTextColor(QtGui.QColor(0, 0, 0))
        self.tar_table.setCurrentCell(0, 0)
        self.tar_table.edit(self.tar_table.currentIndex())
        self.use_recommended_bn = organs.EasyToolButton(
            self, [20, 546, 198, 22], text="Use Recommended DVs",
            font=FONT_ACTION, button_type="action",
            tool_tip="Fill table with FDA recommended daily values")
        self.clear_all_bn = organs.EasyToolButton(
            self, [222, 546, 198, 22], text="Clear All Values",
            font=FONT_ACTION, button_type="action")
        # Connect signals to slots.
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)
        self.use_recommended_bn.clicked.connect(self.use_recommended)
        self.clear_all_bn.clicked.connect(self.clear_all)

    def accept(self):
        """Check for valid inputs and accept the dialog."""
        try:
            # Set focus on button box so that the input on the currently
            # selected field can be locked in prior to accepting the dialog.
            self.button_box.setFocus()
            nutrient_values = {}
            # Convert date field QDate to datetime string.
            date_string = self.date_field.date().toPyDate().isoformat()
            # Collect all nutrient target inputs from Target Table. Skip any
            # nutrients with no targets entered.
            for row in range(self.tar_table.rowCount()):
                val_text = str(self.tar_table.item(row, 0).text()).strip()
                if val_text == "":
                    continue
                value = float(val_text)
                nid = dna.GUI_NUTRIENTS[row]
                # Determine if unit is '% DV' and adjust value accordingly.
                if nid in dna.FDA_RDV:
                    unit = str(self.tar_table.cellWidget(row, 1).currentText())
                    if unit == "% DV":
                        rdv_val = dna.FDA_RDV[nid][0]
                        value = (value / 100.0) * rdv_val
                # Eval final value, rounding to 3 decimal places.
                final_value = organs.numeric_value(value)
                # Check that the nutrient target is greater than zero.
                if final_value <= 0:
                    QtGui.QMessageBox.warning(
                        self, "Invalid Target", "The target for " +
                        dna.NUTRIENTS[nid][0] + " was calculated to be " +
                        "less than zero! Targets are rounded to three " +
                        "decimal places. Enter a higher target value or " +
                        "leave that nutrient blank.")
                    return
                nutrient_values[nid] = final_value
            # Check for at least one nutrient target input.
            if not nutrient_values:
                QtGui.QMessageBox.warning(
                    self, "Missing Target",
                    "You must enter at least one nutrient target to save!")
                return
            # Check for Effective Date existing in Nutrient Guide.
            if date_string in self.existing_effective_dates:
                choice = QtGui.QMessageBox.warning(
                    self, "Confirm Overwrite Targets",
                    "Do you want to replace existing targets for " +
                    "the effective date:\n\n" + date_string,
                    QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
                if choice == QtGui.QMessageBox.No:
                    return
            # Assign targets dict to targets attribute and accept the dialog.
            self.targets = {date_string: nutrient_values}
            QtGui.QDialog.accept(self)
        except ValueError:
            QtGui.QMessageBox.warning(
                self, "Invalid Target(s)",
                "All nutrient targets must be numeric values!")

    def use_recommended(self):
        """Populate the Target Table with FDA recommended daily values."""
        empty_table = True
        for row in range(self.tar_table.rowCount()):
            if str(self.tar_table.item(row, 0).text()) != "":
                empty_table = False
                break
        if not empty_table:
            choice = QtGui.QMessageBox.warning(
                self, "Confirm Replace Targets", "Do you want to replace " +
                "all applicable nutrient targets with FDA recommended " +
                "daily values?", QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
            if choice == QtGui.QMessageBox.No:
                return
        for nid in dna.GUI_NUTRIENTS:
            if nid in dna.FDA_RDV:
                row = dna.GUI_NUTRIENTS.index(nid)
                recommended_daily_value = str(dna.FDA_RDV[nid][0])
                self.tar_table.item(row, 0).setText(recommended_daily_value)
                self.tar_table.cellWidget(row, 1).setCurrentIndex(0)

    def clear_all(self):
        """Clear all nutrient targets from the Target Table."""
        empty_table = True
        for row in range(self.tar_table.rowCount()):
            if str(self.tar_table.item(row, 0).text()) != "":
                empty_table = False
                break
        if empty_table:
            return
        choice = QtGui.QMessageBox.warning(
            self, "Confirm Clear Targets", "Do you want to clear all targets?",
            QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
        if choice == QtGui.QMessageBox.No:
            return
        for row in range(self.tar_table.rowCount()):
            self.tar_table.item(row, 0).setText("")
            if dna.GUI_NUTRIENTS[row] in dna.FDA_RDV:
                self.tar_table.cellWidget(row, 1).setCurrentIndex(0)


# -----------------------------------------------------------------------------
# Build Manager Classes -------------------------------------------------------

# noinspection PyUnusedLocal
class InputBuildParent(organs.EasyDialog):
    """
    Class to create a Build Parent.

    InputBuildParent presents a dialog to the user with selection buttons for
    a new Build Parent to load into the Build Viewer. The Build Parent options
    are Recipe, Meal, Diet, Workout, Cycle, and Program objects. This class
    inherits all attributes and methods from its superclass. Its constructor is
    passed the parent GUI to build a dialog which displays six buttons in a
    grid, one for each option.

    It implements a build_parent attribute to store the Build Parent object
    created from the user's selection. This attribute is assigned to the GUI's
    buildparent attribute, which is set as the top level item in the Build
    Viewer QTreeWidget. The inherited accept method is overridden to
    instantiate the selected build element class and accept the dialog.
    """

    def __init__(self, parent):
        """
        Initialize an InputBuild object.

        Assign None to the parent_element attribute, an empty list to the
        parent_buttons attribute, and a list of the class IDs for the six
        build element choices to the parent_cids attribute. Builds the dialog
        components and connects input field signals to slot methods.

        :param parent: Parent QMainWindow
        :type parent: QMainWindow
        """
        organs.EasyDialog.__init__(self, parent)
        self.build_parent = None
        self.parent_buttons = []
        self.parent_cids = ["R", "M", "D", "W", "C", "P"]
        # Window properties, button box, and outline frame.
        self.setWindowTitle("Create New Build")
        self.setWindowIcon(organs.EasyIcon(dna.ICONS["createnew"]))
        width, height = 300, 204
        self.setFixedSize(width, height)
        self.button_box = QtGui.QDialogButtonBox(self)
        self.button_box.setGeometry((width / 2) - 100, height - 40, 200, 28)
        self.button_box.setStandardButtons(QtGui.QDialogButtonBox.Cancel)
        self.button_box.setCenterButtons(True)
        self.button_box.rejected.connect(self.reject)
        outline = organs.OutlineFrame(self, [5, 4, width - 9, 146])
        # Parent Element section.
        header = organs.EasyLabel(
            self, [10, 4, 280, 26], text="Select a build type to create.",
            font=FONT_HEADER)
        button_frame = organs.EasyFrame(self, [10, 30, 280, 112])
        for cid in self.parent_cids:
            idx = self.parent_cids.index(cid)
            if idx < 3:
                xpos, ypos_adjuster = 0, 0
            else:
                xpos, ypos_adjuster = 142, 3
            button = organs.EasyToolButton(
                button_frame, [xpos, (idx - ypos_adjuster) * 38, 138, 36],
                text=dna.BUILD_ELEMENTS[cid][0], font=FONT_SELECTION,
                button_type="selection")
            button.clicked.connect(self.accept)
            self.parent_buttons.append(button)

    def accept(self):
        """Create Build Parent and accept the dialog."""
        for button in self.parent_buttons:
            if button.isChecked():
                idx = self.parent_buttons.index(button)
                cid = self.parent_cids[idx]
                self.build_parent = body.build_element(cid)
                break
        QtGui.QDialog.accept(self)


# noinspection PyUnusedLocal
class InputBuildElement(organs.EasyDialog):
    """
    Class to edit build element properties.

    InputBuildElement presents a dialog to the user with input fields for a
    build element's properties. Some fields are specific to certain build
    elements. These fields are:

    --All Elements--
        Description: A description between 1-200 characters
    --Recipe--
        Portion Consumed: Numeric amount of the Recipe that the user consumed
        Portion Prepared: Numeric amount of the Recipe that the user prepared
        Portion Unit: An associated unit of measure between 1-40 characters
    --Meal--
        Time: A time in 24-hour clock time
    --Diet--
        Date: A date from 2000-01-01 onward
    --Workout--
        Period Began: A datetime from 2000-01-01 00:00 onward
        Period Ended: A datetime from 2000-01-01 00:00 onward
    --Program--
        Start: A date from 2000-01-01 onward

    InputBuildElement inherits all attributes and methods from its superclass.
    Its constructor is passed the parent GUI, a build element, and, optionally,
    bools indicating that the build element is an inventory item and in the
    user's corresponding favorites list. It builds a dialog specific to the
    build element type passed to it and populates input fields with existing
    property values. It implements a buildelement attribute to store the
    build_element arg, a cid attribute to store its class ID, and an isfavorite
    attribute to store the build element's status as a favorite item.

    The inherited accept method is overridden to check that all input field
    values are valid, call the applicable build element methods to directly
    update its attributes, and accept the dialog. Methods are implemented to
    check for valid Recipe portion components and Workout period datetimes,
    and slot methods are implemented to update 12-hour clock time tags and
    toggle the Favorites Button icon.
    """

    def __init__(
            self, parent, build_element, is_item=False, is_favorite=False):
        """
        Initialize an InputBuildElement object.

        Assigns the build_element arg to the buildelement attribute. Builds the
        dialog components and connects input field signals to slot methods. If
        the is_item arg is True, a Favorites button is added to the dialog
        added to the dialog. If the is_favorite arg is True, the button is
        updated to reflect that.

        :param parent: Parent QMainWindow
        :type parent: QMainWindow
        :param build_element: A build element object
        :type build_element: Recipe, Meal, Diet, Workout, Cycle, Program
        :param is_item: True if build element is an inventory item, else False
        :type is_item: bool
        :param is_favorite: True if build element is a favorite, else False
        :type is_favorite: bool
        """
        organs.EasyDialog.__init__(self, parent)
        self.buildelement = build_element
        self.cid = build_element.cid()
        self.isfavorite = is_favorite
        # Window properties, button box, and outline frames.
        self.setWindowTitle(dna.BUILD_ELEMENTS[self.cid][0] + " Properties")
        if self.cid in dna.NUTRITION_BUILD_ELEMENTS:
            self.setWindowIcon(organs.EasyIcon(dna.ICONS["nutrition"]))
        else:
            self.setWindowIcon(organs.EasyIcon(dna.ICONS["fitness"]))
        width, height = 600, 310
        self.setFixedSize(width, height)
        self.button_box = organs.EasyButtonBox(self)
        outline_a = organs.OutlineFrame(self, [5, 4, width - 9, 56])
        outline_b = organs.OutlineFrame(self, [5, 70, width - 9, 78])
        # Description section (all elements).
        des_text = "".join([
            "DESCRIPTION: Enter a unique description up to 200 characters ",
            "long."])
        description_header = organs.EasyLabel(
            self, [10, 4, 580, 26], text=des_text, font=FONT_HEADER,
            alignment=QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.description_field = organs.EasyLineEdit(
            self, [10, 30, 580, 22], text=build_element.description(),
            max_length=200)
        # Favorite button. Connect button to slot method.
        if is_item:
            self.description_field.resize(520, 22)
            fav_icon = "heart_black" if is_favorite else "heart"
            self.favorite_bn = organs.EasyToolButton(
                self, [546, 10, 42, 42], icon_name=fav_icon,
                icon_size=[40, 40], button_type="selection")
            self.favorite_bn.clicked.connect(self.toggle_favorite)
        # Property stack widget with a page for each build element type.
        self.property_stack = QtGui.QStackedWidget(self)
        self.property_stack.setGeometry(10, 70, 580, 80)
        pages = []
        for _ in range(6):
            page = QtGui.QWidget()
            pages.append(page)
            self.property_stack.addWidget(page)
        # Blank Page section.
        blank_tag = organs.EasyLabel(
            pages[0], [10, 24, 580, 26], font=FONT_TAG,
            text="This build element has no additional attributes.")
        tip_text = "".join([
            "-" * 10, "TIPS", "-" * 10, "\n\n",
            "",
            "A unique description makes this build element easy to identify ",
            "in the Build Viewer--and even easier to find with the Inventory ",
            "Manager if saved as a template."])
        # Recipe Page section.
        if self.cid == "R":
            rec_text = "".join([
                "PORTION: Enter the portion size components of your Recipe."])
            recipe_header = organs.EasyLabel(
                pages[1], [0, 0, 580, 26], text=rec_text, font=FONT_HEADER,
                alignment=QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
            consumed_tag = organs.EasyLabel(
                pages[1], [10, 26, 140, 26], text="Consumed Amount",
                font=FONT_TAG)
            prepared_tag = organs.EasyLabel(
                pages[1], [180, 26, 140, 26], text="Prepared Amount",
                font=FONT_TAG)
            unit_tag = organs.EasyLabel(
                pages[1], [390, 26, 140, 26], text="Portion Unit",
                font=FONT_TAG)
            self.consumed_field = organs.EasyLineEdit(
                pages[1], [30, 48, 100, 22],
                text=str(build_element.consumed()))
            self.prepared_field = organs.EasyLineEdit(
                pages[1], [200, 48, 100, 22],
                text=str(build_element.prepared()))
            self.unit_field = organs.EasyLineEdit(
                pages[1], [370, 48, 180, 22], text=build_element.unit(),
                max_length=40)
            tip_text = "".join([
                "-" * 10, "TIPS", "-" * 10, "\n\n",
                "",
                "The consumed amount is how much of the Recipe you ate. ",
                "The prepared amount is how much of the Recipe you prepared. ",
                "The portion unit is the unit of measure associated with ",
                "both amounts.\n\n",
                "",
                "Example: You consumed 2 of 16 prepared 'pieces' of a ",
                "Recipe\n\n",
                "",
                "If consumed > prepared, this Recipe's nutrient content ",
                "will be calculated accordingly. For example, if you ",
                "consumed 20 of 10 prepared pieces, nutrient values are ",
                "calculated for the entire Recipe and then multiplied ",
                "by 20/10, evaluating to two times the total Recipe.\n\n",
                "",
                "A unique description makes this build element easy to ",
                "identify in the Build Viewer--and even easier to find with ",
                "the Inventory Manager if saved as a template."])
        # Meal Page section. Connect Time Field change to slot method that
        # updates the 12-hour clock time tag.
        if self.cid == "M":
            meal_txt = "".join([
                "TIME: Enter the time you ate this Meal in the format ",
                "'hour:minute'."])
            meal_header = organs.EasyLabel(
                pages[2], [0, 0, 580, 26], text=meal_txt, font=FONT_HEADER,
                alignment=QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
            time = build_element.time()
            self.time_field = organs.EasyTimeEdit(
                pages[2], [200, 48, 80, 22], display_format="hh:mm",
                time=[time.hour, time.minute])
            self.time_field.timeChanged.connect(self.update_time_tag)
            self.time_tag = organs.EasyLabel(
                pages[2], [300, 46, 80, 26], text=time.strftime("%I:%M %p"),
                font=FONT_TAG,
                alignment=QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
            tip_text = "".join([
                "-" * 10, "TIPS", "-" * 10, "\n\n",
                "",
                "The time entered for this Meal will be assumed to have ",
                "occurred on the date specified by its parent Diet. If your ",
                "Meal was eaten past midnight, in the wee hours of the ",
                "morning, be sure that it is a part of a Diet with the ",
                "applicable date.\n\n",
                "",
                "You must enter the time in 24-hour clock time, from 00:00 ",
                "(12:00 AM) to 23:59 (11:59 PM). In 24-hour clock time, ",
                "hours from 1:00 AM to 12:00 PM are unchanged, and hours ",
                "from 1:00 PM to 11:00 PM are converted by adding 12 to ",
                "them. 9:45 PM is 21:45 in 24-hour time.\n\n",
                "",
                "If you do not want to track Meal times, you can leave the ",
                "default value 12:00 AM in the input field; however, this ",
                "will prevent you from accurately tracking Meal times using ",
                "the Data Plotter tool.\n\n",
                "",
                "A unique description makes this build element easy to ",
                "identify in the Build Viewer--and even easier to find with ",
                "the Inventory Manager if saved as a template."])
        # Diet Page section.
        if self.cid == "D":
            diet_txt = "".join([
                "DATE: Enter the date you ate this Diet in the format ",
                "'year-month-day'."])
            diet_header = organs.EasyLabel(
                pages[3], [0, 0, 580, 26], text=diet_txt, font=FONT_HEADER,
                alignment=QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
            date = build_element.date()
            self.date_field = organs.EasyDateEdit(
                pages[3], [240, 48, 100, 22], display_format="yyyy-MM-dd",
                calendar_on=True, date=[date.year, date.month, date.day])
            tip_text = "".join([
                "-" * 10, "TIPS", "-" * 10, "\n\n",
                "",
                "You can also enter a date by clicking on the small arrow ",
                "next to the date input field to open up a calendar tool. ",
                "Use this tool to find a date, then click on it to enter it ",
                "into the input field.\n\n",
                "",
                "A unique description makes this build element easy to ",
                "identify in the Build Viewer--and even easier to find with ",
                "the Inventory Manager if saved as a template."])
        # Workout Page section.
        if self.cid == "W":
            wor_text = "".join([
                "PERIOD: Enter your Workout period in the format ",
                "'year-month-day hour:minute'."])
            workout_header = organs.EasyLabel(
                pages[4], [0, 0, 580, 26], text=wor_text, font=FONT_HEADER,
                alignment=QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
            began_tag = organs.EasyLabel(
                pages[4], [100, 26, 150, 26], text="Began At", font=FONT_TAG)
            ended_tag = organs.EasyLabel(
                pages[4], [330, 26, 150, 26], text="Ended At", font=FONT_TAG)
            beg = build_element.began()
            end = build_element.ended()
            self.began_tag = organs.EasyLabel(
                pages[4], [20, 46, 80, 26], text=beg.strftime("%I:%M %p"),
                font=FONT_TAG,
                alignment=QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
            self.began_field = organs.EasyDateTimeEdit(
                pages[4], [100, 48, 150, 22],
                display_format="yyyy-MM-dd   hh:mm", calendar_on=True,
                date_time=[beg.year, beg.month, beg.day, beg.hour, beg.minute])
            self.began_field.timeChanged.connect(self.update_began_tag)
            self.ended_field = organs.EasyDateTimeEdit(
                pages[4], [330, 48, 150, 22],
                display_format="yyyy-MM-dd   hh:mm", calendar_on=True,
                date_time=[end.year, end.month, end.day, end.hour, end.minute])
            self.ended_field.timeChanged.connect(self.update_ended_tag)
            self.ended_tag = organs.EasyLabel(
                pages[4], [width - 100, 46, 80, 26],
                text=end.strftime("%I:%M %p"), font=FONT_TAG,
                alignment=QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
            tip_text = "".join([
                "-" * 10, "TIPS", "-" * 10, "\n\n",
                "",
                "If this Workout is part of a Program, its period must begin ",
                "on or after the Program start date if you want to save the ",
                "Program as a record.\n\n",
                "",
                "You must enter the time in 24-hour clock time, from 00:00 ",
                "(12:00 AM) to 23:59 (11:59 PM). In 24-hour clock time, ",
                "hours from 1:00 AM to 12:00 PM are unchanged, and hours ",
                "from 1:00 PM to 11:00 PM are converted by adding 12 to ",
                "them. 9:45 PM is 21:45 in 24-hour time.\n\n",
                "",
                "You can also enter a date by clicking on the small arrow ",
                "next to the date input field to open up a calendar tool. ",
                "Use this tool to find a date, then click on it to enter it ",
                "into the input field.\n\n",
                "",
                "A unique description makes this build element easy to ",
                "identify in the Build Viewer--and even easier to find with ",
                "the Inventory Manager if saved as a template."])
        # Program Page section.
        if self.cid == "P":
            pro_text = "".join([
                "START: Enter the date you started this Program in ",
                "the format 'year-month-day'."])
            program_header = organs.EasyLabel(
                pages[5], [0, 0, 580, 26], text=pro_text, font=FONT_HEADER,
                alignment=QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
            start_tag = organs.EasyLabel(
                pages[5], [240, 26, 100, 26], text="Start", font=FONT_TAG)
            start = build_element.start()
            self.start_field = organs.EasyDateEdit(
                pages[5], [240, 48, 100, 22], display_format="yyyy-MM-dd",
                calendar_on=True, date=[start.year, start.month, start.day])
            tip_text = "".join([
                "-" * 10, "TIPS", "-" * 10, "\n\n",
                "",
                "You can also enter a date by clicking on the small arrow ",
                "next to the date input field to open up a calendar tool. ",
                "Use this tool to find a date, then click on it to enter it ",
                "into the input field.\n\n",
                "",
                "A unique description makes this build element easy to ",
                "identify in the Build Viewer--and even easier to find with ",
                "the Inventory Manager if saved as a template."])
        # Initialize tip box.
        tipbox = organs.TipBox(self, [5, 158, 590, 96], text=tip_text)
        # Connect signals to slots.
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)
        # Set stack page for build element type and set focus on description.
        cid_pages = {"R": 1, "M": 2, "D": 3, "W": 4, "C": 0, "P": 5}
        self.property_stack.setCurrentIndex(cid_pages[self.cid])
        self.description_field.setFocus()
        self.description_field.selectAll()

    def accept(self):
        """Check for valid inputs and accept the dialog."""
        # Set focus on button box so that the input on the currently
        # selected field can be locked in prior to accepting the dialog.
        self.button_box.setFocus()
        # Check Recipe portion inputs, update build element portion. Do not
        # round the numeric_value result of each amount field.
        if self.cid == "R":
            if not self.portion_is_valid():
                return
            # Eval consumed and prepared amounts.
            consumed = organs.numeric_value(str(self.consumed_field.text()))
            prepared = organs.numeric_value(str(self.prepared_field.text()))
            unit = str(self.unit_field.text()).strip()
            self.buildelement.set_portion([consumed, prepared, unit])
        # Convert Meal time QTime to datetime.time, set build elem time.
        elif self.cid == "M":
            self.buildelement.set_time(self.time_field.time().toPyTime())
        # Convert Diet date QDate to datetime.date, set build elem date.
        elif self.cid == "D":
            self.buildelement.set_date(self.date_field.date().toPyDate())
        # Check Workout period inputs, update build element period.
        elif self.cid == "W":
            if not self.period_is_valid():
                return
            began = self.began_field.dateTime().toPyDateTime()
            ended = self.ended_field.dateTime().toPyDateTime()
            self.buildelement.set_period([began, ended])
        # Convert Program start QDate to datetime.date, set build elem start.
        elif self.cid == "P":
            self.buildelement.set_start(self.start_field.date().toPyDate())
        # Check description field for input. If no text is entered, assign
        # default '(unnamed)' text to build element description. Update last
        # in case portion/period check fails and is not set. Update the
        # inherited text attribute with new __str__ value and accept dialog.
        des_text = str(self.description_field.text()).strip()
        description = "(unnamed)" if des_text == "" else des_text
        self.buildelement.set_description(description)
        self.buildelement.setText(0, str(self.buildelement))
        QtGui.QDialog.accept(self)

    def update_began_tag(self):
        """Update 12-hour clock time tag for Workout began."""
        self.began_tag.setText(
            self.began_field.time().toPyTime().strftime("%I:%M %p"))

    def update_ended_tag(self):
        """Update 12-hour clock time tag for Workout ended."""
        self.ended_tag.setText(
            self.ended_field.time().toPyTime().strftime("%I:%M %p"))

    def update_time_tag(self):
        """Update 12-hour clock time tag for Meal time."""
        self.time_tag.setText(
            self.time_field.time().toPyTime().strftime("%I:%M %p"))

    def period_is_valid(self):
        """
        Return True if Workout period is valid, otherwise False.

        Verifies that the Ended Field input occurs at a datetime after the
        Began Field input.
        """
        began = self.began_field.dateTime().toPyDateTime()
        ended = self.ended_field.dateTime().toPyDateTime()
        if began >= ended:
            QtGui.QMessageBox.warning(
                self, "Invalid Period",
                "The period cannot end before it begins!")
            return False
        return True

    def portion_is_valid(self):
        """
        Return True if Recipe portion components are valid, otherwise False.

        Verifies that the consumed and prepared amounts are numeric values
        greater than zero and that a unit has been entered.
        """
        try:
            # Eval consumed and prepared amounts, check for non-numeric values.
            consumed = organs.numeric_value(str(self.consumed_field.text()))
            prepared = organs.numeric_value(str(self.prepared_field.text()))
            unit = str(self.unit_field.text()).strip()
            if None in [consumed, prepared]:
                raise ValueError
            # Check for consumed and prepared amounts greater than zero.
            if consumed <= 0 or prepared <= 0:
                QtGui.QMessageBox.warning(
                    self, "Invalid Amount(s)", "Consumed and prepared " +
                    "amounts must be greater than zero! Be aware that " +
                    "both are rounded to three decimal places.")
                if consumed <= 0:
                    self.consumed_field.setFocus()
                    self.consumed_field.selectAll()
                else:
                    self.prepared_field.setFocus()
                    self.prepared_field.selectAll()
                return False
            # Check for consumed amount greater than prepared amount.
            if consumed > prepared:
                QtGui.QMessageBox.warning(
                    self, "Unconventional Amounts",
                    "The consumed amount is greater than the prepared " +
                    "amount. Be aware that this Recipe's nutrient values " +
                    "will be calculated accordingly.")
            # Check for a unit input.
            if unit == "":
                QtGui.QMessageBox.warning(
                    self, "Missing Unit", "You must enter a portion unit!")
                self.unit_field.setFocus()
                return False
            return True
        except ValueError:
            QtGui.QMessageBox.warning(
                self, "Invalid Amount(s)",
                "Consumed and prepared amounts must be numeric values!")
            return False

    def toggle_favorite(self):
        """Toggle the Favorite button's icon."""
        if self.isfavorite:
            self.favorite_bn.setIcon(organs.EasyIcon("heart"))
            self.isfavorite = False
        else:
            self.favorite_bn.setIcon(organs.EasyIcon("heart_black"))
            self.isfavorite = True


# noinspection PyUnusedLocal
class InputIngredient(organs.EasyDialog):
    """
    Class to edit Ingredient Quantities.

    InputIngredient presents a dialog to the user with input fields for an
    Ingredient's Quantities. These fields are:

        Amount: Numeric amount of a Quantity portion size
        Unit: Unit of measure associated with the Quantity portion size amount

    InputIngredient inherits all attributes and methods from its superclass.
    Its constructor is passed the parent GUI and an Ingredient object. It
    builds a dialog to show all child Quantities of the Ingredient and allows
    the user to add or remove them. It implements an ingredient attribute to
    store the ingredient_object arg and a quantities attribute to store a copy
    of the Ingredient container that can be modified without directly affecting
    the real container.

    The inherited accept method is overridden to clear the Ingredient's
    container, add to it all Quantity objects from the quantities attribute,
    widgetize the Ingredient, and accept the dialog. Slot methods are
    implemented to add, remove, and clear all Quantities from the quantities
    attribute and corresponding Quantity Table.
    """

    def __init__(self, parent, ingredient_object):
        """
        Initialize an InputIngredient object.

        Assigns the ingredient_object arg to the ingredient attribute and a
        copy of the ingredient_object arg's container to the quantities
        attribute. Builds the dialog components and connects input field
        signals to slot methods.

        :param parent: Parent QMainWindow
        :type parent: QMainWindow
        :param ingredient_object: An Ingredient object
        :type ingredient_object: Ingredient
        """
        organs.EasyDialog.__init__(self, parent)
        self.ingredient = ingredient_object
        self.quantities = list(ingredient_object.container())
        # Window properties, button box, and outline frame.
        self.setWindowTitle("Ingredient Quantities")
        self.setWindowIcon(organs.EasyIcon(dna.ICONS["quantity"]))
        width, height = 600, 352
        self.setFixedSize(width, height)
        self.button_box = organs.EasyButtonBox(self)
        outline = organs.OutlineFrame(self, [5, 4, width - 9, 294])
        # Quantity section.
        header_text = "".join([
            "ADD QUANTITY: Enter a numeric amount and select a unit of ",
            "measure."])
        header = organs.EasyLabel(
            self, [10, 4, 580, 26], text=header_text, font=FONT_HEADER,
            alignment=QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        amount_tag = organs.EasyLabel(
            self, [20, 30, 80, 26], text="Amount", font=FONT_TAG)
        unit_tag = organs.EasyLabel(
            self, [294, 30, 120, 26], text="Unit of Measure", font=FONT_TAG)
        self.amount_field = organs.EasyLineEdit(self, [10, 52, 110, 22])
        unit_sequences = ingredient_object.unitsequences()
        units = [seq[1] for seq in unit_sequences if seq[1] != "g"]
        units = sorted(list(set(units)), key=lambda s: s.lower())
        self.unit_field = organs.EasyComboBox(
            self, [130, 52, 460, 22], first_item="g", items=units)
        self.add_quantity_bn = organs.EasyToolButton(
            self, [10, 80, 110, 24], text="Add Quantity", font=FONT_ACTION,
            button_type="action")
        # Quantity Table section. Truncate Ingredient description if too long.
        ing_str = str(ingredient_object)
        ing_text = ing_str[:70] + "..." if len(ing_str) > 70 else ing_str
        ingredient_header = organs.EasyLabel(
            self, [10, 114, 580, 26], text=ing_text, font=FONT_HEADER)
        self.qty_table = organs.EasyTableWidget(
            self, [10, 140, 580, 120], dims=[1, len(self.quantities)],
            center_text=True, column_labels=["Quantities"],
            column_widths=[556], row_height=24, row_header_hidden=True,
            edit_off=True, resize_off=True, stretch_last_section=True)
        for quantity in self.quantities:
            row = self.quantities.index(quantity)
            self.qty_table.item(row, 0).setText(str(quantity))
        self.remove_quantity_bn = organs.EasyToolButton(
            self, [10, 266, 170, 24], text="Remove Quantity",
            font=FONT_ACTION, button_type="action")
        self.clear_quantities_bn = organs.EasyToolButton(
            self, [420, 266, 170, 24], text="Clear Quantities",
            font=FONT_ACTION, button_type="action")
        # Connect signals to slots.
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)
        self.add_quantity_bn.clicked.connect(self.add_quantity)
        self.remove_quantity_bn.clicked.connect(self.remove_quantity)
        self.clear_quantities_bn.clicked.connect(self.clear_quantities)
        # Set focus on the amount field.
        self.amount_field.setFocus()

    def accept(self):
        """Update the Ingredient object's Quantities and accept the dialog."""
        self.ingredient.clear_container()
        for quantity in self.quantities:
            self.ingredient.add_child(quantity)
        self.ingredient.widgetize()
        QtGui.QDialog.accept(self)

    def add_quantity(self):
        """Create a Quantity with the amount and user inputs."""
        try:
            amt_text = str(self.amount_field.text()).strip()
            # Check for an amount input.
            if amt_text == "":
                QtGui.QMessageBox.warning(
                    self, "Missing Amount", "You must enter an amount!")
                self.amount_field.setFocus()
                return
            # Eval amount and check for non-numeric value.
            amount = organs.numeric_value(amt_text)
            if amount is None:
                raise ValueError
            # Check for amount less than or equal to zero.
            if amount <= 0:
                QtGui.QMessageBox.warning(
                    self, "Invalid Amount", "The amount value must be " +
                    "greater than zero! Be aware that it is rounded to " +
                    "three decimal places.")
                self.amount_field.setFocus()
                self.amount_field.selectAll()
                return
            # Construct a Quantity with amount and unit, append to quantities.
            unit = str(self.unit_field.currentText())
            quantity = body.Quantity(self.ingredient.itemid())
            quantity.add_child([amount, unit])
            self.quantities.append(quantity)
            # Update Quantity Table.
            row_count = self.qty_table.rowCount()
            self.qty_table.setRowCount(row_count + 1)
            quantity_item = QtGui.QTableWidgetItem()
            quantity_item.setText(str(quantity))
            quantity_item.setTextAlignment(QtCore.Qt.AlignCenter)
            self.qty_table.setItem(row_count, 0, quantity_item)
            # Scroll to the new Quantity, clear and set focus on amount field.
            self.qty_table.scrollToItem(
                quantity_item, QtGui.QAbstractItemView.PositionAtTop)
            self.qty_table.selectRow(row_count)
            self.amount_field.clear()
            self.amount_field.setFocus()
        except ValueError:
            QtGui.QMessageBox.warning(
                self, "Invalid Amount", "The amount must be a numeric value!")
            self.amount_field.setFocus()
            self.amount_field.selectAll()

    def clear_quantities(self):
        """Clear all Quantities."""
        if not self.quantities:
            return
        self.quantities = []
        self.qty_table.setRowCount(0)

    def remove_quantity(self):
        """Remove the Quantity selected in the Quantity Table."""
        row = self.qty_table.currentRow()
        if row == -1:
            return
        self.quantities.pop(row)
        self.qty_table.removeRow(row)


# noinspection PyUnusedLocal
class InputActivity(organs.EasyDialog):
    """
    Class to edit Activity Sessions.

    InputActivity presents a dialog to the user with an input table for an
    Activity's Sessions. The three columns in this input table are:

        Effort: Numeric effort amount of Session performance measurement
        Intensity: Numeric intensity amount of Session performance measurement
        Note: An optional note

    InputActivity inherits all attributes and methods from its superclass. Its
    constructor is passed the parent GUI and an Activity object. It builds a
    dialog to show all child Session of the Activity and allows the user to add
    or remove them. It implements an activity attribute to store the
    activity_object arg.

    The inherited accept method is overridden to clear the Activity's
    container, add to it all Session objects created by parsing the Session
    Table cell data, widgetize the Activity, and accept the dialog. A slot
    method is implemented to add an additional blank row to the Session Table.
    """

    def __init__(self, parent, activity_object):
        """
        Initialize an InputActivity object.

        Assigns the activity_object arg to the activity attribute. Builds the
        dialog components and connects input field signals to slot methods.

        :param parent: Parent QMainWindow
        :type parent: QMainWindow
        :param activity_object: An Activity object
        :type activity_object: Activity
        """
        organs.EasyDialog.__init__(self, parent)
        self.activity = activity_object
        # Window properties, button box, and outline frame.
        self.setWindowTitle("Activity Sessions")
        self.setWindowIcon(organs.EasyIcon(dna.ICONS["session"]))
        width, height = 600, 506
        self.setFixedSize(width, height)
        self.button_box = organs.EasyButtonBox(self)
        outline = organs.OutlineFrame(self, [5, 4, width - 9, 336])
        # Headers and tags.
        header_text = "".join([
            "ADD SESSIONS: Enter effort and intensity amounts for each ",
            "Session--one per row."])
        header = organs.EasyLabel(
            self, [10, 4, 580, 26], text=header_text, font=FONT_HEADER,
            alignment=QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        activity_tag = organs.EasyLabel(
            self, [10, 30, 110, 26], text="Activity:", font=FONT_TAG,
            alignment=QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        activity_text = organs.EasyLabel(
            self, [130, 30, width - 140, 26], text=str(activity_object)[3:],
            alignment=QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        units = activity_object.units()
        effort_tag = organs.EasyLabel(
            self, [10, 52, 110, 26], text="Effort Unit:", font=FONT_TAG,
            alignment=QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        effort_text = organs.EasyLabel(
            self, [130, 52, width - 140, 26], text=units[0],
            alignment=QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        intensity_tag = organs.EasyLabel(
            self, [10, 74, 110, 26], text="Intensity Unit:", font=FONT_TAG,
            alignment=QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        intensity_text = organs.EasyLabel(
            self, [130, 74, width - 140, 26], text=units[1],
            alignment=QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        # Session Table.
        self.add_row_bn = organs.EasyToolButton(
            self, [width - 150, 82, 140, 24], text="Add Blank Row",
            font=FONT_ACTION, button_type="action")
        self.ses_table = organs.EasyTableWidget(
            self, [10, 110, width - 20, 222], center_text=True,
            dims=[3, len(activity_object.container())], row_height=24,
            column_labels=["Effort", "Intensity", "Note (optional)"],
            column_width=110, stretch_last_section=True)
        row = 0
        for ses in activity_object.container():
            ses_text = [str(ses.effort()), str(ses.intensity()), ses.note()]
            for col in range(3):
                self.ses_table.item(row, col).setText(ses_text[col])
            row += 1
        # Make sure there are at least 10 rows. If not, add blank rows.
        for _ in range(row, 10):
            self.add_row()
        # Tip box section.
        tip_text = "".join([
            "-" * 10, "TIPS", "-" * 10, "\n\n",
            "",
            "The Session note is optional. It is provided in case you want ",
            "to identify special information, such as additional equipment ",
            "used or if the Session is a superset of a previous Activity.\n\n",
            "",
            "If you are entering Session info for an Exercise that ",
            "does not have an intensity unit specified (e.g. 'NA'), ",
            "enter a value of '1' into the Intensity column. The magnitude ",
            "of this Session will just be its effort amount.\n\n",
            "",
            "Effort and intensity columns accept simple fractions such as ",
            "'1/2'. You might use this feature to enter an effort of ",
            "'35.5/60' if you ran for 35.5 minutes and your effort unit ",
            "is 'hours'. You might enter an intensity value of '5/1.25' ",
            "if your intensity unit is 'mph' and you want to calculate ",
            "the speed when running 5 miles in 1.25 hours (70 minutes). ",
            "Complex fractions such as '(4/5)/6' are not valid.\n\n",
            "",
            "When you click 'OK', blank rows in the table are ignored. Rows ",
            "with only an effort or only an intensity are counted as ",
            "incomplete. Complete Session info has both effort and intensity ",
            "amounts."])
        tipbox = organs.TipBox(self, [5, 350, width - 10, 100], text=tip_text)
        # Connect signals to slots.
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)
        self.add_row_bn.clicked.connect(self.add_row)
        # Set focus on the first effort cell in the session table.
        self.ses_table.setCurrentCell(0, 0)
        self.ses_table.edit(self.ses_table.currentIndex())

    def accept(self):
        """Update the Activity object's Sessions and accept the dialog."""
        try:
            # Set focus on button box so that the input on the currently
            # selected item can be locked in prior to accepting the dialog.
            self.button_box.setFocus()
            # Parse the table inputs.
            session_children = []
            incomplete_session = False
            for row in range(self.ses_table.rowCount()):
                eff_text = str(self.ses_table.item(row, 0).text()).strip()
                int_text = str(self.ses_table.item(row, 1).text()).strip()
                unit = str(self.ses_table.item(row, 2).text()).strip()
                # Ignore blank rows.
                if [eff_text, int_text, unit].count("") == 3:
                    continue
                # Check for no effort/intensity amount in non-blank rows.
                if "" in [eff_text, int_text]:
                    incomplete_session = True
                    continue
                # Eval effort/intensity text and check for non-numeric values.
                effort = organs.numeric_value(eff_text, round_digits=5)
                intensity = organs.numeric_value(int_text, round_digits=5)
                if None in [effort, intensity]:
                    raise ValueError
                # Check for effort/intensity less than or equal to zero.
                if effort <= 0 or intensity <= 0:
                    QtGui.QMessageBox.warning(
                        self, "Invalid Amount(s)", "All effort and " +
                        "intensity amounts must be greater than zero! " +
                        "Be aware that amounts are rounded to five decimal " +
                        "places.")
                    return
                session_children.append([effort, intensity, unit])
            # Check if the user wants to discard incomplete session rows.
            if incomplete_session:
                choice = QtGui.QMessageBox.warning(
                    self, "Incomplete Session(s)", "At least one Session " +
                    "is missing both effort and intensity amounts. Click " +
                    "'Save' to ignore all incomplete Sessions and save " +
                    "anyway. Click 'Cancel' to go back and make changes.",
                    QtGui.QMessageBox.Save | QtGui.QMessageBox.Cancel)
                if choice == QtGui.QMessageBox.Cancel:
                    return
            # Build Session objects and add them to the Activity.
            itemid = self.activity.itemid()
            self.activity.clear_container()
            for session_child in session_children:
                session = body.Session(itemid)
                session.add_child(session_child)
                self.activity.add_child(session)
            self.activity.widgetize()
            QtGui.QDialog.accept(self)
        except ValueError:
            QtGui.QMessageBox.warning(
                self, "Invalid Amount(s)",
                "All effort and intensity amounts must be numeric values!")

    def add_row(self):
        """Add a blank row to the Session Table."""
        row_count = self.ses_table.rowCount()
        self.ses_table.setRowCount(row_count + 1)
        for col in range(3):
            blank_item = QtGui.QTableWidgetItem()
            blank_item.setTextAlignment(QtCore.Qt.AlignCenter)
            self.ses_table.setItem(row_count, col, blank_item)


# -----------------------------------------------------------------------------
# Inventory Manager Classes ---------------------------------------------------

# noinspection PyUnusedLocal
class InputFood(organs.EasyDialog):
    """
    Class to edit Food reference item properties.

    InputFood presents a dialog to the user with input fields for a Food's
    properties. These fields are:

        Description: A description between 1-200 characters
        Food Group: The food group name
        Amount: Numeric amount for a unit sequence
        Unit: Unit of measure between 1-30 characters for a unit sequence
        Gram Weight: Numeric gram weight for a unit sequence
        Unit Sequence Table: A table with existing unit sequences
        Serving Size: The serving size associated with the nutrient values
            entered into the Nutrient Content Table
        Nutrient Content Table: A table in which to enter nutrient values and
            each corresponding unit of measure for a selected serving size

    InputFood inherits all attributes and methods from its superclass. Its
    constructor is passed the parent GUI, the user's User object, and an
    optional Reference object. It builds a dialog and, if a Reference object is
    passed to it, populates all input fields with existing property values.
    It implements a food attribute to store the reference arg or, if it is
    None, a new Reference object with null properties.

    The inherited accept method is overridden to check that all input field
    values are valid and accept the dialog. Slot methods are implemented to
    add and remove unit sequences from the Unit Sequence Table, toggle the
    Favorite Button icon, update the food attribute's 'nutrientcontent'
    property with nutrient value inputs, and update the Nutrient Table.
    """

    def __init__(self, parent, user, reference=None):
        """
        Initialize an InputFood object.

        Assigns a new Reference object, or the existing Reference object
        assigned to the reference parameter, to the food attribute. The user
        arg is ignored in the current version of this application and included
        here only to match the InputExercise constructor signature and allow
        the GUI to handle both in a standardized manner. Builds the dialog
        components and connects input field signals to slot methods.

        :param parent: Parent QMainWindow
        :type parent: QMainWindow
        :param user: The current user's User object
        :type user: User
        :param reference: A Reference object with existing Food properties
        :type reference: Reference
        """
        organs.EasyDialog.__init__(self, parent)
        self.food = body.Reference("Food") if reference is None else reference
        # Window properties, button box, and outline frame.
        self.setWindowTitle("Food Properties")
        self.setWindowIcon(organs.EasyIcon(dna.ICONS["nutrition"]))
        width, height = 800, 570
        self.setFixedSize(width, height)
        self.button_box = organs.EasyButtonBox(self)
        outline_a = organs.OutlineFrame(self, [5, 4, width - 9, 56])
        outline_b = organs.OutlineFrame(self, [5, 70, 372, 54])
        outline_c = organs.OutlineFrame(self, [5, 134, 372, 272])
        outline_d = organs.OutlineFrame(self, [386, 70, 409, 336])
        # Description section.
        des_text = "".join([
            "DESCRIPTION: Enter a unique description up to 200 ",
            "characters long."])
        description_header = organs.EasyLabel(
            self, [10, 4, 780, 26], text=des_text, font=FONT_HEADER,
            alignment=QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.description_field = organs.EasyLineEdit(
            self, [10, 30, 720, 22], max_length=200)
        # Favorite button.
        fav_icon = "heart_black" if self.food.info("isfavorite") else "heart"
        self.favorite_bn = organs.EasyToolButton(
            self, [746, 10, 42, 42], icon_name=fav_icon, icon_size=[40, 40],
            button_type="selection")
        # Food Group section.
        group_header = organs.EasyLabel(
            self, [10, 70, 364, 26], text="FOOD GROUP: Select a food group.",
            font=FONT_HEADER,
            alignment=QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        group_top = "-" * 15 + "FOOD GROUPS" + "-" * 15
        group_names = sorted(
            dna.FOOD_GROUPS.values(), key=lambda s: s.lower())
        self.group_field = organs.EasyComboBox(
            self, [44, 94, 280, 22], items=group_names, first_item=group_top)
        # Unit Sequences section.
        seq_header = organs.EasyLabel(
            self, [10, 134, 364, 26], font=FONT_HEADER,
            text="UNIT SEQUENCES: Enter a serving size and its weight.",
            alignment=QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        amount_tag = organs.EasyLabel(
            self, [16, 160, 80, 26], text="Amount", font=FONT_TAG)
        unit_tag = organs.EasyLabel(
            self, [101, 160, 180, 26], text="Unit of Measure", font=FONT_TAG)
        weight_tag = organs.EasyLabel(
            self, [286, 160, 80, 26], text="Weight (g)", font=FONT_TAG)
        self.amount_field = organs.EasyLineEdit(self, [16, 182, 80, 22])
        self.unit_field = organs.EasyLineEdit(
            self, [101, 182, 180, 22], max_length=30)
        self.weight_field = organs.EasyLineEdit(self, [286, 182, 80, 22])
        self.add_sequence_bn = organs.EasyToolButton(
            self, [101, 210, 180, 24], text="Add Unit Sequence",
            font=FONT_ACTION, button_type="action")
        self.seq_table = organs.EasyTableWidget(
            self, [10, 248, 360, 120], dims=[3, 0], row_height=22,
            column_labels=["Amount", "Unit of Measure", "Weight (g)"],
            column_widths=[82, 170, 82], row_header_hidden=True, edit_off=True,
            select_rows=True, stretch_last_section=True)
        self.remove_sequence_bn = organs.EasyToolButton(
            self, [101, 374, 180, 24], text="Remove Unit Sequence",
            font=FONT_ACTION, button_type="action")
        # Nutrient Content section.
        nut_header_text = "".join([
            "NUTRIENT CONTENT: Enter values for a serving size."])
        nutrient_header = organs.EasyLabel(
            self, [391, 70, 399, 26], text=nut_header_text, font=FONT_HEADER,
            alignment=QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        serving_tag = organs.EasyLabel(
            self, [416, 94, 100, 26], text="Serving Size:", font=FONT_TAG)
        self.serving_size_field = organs.EasyComboBox(
            self, [524, 94, 240, 22], first_item="ENTER A UNIT SEQUENCE")
        rlabs = [dna.NUTRIENTS[nid][0] for nid in dna.GUI_NUTRIENTS]
        self.nut_table = organs.EasyTableWidget(
            self, [391, 122, 398, 276], dims=[2, len(rlabs)], row_height=28,
            center_text=True, column_labels=["Value", "Unit"], resize_off=True,
            column_widths=[100, 64], row_labels=rlabs, row_header_width=210,
            stretch_last_section=True)
        for nid in dna.GUI_NUTRIENTS:
            row = dna.GUI_NUTRIENTS.index(nid)
            # Add unit drop-down if nutrient has recommended daily value.
            if nid in dna.FDA_RDV:
                unit_drop = QtGui.QComboBox(self)
                unit_drop.addItem(dna.NUTRIENTS[nid][2])
                unit_drop.addItem("% DV")
                unit_drop.currentIndexChanged.connect(self.update_nut_table)
                self.nut_table.setCellWidget(row, 1, unit_drop)
            else:
                unit_item = self.nut_table.item(row, 1)
                unit_item.setText(dna.NUTRIENTS[nid][2])
                # Set color to black, as text will dim when not selectable.
                unit_item.setFlags(QtCore.Qt.ItemIsSelectable)
                unit_item.setTextColor(QtGui.QColor(0, 0, 0))
        # Update fields for existing Food properties.
        if reference is not None:
            self.description_field.setText(self.food.info("description"))
            self.group_field.setCurrentIndex(
                self.group_field.findText(
                    dna.FOOD_GROUPS[self.food.info("groupid")]))
            self.seq_table.setRowCount(len(self.food.info("unitsequences")))
            self.remove_sequence_bn.setEnabled(False)
            self.serving_size_field.removeItem(0)
            for row in range(self.seq_table.rowCount()):
                seq = self.food.info("unitsequences")[row]
                serving_text = str(seq[0]) + " " + seq[1]
                for col in range(3):
                    seq_item = QtGui.QTableWidgetItem()
                    seq_item.setText(str(seq[col]))
                    seq_item.setTextAlignment(QtCore.Qt.AlignCenter)
                    self.seq_table.setItem(row, col, seq_item)
                self.serving_size_field.addItem(serving_text)
            self.update_nut_table()
        # Tip box section.
        tip_text = "".join([
            "-" * 10, "TIPS", "-" * 10, "\n\n",
            "",
            "Click the Favorite button in the top right corner, shown with a ",
            "heart icon, to add or remove this Food from your Favorite Foods ",
            "list. If the heart is solid black, this Food is a favorite.\n\n",
            "",
            "A unique DESCRIPTION makes this Food easy to find with the ",
            "Inventory Manager. When you add this Food to a build as an ",
            "Ingredient, that Ingredient will display this description.\n\n",
            "",
            "UNIT SEQUENCES of a Food are different serving sizes and each ",
            "one's weight in grams. A serving size is an amount of some unit ",
            "of measure (e.g. '1 cup'). Gram weight is used to relate all ",
            "serving sizes to a standard unit, and it is usually found in ",
            "parentheses on the Food's nutrition label. If no weight is ",
            "given, you can weigh out a known serving size or find the gram ",
            "weight of a similar Food with the same serving size and use ",
            "that (e.g. 1 cup, or 240 mL, of milk is equal to 244 grams).\n\n",
            "",
            "Once you save a Food, you can continue adding unit sequences to ",
            "it, but you can no longer delete them. This prevents you from ",
            "deleting serving sizes that are referenced by Ingredient ",
            "Quantities added to templates and records.\n\n",
            "",
            "You must select a serving size to associate with the Food's ",
            "NUTRIENT CONTENT. This connects the nutrient values to a known ",
            "portion. For example, if you know nutrient values for 1 cup ",
            "of the Food, you would select '1 cup' from the Serving Size ",
            "drop-down list before entering values into the table.\n\n",
            "",
            "Some nutrients in the NUTRIENT CONTENT table have a drop-down ",
            "list in the Unit column. For these nutrients, you can enter ",
            "one of two types of Values: an amount of the unit of measure ",
            "shown, or a percentage of the US FDA recommended daily value ",
            "for that nutrient. If you enter a percentage, select the '% DV' ",
            "option from the Unit drop-down list.\n\n",
            "",
            "If you are editing an existing Food, and you change either the ",
            "NUTRIENT CONTENT Serving Size or the unit selected in ",
            "one of the Unit drop-down lists, the applicable nutrient ",
            "Value(s) will automatically update to reflect this change.\n\n",
            "",
            "UNIT SEQUENCES Amount and Weight fields and NUTRIENT CONTENT ",
            "Value fields accept simple fractions such as '1/2'. You might ",
            "use this feature to enter an Amount of '1/3' if your serving ",
            "size is one-third of a 'cup'. Complex fractions such as ",
            "'(4/5)/6' or '5/10/3' are not valid."])
        tipbox = organs.TipBox(self, [5, 416, 790, 100], text=tip_text)
        # Connect signals to slots.
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)
        self.favorite_bn.clicked.connect(self.toggle_favorite)
        self.add_sequence_bn.clicked.connect(self.add_sequence)
        self.remove_sequence_bn.clicked.connect(self.remove_sequence)
        self.serving_size_field.currentIndexChanged.connect(
            self.update_nut_table)
        self.nut_table.cellChanged.connect(self.update_nutrientcontent)
        # Set focus on the description field.
        self.description_field.setFocus()

    def accept(self):
        """Check for valid inputs and accept the dialog."""
        # Set focus on button box so that the input on the currently
        # selected field can be locked in prior to accepting the dialog.
        self.button_box.setFocus()
        description = str(self.description_field.text()).strip()
        # Check description field for input.
        if description == "":
            QtGui.QMessageBox.warning(
                self, "Missing Description",
                "You must enter a description for this Food!")
            self.description_field.setFocus()
            return
        # Check food group selected and determine food group ID.
        group_name = str(self.group_field.currentText())
        groupid = None
        for gid, name in dna.FOOD_GROUPS.items():
            if name == group_name:
                groupid = gid
                break
        if groupid is None:
            QtGui.QMessageBox.warning(
                self, "Missing Food Group",
                "You must select a food group!")
            return
        # Check for at least one unit sequence input.
        if not self.food.info("unitsequences"):
            QtGui.QMessageBox.warning(
                self, "Missing Unit Sequence",
                "You must enter at least one unit sequence!")
            self.amount_field.setFocus()
            return
        # Check for at least one nutrient value input.
        if not self.food.info("nutrientcontent"):
            QtGui.QMessageBox.warning(
                self, "Missing Nutrient Content", "You must enter at least " +
                "one nutrient value for the selected serving size!")
            return
        # Update food attribute with remaining properties.
        self.food.update_info({
            "description": description, "groupid": groupid})
        QtGui.QDialog.accept(self)

    def add_sequence(self):
        """Add a unit sequence to the Food."""
        try:
            amt_text = str(self.amount_field.text()).strip()
            unit = str(self.unit_field.text()).strip()
            wgt_text = str(self.weight_field.text()).strip()
            # Check for all unit sequence inputs.
            if amt_text == "":
                QtGui.QMessageBox.warning(
                    self, "Missing Amount", "You must enter an amount value!")
                self.amount_field.setFocus()
                return
            if unit == "":
                QtGui.QMessageBox.warning(
                    self, "Missing Unit", "You must enter a unit of measure!")
                self.unit_field.setFocus()
                return
            if wgt_text == "":
                QtGui.QMessageBox.warning(
                    self, "Missing Weight", "You must enter a gram weight!")
                self.weight_field.setFocus()
                return
            # Eval amount and weight and check for non-numeric values.
            amount = organs.numeric_value(amt_text, round_digits=5)
            weight = organs.numeric_value(wgt_text, round_digits=5)
            if None in [amount, weight]:
                raise ValueError
            # Check that amount and weight are both greater than zero.
            if amount <= 0 or weight <= 0:
                QtGui.QMessageBox.warning(
                    self, "Invalid Amount/Weight", "The amount and weight " +
                    "values must be greater than zero! Be aware that both " +
                    "are rounded to five decimal places.")
                if amount <= 0:
                    self.amount_field.setFocus()
                    self.amount_field.selectAll()
                else:
                    self.weight_field.setFocus()
                    self.weight_field.selectAll()
                return
            # Check for existing serving size unit.
            for seq in self.food.info("unitsequences"):
                if seq[1] == unit:
                    QtGui.QMessageBox.warning(
                        self, "Existing Unit", "A unit sequence already " +
                        "exists with this unit of measure!")
                    self.unit_field.setFocus()
                    self.unit_field.selectAll()
                    return
            # Add unit sequence to the food attribute and Sequence Table, add
            # serving size to Serving Size field (remove placeholder if it has
            # not yet been removed). The food's info is DIRECTLY modified.
            self.food.info("unitsequences").append([amount, unit, weight])
            serving_text = str(amount) + " " + unit
            if self.serving_size_field.itemText(0) == "ENTER A UNIT SEQUENCE":
                self.serving_size_field.removeItem(0)
            self.serving_size_field.addItem(serving_text)
            row_count = self.seq_table.rowCount()
            self.seq_table.setRowCount(row_count + 1)
            sequence_text = [str(amount), unit, str(weight)]
            for col in range(3):
                seq_item = QtGui.QTableWidgetItem()
                seq_item.setText(sequence_text[col])
                seq_item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.seq_table.setItem(row_count, col, seq_item)
            # Scroll to the new unit sequence item, clear all unit sequence
            # input fields and set the focus on the amount field.
            self.seq_table.scrollToItem(
                self.seq_table.item(row_count, 1),
                QtGui.QAbstractItemView.PositionAtTop)
            self.seq_table.selectRow(row_count)
            self.amount_field.clear()
            self.unit_field.clear()
            self.weight_field.clear()
            self.amount_field.setFocus()
        except ValueError:
            QtGui.QMessageBox.warning(
                self, "Invalid Amount/Weight",
                "Unit sequence amount and weight must be numeric values!")

    def remove_sequence(self):
        """Remove a unit sequence selected in the Unit Sequence Table."""
        row = self.seq_table.currentRow()
        if row == -1:
            QtGui.QMessageBox.warning(
                self, "No Unit Sequence Selected",
                "You must select a unit sequence to remove!")
            return
        # The food's info is DIRECTLY modified.
        self.food.info("unitsequences").pop(row)
        self.seq_table.removeRow(row)
        self.serving_size_field.removeItem(row)
        # Re-add the placeholder if all unit sequences have been removed.
        if self.serving_size_field.count() == 0:
            self.serving_size_field.addItem("ENTER A UNIT SEQUENCE")

    def toggle_favorite(self):
        """Toggle the Favorite button's icon."""
        if self.food.info("isfavorite"):
            self.favorite_bn.setIcon(organs.EasyIcon("heart"))
            self.food.set_property("isfavorite", False)
        else:
            self.favorite_bn.setIcon(organs.EasyIcon("heart_black"))
            self.food.set_property("isfavorite", True)

    def update_nut_table(self):
        """
        Update the Nutrient Content Table.

        Updates the Nutrient Content Table when the user selects a different
        Serving Size field option or Unit column drop-down option. This ensures
        that nutrient values shown in the table are accurate. In either case,
        the food attribute's 'nutrientcontent' property, which stores nutrient
        values for 100 grams of the Food, is used as a standard reference from
        which which to calculate updated values.

        If a new Food reference item is being edited, this method is ignored.
        This lets the user enter nutrient values without having to select the
        right serving size first. If this method were executed and the user
        attempted to select a different serving size after entering all
        relevant nutrient values, the values would be recalculated for the new
        serving size and the user would be forced to reenter data.
        """
        try:
            # If a Food has no item ID and is not a data capsule, check if the
            # Unit drop change would affect a Value and make change to NutCont.
            if (self.food.info("itemid") == "" and
               not self.food.info("isdatacapsule")):
                row = self.nut_table.currentRow()
                if row != -1:
                    self.update_nutrientcontent(row, 0)
                return
            # Block table signals so cells can be changed without calling
            # update_nutrientcontent each time.
            self.nut_table.blockSignals(True)
            # Calculate a nutrient multiplier for the selected serving size's
            # gram weight. This is the inverse of update_nutrientcontent.
            multiplier = 1
            for seq in self.food.info("unitsequences"):
                serving_text = str(seq[0]) + " " + seq[1]
                if serving_text == str(self.serving_size_field.currentText()):
                    multiplier = seq[2] / 100.0
                    break
            nutcont = self.food.info("nutrientcontent")
            for nid in dna.GUI_NUTRIENTS:
                row = dna.GUI_NUTRIENTS.index(nid)
                val_text = ""
                if nid in nutcont:
                    # Value for 100 grams (one hectogram).
                    hec_val = nutcont[nid]
                    # Determine if %DV unit and convert to a percentage value.
                    if nid in dna.FDA_RDV:
                        unit = str(
                            self.nut_table.cellWidget(row, 1).currentText())
                        if unit == "% DV":
                            rdv_val = float(dna.FDA_RDV[nid][0])
                            hec_val = (hec_val / rdv_val) * 100
                    # Eval hectogram value times multiplier, check non-numeric.
                    value = organs.numeric_value(hec_val * multiplier)
                    if value is None:
                        raise ValueError
                    val_text = str(value)
                self.nut_table.item(row, 0).setText(val_text)
            self.nut_table.blockSignals(False)
        except ValueError:
            self.nut_table.blockSignals(False)
            QtGui.QMessageBox.warning(
                self, "Invalid Nutrient Value(s)",
                "Nutrient values must be numeric!")

    def update_nutrientcontent(self, row, col):
        """
        Updates the food attribute's 'nutrientcontent' property.

        Determines the Nutrient Content Table item that has changed, its new
        value, and the nutrient ID associated with it. The value is checked for
        validity before being mapped to the nutrient ID key in the food
        attribute's 'nutrientcontent' property.

        :param row: The row of the changed Nutrient Content Table item
        :type row: int
        :param col: The column of the changed Nutrient Content Table item
        :type col: int
        """
        try:
            nid = dna.GUI_NUTRIENTS[row]
            val_text = str(self.nut_table.item(row, 0).text()).strip()
            # If the value changed to blank text, try to remove that nutrient
            # ID key from the food's nutrient content.
            if val_text == "":
                if nid in self.food.info("nutrientcontent"):
                    self.food.info("nutrientcontent").pop(nid)
                return
            # Calculate a nutrient multiplier for the selected serving size's
            # gram weight. This is the inverse of update_nut_table.
            multiplier = 1
            for seq in self.food.info("unitsequences"):
                serving_text = str(seq[0]) + " " + seq[1]
                if serving_text == str(self.serving_size_field.currentText()):
                    multiplier = 100.0 / seq[2]
                    break
            # Eval value text and check for non-numeric value.
            value = organs.numeric_value(val_text)
            if value is None:
                raise ValueError
            # Determine if %DV unit and convert to actual value.
            if nid in dna.FDA_RDV:
                unit = str(self.nut_table.cellWidget(row, 1).currentText())
                if unit == "% DV":
                    rdv_val = dna.FDA_RDV[nid][0]
                    value = (value / 100.0) * rdv_val
            # Eval value times multiplier.
            final_value = organs.numeric_value(value * multiplier)
            # Check for value less than zero and remove it from cell.
            if final_value <= 0:
                QtGui.QMessageBox.warning(
                    self, "Invalid Nutrient Value", "The nutrient value " +
                    "was calculated to be less than zero! Final values are " +
                    "rounded to three decimal places. Enter a higher " +
                    "value or leave that nutrient blank.")
                self.nut_table.blockSignals(True)
                self.nut_table.item(row, 0).setText("")
                self.nut_table.blockSignals(False)
                if nid in self.food.info("nutrientcontent"):
                    self.food.info("nutrientcontent").pop(nid)
                return
            # Update nutrient content (DIRECTLY).
            self.food.info("nutrientcontent")[nid] = final_value
        except ValueError:
            self.nut_table.blockSignals(True)
            self.nut_table.item(row, 0).setText("")
            self.nut_table.blockSignals(False)
            nid = dna.GUI_NUTRIENTS[row]
            if nid in self.food.info("nutrientcontent"):
                self.food.info("nutrientcontent").pop(nid)
            QtGui.QMessageBox.warning(
                self, "Invalid Nutrient Value",
                "Nutrient values must be numeric!")


# noinspection PyUnusedLocal
class InputExercise(organs.EasyDialog):
    """
    Class to prompt the user for Exercise reference item properties.

    InputExercise presents a dialog to the user with input fields for an
    Exercise's properties. These fields are:

        Description: A description between 1-200 characters
        Focus Muscle: The focus muscle
        Effort: Unit of measure between 1-20 characters for performance effort,
            or how much work is accomplished
        Intensity: Unit of measure between 1-20 characters for performance
            intensity, or how hard the user was pushed to do the work
        Tags: All informational tags that apply
        Existing Tags: All existing Exercise tags

    InputExercise inherits all attributes and methods from its superclass. Its
    constructor is passed the parent GUI, the user's User object, and an
    optional Reference object. It builds a dialog and, if a Reference object is
    passed to it, populates all input fields with existing property values. It
    implements an exercise attribute to store the reference arg or, if it is
    None, a new Reference object with null properties. The user arg is used to
    find all existing Exercise tags for the Existing Tags field.

    The inherited accept method is overridden to check that all input field
    values are valid and accept and dialog. Slot methods are implemented to add
    a tag from the Existing Tags Field and toggle the Favorite Button icon.
    """

    def __init__(self, parent, user, reference=None):
        """
        Initialize an InputExercise object.

        Assigns a new Reference object, or the existing Reference object
        assigned to the reference parameter, to the exercise attribute. Builds
        the dialog components and connects input field signals to slot methods.

        :param parent: Parent QMainWindow
        :type parent: QMainWindow
        :param user: The current user's User object
        :type user: User
        :param reference: A Reference object with existing Exercise properties
        :type reference: Reference
        """
        organs.EasyDialog.__init__(self, parent)
        if reference is None:
            self.exercise = body.Reference("Exercise")
        else:
            self.exercise = reference
        # Window properties, button box, and outline frames.
        self.setWindowTitle("Exercise Properties")
        self.setWindowIcon(organs.EasyIcon(dna.ICONS["fitness"]))
        width, height = 700, 476
        self.setFixedSize(width, height)
        self.button_box = organs.EasyButtonBox(self)
        outline_a = organs.OutlineFrame(self, [5, 4, width - 9, 56])
        outline_b = organs.OutlineFrame(self, [5, 70, width - 9, 36])
        outline_c = organs.OutlineFrame(self, [5, 116, width - 9, 100])
        outline_d = organs.OutlineFrame(self, [5, 226, width - 9, 84])
        # Description section.
        des_text = "".join([
            "DESCRIPTION: Enter a unique description up to 200 ",
            "characters long."])
        description_header = organs.EasyLabel(
            self, [10, 4, 680, 26], text=des_text, font=FONT_HEADER,
            alignment=QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.description_field = organs.EasyLineEdit(
            self, [10, 30, 620, 22], max_length=200)
        # Favorite button.
        f_icon = "heart_black" if self.exercise.info("isfavorite") else "heart"
        self.favorite_bn = organs.EasyToolButton(
            self, [646, 10, 42, 42], icon_name=f_icon, icon_size=[40, 40],
            button_type="selection")
        # Focus Muscle section.
        foc_text = "FOCUS MUSCLE: Select the primary focus muscle."
        focusmuscle_header = organs.EasyLabel(
            self, [10, 70, 680, 26], text=foc_text, font=FONT_HEADER,
            alignment=QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.focusmuscle_field = organs.EasyComboBox(
            self, [550, 76, 140, 22], first_item="-----MUSCLES-----",
            items=dna.MUSCLES)
        # Performance Metric Units section.
        units_text = "".join([
            "UNITS: Enter measurement units for the performance metrics ",
            "'effort' and 'intensity'."])
        units_header = organs.EasyLabel(
            self, [10, 116, 680, 26], text=units_text, font=FONT_HEADER,
            alignment=QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        effort_tag = organs.EasyLabel(
            self, [140, 142, 160, 26], text="Effort Unit", font=FONT_TAG)
        intensity_tag = organs.EasyLabel(
            self, [400, 142, 160, 26], text="Intensity Unit", font=FONT_TAG)
        self.effort_field = organs.EasyLineEdit(
            self, [140, 164, 160, 22], max_length=20)
        self.intensity_field = organs.EasyLineEdit(
            self, [400, 164, 160, 22], max_length=20)
        effort_ex_tag = organs.EasyLabel(
            self, [120, 186, 200, 26], text="(e.g. rep, min, mi, km)",
            font=FONT_HEADER)
        intensity_ex_tag = organs.EasyLabel(
            self, [380, 186, 200, 26], text="(e.g. lb, kg, mph, kph)",
            font=FONT_HEADER)
        # Tags section.
        tags_text = "".join([
            "TAGS: Enter custom tags separated by commas. Add existing ",
            "tags from the drop-down list."])
        tags_header = organs.EasyLabel(
            self, [10, 226, 680, 26], text=tags_text, font=FONT_HEADER,
            alignment=QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.tags_field = organs.EasyLineEdit(self, [10, 252, 680, 22])
        existing_tags = set()
        edref = user.exercise_details()
        for itemid in edref:
            for tag in edref[itemid][3]:
                existing_tags.add(tag)
        sorted_tags = sorted(list(existing_tags), key=lambda s: s.lower())
        self.existing_tags_field = organs.EasyComboBox(
            self, [10, 280, 300, 22], items=sorted_tags,
            first_item="-" * 14 + "ALL EXISTING TAGS" + "-" * 14)
        self.add_tag_bn = organs.EasyToolButton(
            self, [320, 280, 200, 22], text="Add Existing Tag",
            font=FONT_ACTION, button_type="action")
        # Update fields for existing Exercise properties.
        if reference is not None:
            self.description_field.setText(self.exercise.info("description"))
            self.focusmuscle_field.setCurrentIndex(
                self.focusmuscle_field.findText(
                    self.exercise.info("focusmuscle")))
            self.effort_field.setText(self.exercise.info("units")[0])
            self.intensity_field.setText(self.exercise.info("units")[1])
            self.tags_field.setText(
                ", ".join([tag for tag in self.exercise.info("tags")]))
        # Tip box section.
        tip_text = "".join([
            "-" * 10, "TIPS", "-" * 10, "\n\n",
            "",
            "Click the Favorite button in the top right corner, shown with a ",
            "heart icon, to add or remove this Exercise from your Favorite ",
            "Exercises list. If the heart is solid black, this Exercise is a ",
            "favorite.\n\n",
            "",
            "A unique DESCRIPTION makes this Exercise easy to find with the ",
            "Inventory Manager. When you add this Exercise to a build as an ",
            "Activity, that Activity will display this description.\n\n",
            "",
            "The FOCUS MUSCLE is the muscle that is primarily used to ",
            "perform this Exercise. If you can't identify a focus muscle, ",
            "select 'NA' (not applicable) or one of the general areas like ",
            "'Upper Body'.\n\n",
            "",
            "The EFFORT UNIT and INTENSITY UNIT are units of measure for the ",
            "Exercise performance metrics 'effort' and 'intensity'. Effort ",
            "is how much work you did, and intensity is how hard you pushed ",
            "yourself to do that work. Enter whichever units make the most ",
            "sense to you.\n\n",
            "",
            "Exercise effort might be measured in 'rep' (repetitions) or ",
            "'min' (minutes), such as in '10 rep of squats' or '10 min of ",
            "running'. Exercise intensity might be measured in 'lb' (pounds) ",
            "or 'mph' (miles her hour), such as in '10 rep of squats at ",
            "200 lb' or '10 min of running at 6 mph'.\n\n",
            "",
            "OnTrack uses a 'magnitude' value to help you compare different ",
            "Activity/Exercise Sessions when tracking performance. Each ",
            "Session's magnitude is calculated by multiplying it's effort ",
            "amount by its intensity amount. If during a Session you ",
            "perform 10 reps of some Exercise at 200 lb, the magnitude is ",
            "10 times 200, or 2000. Magnitudes do not have associated units ",
            "of measure.\n\n",
            "",
            "TAGS let you categorize similar Exercises using additional ",
            "labels. Enter into the Tags field as many different tags as ",
            "you want. Separate tags with commas, such as in 'Tag 1, Tag 2, ",
            "Tag 3'. It is recommended that tags be between 1-30 characters ",
            "long. You can also add an existing tag, available in the drop-",
            "down list under the Tags field.\n\n",
            "",
            "The Data Plotter tool lets you filter performance ",
            "results by Exercise tag. You might use tags to identify ",
            "types of Exercises (e.g. 'Cardio', 'Weightlifting'), types of ",
            "Exercise splits (e.g. 'Push', 'Pull'), or equipment ",
            "(e.g. 'Barbell', 'Machine')."])
        tipbox = organs.TipBox(self, [5, 322, 690, 100], text=tip_text)
        # Connect signals to slots.
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)
        self.favorite_bn.clicked.connect(self.toggle_favorite)
        self.add_tag_bn.clicked.connect(self.add_tag)
        # Set focus on the description field.
        self.description_field.setFocus()

    def accept(self):
        """Check for valid inputs and accept the dialog."""
        # Set focus on button box so that the input on the currently
        # selected field can be locked in prior to accepting the dialog.
        self.button_box.setFocus()
        description = str(self.description_field.text()).strip()
        # Check description field for input.
        if description == "":
            QtGui.QMessageBox.warning(
                self, "Missing Description",
                "You must enter a description for this Exercise!")
            self.description_field.setFocus()
            return
        # Check focus muscle selected.
        focusmuscle = str(self.focusmuscle_field.currentText())
        if focusmuscle == "-----MUSCLES-----":
            QtGui.QMessageBox.warning(
                self, "Missing Focus Muscle",
                "You must select a focus muscle!")
            return
        effort = str(self.effort_field.text()).strip()
        intensity = str(self.intensity_field.text()).strip()
        # Check for both performance metric units.
        if effort == "":
            QtGui.QMessageBox.warning(
                self, "Missing Effort Unit", "You must enter a measurement " +
                "unit for the performance metric 'effort'!")
            self.effort_field.setFocus()
            return
        if intensity == "":
            QtGui.QMessageBox.warning(
                self, "Missing Intensity Unit", "You must enter a " +
                "measurement unit for the performance metric 'intensity'!")
            self.intensity_field.setFocus()
            return
        # Parse tags from Tags Field and collect them in a list.
        tags_text = str(self.tags_field.text())
        all_tags = [
            tag.strip() for tag in tags_text.split(",") if tag.strip() != ""]
        # Check for repeated tags (case-insensitive).
        repeated_tags = set()
        for tag in all_tags:
            if all_tags.count(tag) > 1:
                repeated_tags.add(tag)
        if repeated_tags:
            bad_tags = ", ".join(sorted(list(repeated_tags)))
            repeated_string = "The tag"
            repeated_string += "s " if len(repeated_tags) > 1 else " "
            repeated_string += "'" + bad_tags + "' occur"
            repeated_string += " " if len(repeated_tags) > 1 else "s "
            repeated_string += "more than once. "
            repeated_string += "Only one instance of each tag will be saved."
            QtGui.QMessageBox.warning(
                self, "Repeated Tags", repeated_string)
        # Collect unique tags and sort alphabetically (case-insensitive).
        tags = sorted(list(set(all_tags)), key=lambda s: s.lower())
        if "-" * 14 + "ALL EXISTING TAGS" + "-" * 14 in tags:
            QtGui.QMessageBox.warning(
                self, "Invalid Tag",
                "Very funny. The tag '" + "-" * 14 + "ALL " + "EXISTING TAGS" +
                "-" * 14 + "' will be removed.")
            tags.remove("-" * 14 + "ALL EXISTING TAGS" + "-" * 14)
        # Check for tags longer than 30 characters.
        for tag in tags:
            if len(tag) > 30:
                choice = QtGui.QMessageBox.warning(
                    self, "Long Tag", "At least one tag is more than 30 " +
                    "characters long. It is recommended that you keep tag " +
                    "lengths to under 30 characters. Click 'Save' to keep " +
                    "tags as is. Click 'Cancel' to go back and make changes.",
                    QtGui.QMessageBox.Save | QtGui.QMessageBox.Cancel)
                if choice == QtGui.QMessageBox.Cancel:
                    return
            break
        # Update exercise attribute with properties.
        self.exercise.update_info({
            "description": description, "focusmuscle": focusmuscle,
            "units": [effort, intensity], "tags": tags})
        QtGui.QDialog.accept(self)

    def add_tag(self):
        """Add the selected existing tag to the Tags field."""
        selected_tag = str(self.existing_tags_field.currentText())
        # Check that an existing tag is selected.
        if selected_tag == "-" * 14 + "ALL EXISTING TAGS" + "-" * 14:
            QtGui.QMessageBox.warning(
                self, "No Tag Selected",
                "You must select an existing tag to add!")
            return
        # Parse tags from tags field and collect them in a list.
        tags_text = str(self.tags_field.text())
        all_tags = [
            tag.strip() for tag in tags_text.split(",") if tag.strip() != ""]
        # Check for selected tag already having been added to the tags field.
        if selected_tag in all_tags:
            QtGui.QMessageBox.warning(
                self, "Tag Already Exists",
                "The selected tag has already been added!")
            return
        # Update tags field with new tag.
        all_tags.append(selected_tag)
        new_tags_text = ", ".join(all_tags)
        self.tags_field.setText(new_tags_text)

    def toggle_favorite(self):
        """Toggle the Favorite button's icon."""
        if self.exercise.info("isfavorite"):
            self.favorite_bn.setIcon(organs.EasyIcon("heart"))
            self.exercise.set_property("isfavorite", False)
        else:
            self.favorite_bn.setIcon(organs.EasyIcon("heart_black"))
            self.exercise.set_property("isfavorite", True)


# -----------------------------------------------------------------------------
# Settings Class --------------------------------------------------------------

# noinspection PyUnusedLocal,PyAttributeOutsideInit
class InputSettings(organs.EasyDialog):
    """
    Class to edit application and user settings.

    InputSettings presents a dialog to the user with input fields for custom
    application settings. These fields are:

    --DEFAULT USER LOGIN--
        Default User: Current user that is automatically logged in at app start
    --APPLICATION BEHAVIOR FOR THIS USER--
        Ask Exit: Prompt the user to confirm exiting the application
        Ask Delete: Prompt the user to confirm item deletion
        Build Only: Update Build Info for build only or selected element
        Sort ID: Sort inventories by item ID or description
        Sort Up: Sort inventories in ascending or descending order
        Nutrients: Nutrients to display in Build Info and their order
        Muscles: Focus muscles to display in Build Info and their order

    InputSettings inherits all attributes and methods from its superclass. Its
    constructor is passed the parent GUI, the current AppState object, and the
    current user's User object to build a dialog. It implements default_user
    and settings attributes to store the user's inputs. The default_user
    attribute is assigned a username string and user_settings has the format:

        {'askdelete': bool, 'askexit': bool, 'buildonly': bool,
         'sortid': bool, 'sortup': bool, 'nutrients': list, 'muscles': list}

    This attribute can be passed to the user's update_settings method to change
    the user's settings and update the Profile.json file data. The default_user
    attribute can be passed to the appstate's set_default_user method to change
    the user who is logged in when the application is opened.

    The inherited accept method is overridden to check that all input field
    values are valid and accept the dialog. Methods are implemented to set up
    the dialog for a logged in user, update the Muscles Table, and update the
    Nutrients Table. Slot methods are implemented to evaluate Muscles Table
    changes and evaluate Nutrients Table changes.
    """

    def __init__(self, parent, appstate, user):
        """
        Initialize an InputSettings object.

        Assigns the appstate arg's default user default_user attribute and the
        user arg to the user attribute. Builds the dialog components and
        connects input field signals to slot methods.

        :param parent: Parent QMainWindow
        :type parent: QMainWindow
        :param appstate: The current app's AppState object
        :type appstate: AppState
        :param user: The current user's User object
        :type user: User
        """
        organs.EasyDialog.__init__(self, parent)
        self.default_user = appstate.default_user()
        self.user = user
        self.settings = {}
        # Window properties, button box, and outline frames.
        self.setWindowTitle("Settings")
        self.setWindowIcon(organs.EasyIcon("settings"))
        self._wd, height = 900, 630
        self.setFixedSize(self._wd, height)
        self.button_box = organs.EasyButtonBox(self)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)
        outline_a = organs.OutlineFrame(self, [5, 4, self._wd - 9, 56])
        outline_b = organs.OutlineFrame(self, [5, 70, self._wd - 9, 506])
        # Default User section.
        default_header = organs.EasyLabel(
            self, [10, 4, self._wd - 20, 26], text="DEFAULT USER LOGIN",
            font=FONT_TAG)
        def_txt = "".join([
            "Select any current user to be automatically logged in each time ",
            "OnTrack is opened."])
        default_dx = organs.EasyLabel(
            self, [10, 30, self._wd - 320, 26], text=def_txt, font=FONT_HEADER,
            alignment=QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.default_user_field = organs.EasyComboBox(
            self, [self._wd - 310, 30, 300, 22], items=appstate.users(),
            first_item="-" * 13 + "DO NOT LOG IN ANYONE" + "-" * 13)
        if self.default_user is not None and \
           self.default_user in appstate.users():
            self.default_user_field.setCurrentIndex(
                self.default_user_field.findText(self.default_user))
        # App Behavior section.
        application_header = organs.EasyLabel(
            self, [10, 70, self._wd - 20, 26], font=FONT_TAG,
            text="APPLICATION BEHAVIOR FOR THIS USER")
        # Set up dialog and user_settings attribute for the user.
        self.setup_dialog()

    def setup_dialog(self):
        """Set up the dialog for the user's settings."""
        # If no user is logged in, display a message and return.
        if self.user is None:
            no_user_tag = organs.EasyLabel(
                self, [10, 300, self._wd - 20, 26], font=FONT_HEADER,
                text="No user is currently logged in")
            return
        # Set up settings checkboxes.
        settings = self.user.settings()
        # Ask Exit checkbox.
        self.askexit_cb = QtGui.QCheckBox(self)
        self.askexit_cb.move(20, 100)
        self.askexit_cb.setChecked(settings["askexit"])
        askexit_text = "".join([
            "Check if you want to be asked for confirmation ",
            "before closing the OnTrack application window."])
        cb_wid = self.askexit_cb.width()
        askexit_tag = organs.EasyLabel(
            self, [cb_wid - 20, 96, self._wd - cb_wid, 26], text=askexit_text,
            font=FONT_HEADER,
            alignment=QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        # Ask Delete checkbox.
        self.askdelete_cb = QtGui.QCheckBox(self)
        self.askdelete_cb.move(20, 126)
        self.askdelete_cb.setChecked(settings["askdelete"])
        askdelete_text = "".join([
            "Check if you want to be asked for confirmation before deleting ",
            "an inventory item with the Inventory Manager."])
        askdelete_tag = organs.EasyLabel(
            self, [cb_wid - 20, 122, self._wd - cb_wid, 26],
            text=askdelete_text, font=FONT_HEADER,
            alignment=QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        # Build Only checkbox.
        self.buildonly_cb = QtGui.QCheckBox(self)
        self.buildonly_cb.move(20, 152)
        self.buildonly_cb.setChecked(settings["buildonly"])
        buildonly_text = "".join([
            "Check if you want the Build Info table to show data for the ",
            "entire build, uncheck to show data for the selected element."])
        buildonly_text = organs.EasyLabel(
            self, [cb_wid - 20, 148, self._wd - cb_wid, 26],
            text=buildonly_text, font=FONT_HEADER,
            alignment=QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        # Sort ID checkbox.
        self.sortid_cb = QtGui.QCheckBox(self)
        self.sortid_cb.move(20, 178)
        self.sortid_cb.setChecked(settings["sortid"])
        sortid_text = "".join([
            "Check if you want inventory items to be sorted by "
            "item ID by default, uncheck to sort by item description."])
        sortid_tag = organs.EasyLabel(
            self, [cb_wid - 20, 174, self._wd - cb_wid, 26], text=sortid_text,
            font=FONT_HEADER,
            alignment=QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        # Sort Up checkbox.
        self.sortup_cb = QtGui.QCheckBox(self)
        self.sortup_cb.move(20, 204)
        self.sortup_cb.setChecked(settings["sortup"])
        sortup_text = "".join([
            "Check if you want inventory items to be sorted in ascending "
            "order by default, uncheck to sort in descending order."])
        sortup_text = organs.EasyLabel(
            self, [cb_wid - 20, 200, self._wd - cb_wid, 26], text=sortup_text,
            font=FONT_HEADER,
            alignment=QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        # Set up nutrient and muscle tables.
        tab_txt = "".join([
            "Select which nutrients and focus muscles appear in the Build ",
            "Info Viewer and their order."])
        tables_tag = organs.EasyLabel(
            self, [10, 236, self._wd - 20, 26], text=tab_txt, font=FONT_HEADER)
        nut_tag = organs.EasyLabel(
            self, [46, 260, 330, 26], text="Nutrients", font=FONT_TAG)
        mus_tag = organs.EasyLabel(
            self, [542, 260, 200, 26], text="Muscles", font=FONT_TAG)
        mov_bn_txt = ["Move To Top", "Move Up", "Move Down", "Move To Bottom"]
        chk_bn_txt = [
            "Check All", "Uncheck All", "Use Original", "Use Defaults"]
        # Nutrients table.
        self.nut_table = organs.EasyTableWidget(
            self, [46, 282, 330, 284], column_header_hidden=True,
            row_height=28, grid_off=True, resize_off=True, select_rows=True,
            single_selection=True, stretch_last_section=True)
        chknuts = [dna.NUTRIENTS[nid][0] for nid in settings["nutrients"]]
        nuts = chknuts[:]
        for nid in dna.GUI_NUTRIENTS:
            if dna.NUTRIENTS[nid][0] not in nuts:
                nuts.append(dna.NUTRIENTS[nid][0])
        self.update_nutrient_table(nuts, chknuts)
        # Nutrients table buttons.
        self.nut_mapper = QtCore.QSignalMapper()
        for idx in range(4):
            bn_type = {
                0: ([378, 282 + (idx * 26), 110, 24], mov_bn_txt, 0),
                1: ([378, 464 + (idx * 26), 110, 24], chk_bn_txt, 4)}
            for bn_idx in range(2):
                button = organs.EasyToolButton(
                    self, bn_type[bn_idx][0], text=bn_type[bn_idx][1][idx],
                    button_type="action")
                self.nut_mapper.setMapping(button, idx + bn_type[bn_idx][2])
                button.clicked.connect(self.nut_mapper.map)
        self.nut_mapper.mapped[int].connect(self.eval_nutrients)
        # Muscles table.
        self.mus_table = organs.EasyTableWidget(
            self, [542, 282, 200, 284], column_header_hidden=True,
            row_height=28, grid_off=True, resize_off=True, select_rows=True,
            single_selection=True, stretch_last_section=True)
        chkmuss = settings["muscles"]
        muss = chkmuss[:] + [mus for mus in dna.MUSCLES if mus not in chkmuss]
        self.update_muscles_table(muss, chkmuss)
        # Muscle table buttons.
        self.mus_mapper = QtCore.QSignalMapper()
        for idx in range(4):
            bn_type = {
                0: ([744, 282 + (idx * 26), 110, 24], mov_bn_txt, 0),
                1: ([744, 464 + (idx * 26), 110, 24], chk_bn_txt, 4)}
            for bn_idx in range(2):
                button = organs.EasyToolButton(
                    self, bn_type[bn_idx][0], text=bn_type[bn_idx][1][idx],
                    button_type="action")
                self.mus_mapper.setMapping(button, idx + bn_type[bn_idx][2])
                button.clicked.connect(self.mus_mapper.map)
        self.mus_mapper.mapped[int].connect(self.eval_muscles)

    def accept(self):
        """Check for valid inputs and accept the dialog."""
        # Collect default user. Assign None to it if no username is selected.
        current_default = str(self.default_user_field.currentText())
        if current_default == "-" * 13 + "DO NOT LOG IN ANYONE" + "-" * 13:
            self.default_user = None
        else:
            self.default_user = current_default
        # Process remaining inputs if user is not None.
        if self.user is not None:
            valid_settings = {
                "askexit": self.askexit_cb.isChecked(),
                "askdelete": self.askdelete_cb.isChecked(),
                "buildonly": self.buildonly_cb.isChecked(),
                "sortid": self.sortid_cb.isChecked(),
                "sortup": self.sortup_cb.isChecked(),
                "nutrients": [],
                "muscles": []}
            # Collect checked nutrients in order and check for macros and
            # energy so that the user is viewing the most important nutrients.
            for row in range(self.nut_table.rowCount()):
                if self.nut_table.cellWidget(
                        row, 0).layout().itemAt(0).widget().isChecked():
                    nut_name = str(
                        self.nut_table.verticalHeaderItem(row).text())
                    for nid in dna.GUI_NUTRIENTS:
                        if nut_name == dna.NUTRIENTS[nid][0]:
                            valid_settings["nutrients"].append(nid)
            if not set(dna.MACROS.keys()) <= set(valid_settings["nutrients"]):
                QtGui.QMessageBox.warning(
                    self, "Missing Macronutrients",
                    "You must have the following nutrients checked:\n\n" +
                    "Energy, Protein, Fat, Carbohydrate")
                return
            # Collect checked muscles in order and check for at least one so
            # that the user is viewing some kind of muscle performance.
            for row in range(self.mus_table.rowCount()):
                if self.mus_table.cellWidget(
                        row, 0).layout().itemAt(0).widget().isChecked():
                    valid_settings["muscles"].append(
                        str(self.mus_table.verticalHeaderItem(row).text()))
            if len(valid_settings["muscles"]) < 1:
                QtGui.QMessageBox.warning(
                    self, "Missing Muscles",
                    "You must check at least one focus muscle!")
                return
            self.settings = valid_settings
        QtGui.QDialog.accept(self)

    def eval_muscles(self, action_num):
        """
        Determine muscle changes and call update_muscles_table method.

        :param action_num: Action number: 0-Move To Top, 1-Move Up, 2-Move
            Down, 3-Move To Bottom, 4-Check All, 5-Uncheck All, 6-Use Original,
            7-Use Defaults
        :type action_num: int
        """
        curr_row = self.mus_table.currentRow()
        # Return if no item is selected and a move button is clicked.
        if curr_row == -1 and action_num in range(4):
            return
        # Capture all checked rows to reorganize muscles.
        muss = []
        chkmuss = []
        for row in range(self.mus_table.rowCount()):
            mus_name = str(self.mus_table.verticalHeaderItem(row).text())
            muss.append(mus_name)
            if self.mus_table.cellWidget(
                    row, 0).layout().itemAt(0).widget().isChecked():
                chkmuss.append(mus_name)
        # Determine row to select and rearrange names.
        select_row = 0 if action_num in range(4, 8) else None
        if action_num == 0:
            if curr_row == 0:
                return
            muss.insert(0, muss.pop(curr_row))
            select_row = 0
        elif action_num == 1:
            if curr_row == 0:
                return
            idx = curr_row - 1
            muss.insert(idx, muss.pop(curr_row))
            select_row = idx
        elif action_num == 2:
            if curr_row == len(muss) - 1:
                return
            idx = curr_row + 1
            muss.insert(idx, muss.pop(curr_row))
            select_row = idx
        elif action_num == 3:
            if curr_row == len(muss) - 1:
                return
            muss.insert(len(muss) - 1, muss.pop(curr_row))
            select_row = len(muss) - 1
        elif action_num == 4:
            chkmuss = muss
        elif action_num == 5:
            chkmuss = []
        elif action_num == 6:
            chkmuss = self.user.settings()["muscles"]
            muss = chkmuss[:]
            muss += [mus for mus in dna.MUSCLES if mus not in chkmuss]
        elif action_num == 7:
            chkmuss = dna.MUSCLES
            muss = chkmuss
        self.update_muscles_table(muss, chkmuss, select_row)

    def eval_nutrients(self, action_num):
        """
        Determine nutrients changes and call update_nutrients_table method.

        :param action_num: Action number: 0-Move To Top, 1-Move Up, 2-Move
            Down, 3-Move To Bottom, 4-Check All, 5-Uncheck All, 6-Use Original,
            7-Use Defaults
        :type action_num: int
        """
        curr_row = self.nut_table.currentRow()
        # Return if no item is selected and a move button is clicked.
        if curr_row == -1 and action_num in range(4):
            return
        # Capture all checked rows to reorganize nutrients.
        nuts = []
        chknuts = []
        for row in range(self.nut_table.rowCount()):
            nut_name = str(self.nut_table.verticalHeaderItem(row).text())
            nuts.append(nut_name)
            if self.nut_table.cellWidget(
                    row, 0).layout().itemAt(0).widget().isChecked():
                chknuts.append(nut_name)
        # Determine row to select and rearrange names.
        select_row = 0 if action_num in range(4, 8) else None
        if action_num == 0:
            if curr_row == 0:
                return
            nuts.insert(0, nuts.pop(curr_row))
            select_row = 0
        elif action_num == 1:
            if curr_row == 0:
                return
            idx = curr_row - 1
            nuts.insert(idx, nuts.pop(curr_row))
            select_row = idx
        elif action_num == 2:
            if curr_row == len(nuts) - 1:
                return
            idx = curr_row + 1
            nuts.insert(idx, nuts.pop(curr_row))
            select_row = idx
        elif action_num == 3:
            if curr_row == len(nuts) - 1:
                return
            nuts.insert(len(nuts) - 1, nuts.pop(curr_row))
            select_row = len(nuts) - 1
        elif action_num == 4:
            chknuts = nuts
        elif action_num == 5:
            chknuts = []
        elif action_num == 6:
            chknuts = [dna.NUTRIENTS[nid][0] for nid in
                       self.user.settings()["nutrients"]]
            nuts = chknuts[:]
            for nid in dna.GUI_NUTRIENTS:
                if dna.NUTRIENTS[nid][0] not in nuts:
                    nuts.append(dna.NUTRIENTS[nid][0])
        elif action_num == 7:
            chknuts = [dna.NUTRIENTS[nid][0] for nid in dna.GUI_NUTRIENTS]
            nuts = chknuts
        self.update_nutrient_table(nuts, chknuts, select_row)

    def update_muscles_table(self, muscles, checked, selected_row=None):
        """
        Update the Muscles Table with the current settings.

        :param muscles: All muscles in the correct order
        :type muscles: list
        :param checked: All muscles to mark as checked
        :type checked: list
        :param selected_row: The row number which to select
        :type selected_row: int
        """
        self.mus_table.setRowCount(0)
        self.mus_table.setColumnCount(0)
        self.mus_table.clear()
        self.mus_table.setColumnCount(1)
        self.mus_table.setRowCount(len(muscles))
        self.mus_table.setVerticalHeaderLabels(muscles)
        for row in range(self.mus_table.rowCount()):
            # This item is necessary to scroll when a row is moved.
            item = QtGui.QTableWidgetItem()
            self.mus_table.setItem(row, 0, item)
            # Cell widget -> layout -> item -> widget...to access checkbox.
            mus_widget = QtGui.QWidget()
            mus_hlayout = QtGui.QHBoxLayout(mus_widget)
            mus_hlayout.setAlignment(QtCore.Qt.AlignCenter)
            mus_hlayout.setContentsMargins(0, 0, 0, 0)
            mus_cb = QtGui.QCheckBox()
            if str(self.mus_table.verticalHeaderItem(row).text()) in checked:
                mus_cb.setChecked(True)
            mus_hlayout.addWidget(mus_cb)
            self.mus_table.setCellWidget(row, 0, mus_widget)
        QtGui.QApplication.processEvents()
        if selected_row is not None:
            self.mus_table.scrollToItem(
                self.mus_table.item(selected_row, 0),
                QtGui.QAbstractItemView.PositionAtCenter)
            self.mus_table.selectRow(selected_row)

    def update_nutrient_table(self, nutrients, checked, selected_row=None):
        """
        Update the Nutrient Table with the current settings.

        :param nutrients: All nutrients in the correct order
        :type nutrients: list
        :param checked: All nutrients to mark as checked
        :type checked: list
        :param selected_row: The row to select
        :type selected_row: int
        """
        self.nut_table.setRowCount(0)
        self.nut_table.setColumnCount(0)
        self.nut_table.clear()
        self.nut_table.setColumnCount(1)
        self.nut_table.setRowCount(len(nutrients))
        self.nut_table.setVerticalHeaderLabels(nutrients)
        for row in range(self.nut_table.rowCount()):
            # This item is necessary to scroll when a row is moved.
            item = QtGui.QTableWidgetItem()
            self.nut_table.setItem(row, 0, item)
            # Cell widget -> layout -> item -> widget...to access checkbox.
            nut_widget = QtGui.QWidget()
            nut_hlayout = QtGui.QHBoxLayout(nut_widget)
            nut_hlayout.setAlignment(QtCore.Qt.AlignCenter)
            nut_hlayout.setContentsMargins(0, 0, 0, 0)
            nut_cb = QtGui.QCheckBox()
            if str(self.nut_table.verticalHeaderItem(row).text()) in checked:
                nut_cb.setChecked(True)
            nut_hlayout.addWidget(nut_cb)
            self.nut_table.setCellWidget(row, 0, nut_widget)
        QtGui.QApplication.processEvents()
        if selected_row is not None:
            self.nut_table.scrollToItem(
                self.nut_table.item(selected_row, 0),
                QtGui.QAbstractItemView.PositionAtCenter)
            self.nut_table.selectRow(selected_row)

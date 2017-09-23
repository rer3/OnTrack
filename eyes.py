#!/usr/bin/env python2.7
"""
This module contains functions and classes to analyze and plot user data.
----------
The objects in this module are used by the Data Plotter tool to analyze user
data sets, such as the Health Diary or Program record objects, and plot them.
The functions take source data and converts them into lists of x- and y-coords
that can be plotted by the plotting classes. Plotting classes implement
matplotlib objects to draw plots on a canvas.
----------
Constants: colors, fonts, and attributes used by plotting classes.
    COLOR_LINES: Hex code of line plot line color
    COLOR_MACROPROP: List of hex codes of macro proportion plot colors
    COLOR_PROGRAM: Hex code of Program start vertical line color
    COLOR_TARGET: Hex code of nutrient target horizontal line color
    FONT_ACTION: QFont object for Plot Data action button
    FONT_TAG: QFont object for field description tags

Processing Functions: functions to analyze user data and return lists of x-
and y-coordinates that can be used by a plotting class to plot data.
    process_health_metrics: function to process Health Diary data
    process_nutrient_targets: function to process Nutrient Guide data
    process_macro_proportions: function to process macronutrient weights
    process_meal_times: function to process Meal times
    process_nutrient_values: function process nutrient values
    process_performance_results: function to process performance results
    process_workout_periods: function to process Workout period datetimes
    time_float: function to return the float value of a time string

Plotting Classes: classes to plot user data that has been analyzed and
transformed by the processing functions.
    MatNavTool: NavigationToolbar subclass with custom toolbar buttons
    EasyPlot: EasyDialog subclass and plotting dialog superclass
    PlotHealthDiary: EasyPlot subclass to plot health metric measurements
    PlotNutrientGuide: EasyPlot subclass to plot nutrient target values
    PlotMacroProportions: EasyPlot subclass to plot macronutrient proportions
    PlotMealTimes: EasyPlot subclass to plot Meal times
    PlotNutrientValues: EasyPlot subclass to plot nutrient values
    PlotPerformance: EasyPlot subclass to plot performance results per property
    PlotWorkoutPeriods: EasyPlot subclass to plot Workout periods
"""


import datetime
import sys

import matplotlib.dates as mdates
from matplotlib.backends.backend_qt4agg import (
    FigureCanvasQTAgg as FigureCanvas,
    NavigationToolbar2QT as NavigationToolbar)
from matplotlib.figure import Figure
from PyQt4 import QtCore
from PyQt4 import QtGui

import album
import dna
import organs


# -----------------------------------------------------------------------------
# Constants -------------------------------------------------------------------

COLOR_LINES = "#0BB0DC"
COLOR_MACROPROP = ["#ffa4ae", "#e7e538", "#bdbef1"]
COLOR_PROGRAM = "#F33A6F"
COLOR_TARGET = "#E31F69"
FONT_ACTION = FONT_TAG = organs.arial_small


# -----------------------------------------------------------------------------
# Processing Functions --------------------------------------------------------

def process_health_metrics(health_diary, first_date, last_date, metric):
    """
    Return a health metric measurements data set that can be plotted.

    This function iterates over the user's Health Diary entries to find all
    entry dates between the first_date and last_date args that include the
    metric arg and determines the measurement. The Health Diary is in the
    format:

        {entry date: {health metric: measurement value, ...}, ...}

    Returns a tuple with an x-coord list with all applicable entry dates, as
    datetime.date objects, and a y-coord list with corresponding health metric
    measurements. These lists are in the format:

    --X: Entry Dates--
        [first entry date, second entry date, ...]
    --Y: Health Metric Measurements--
        [first date measurement, second date measurement, ...]

    Health metric measurements are displayed in a line plot.

    :param health_diary: The user's Health Diary
    :type health_diary: dict
    :param first_date: The earliest Health Diary entry date to process
    :type first_date: QDate
    :param last_date: The latest Health Diary entry date to process
    :type last_date: QDate
    :param metric: A health metric
    :type metric: str
    :return: Clean data in the format: (entry dates list, health metric
        measurements list)
    :rtype: tuple
    """
    # Convert first/last dates to datetime.date strings to compare with Health
    # Diary keys, then convert back to datetime.date for use of mdates.
    first = first_date.toPyDate().strftime("%Y-%m-%d")
    last = last_date.toPyDate().strftime("%Y-%m-%d")
    result_dates = []
    result_measurements = []
    sorted_entry_dates = sorted(health_diary.keys())
    for date in sorted_entry_dates:
        if first <= date <= last and metric in health_diary[date]:
            result_dates.append(
                datetime.datetime.strptime(date, "%Y-%m-%d").date())
            result_measurements.append(health_diary[date][metric])
    return result_dates, result_measurements


def process_nutrient_targets(
        nutrient_guide, first_date, last_date, nutrient_id):
    """
    Return a nutrient targets data set that can be plotted.

    This function iterates over the user's Nutrient Guide to find all effective
    dates between the first_date and last_date args that include the
    nutrient_id arg and determines the target. The Nutrient Guide is in the
    format:

        {effective date: {nutrient ID: target value, ...}, ...}

    Returns a tuple with an x-coord list with all applicable effective dates,
    as datetime.date objects, and a y-coord list with corresponding nutrient
    target values. These lists are in the format:

    --X: Effective Dates--
        [first effective date, second effective date, ...]
    --Y: Target Nutrient Values--
        [first date target, second date target, ...]

    Nutrient targets are displayed in a line plot.

    :param nutrient_guide: The user's Nutrient Guide
    :type nutrient_guide: dict
    :param first_date: The earliest Nutrient Guide effective date to process
    :type first_date: QDate
    :param last_date: The latest Nutrient Guide effective date to process
    :type last_date: QDate
    :param nutrient_id: A nutrient ID
    :type nutrient_id: str
    :return: Clean data in the format: (effective dates list,
        target nutrient values list)
    :rtype: tuple
    """
    # Convert first/last dates to datetime.date strings to compare with Nut
    # Guide keys, then convert back to datetime.date for use of mdates.
    first = first_date.toPyDate().strftime("%Y-%m-%d")
    last = last_date.toPyDate().strftime("%Y-%m-%d")
    result_dates = []
    result_targets = []
    sorted_effective_dates = sorted(nutrient_guide.keys())
    for date in sorted_effective_dates:
        if first <= date <= last and nutrient_id in nutrient_guide[date]:
            result_dates.append(
                datetime.datetime.strptime(date, "%Y-%m-%d").date())
            result_targets.append(nutrient_guide[date][nutrient_id])
    return result_dates, result_targets


def process_macro_proportions(diet_objects, first_date, last_date):
    """
    Return a macronutrient proportions data set that can be plotted.

    This function iterates over the user's Diet record objects to find all
    record IDs (Diet dates) between the first_date and last_date args, calls
    each applicable Diet's macro_weights method to determine macronutrient gram
    weights, and calculates the relative proportions of each based on caloric
    value. Macro weights are in the format:

        {'203': protein weight, '204': fat weight, '205': carbohydrate weight}

    Returns a tuple with an x-coord list with all applicable Diet dates, as
    datetime.date objects, and three y-coord lists with corresponding protein,
    fat, and carbohydrate proportions as percentages of the total caloric value
    of the Diet. These lists are in the format:

    --X: Diet Dates--
        [first Diet date, second Diet date, ...]
    --Y1: Protein Percentages--
        [first date percentage, second date percentage, ...]
    --Y2: Fat Percentages--
        [first date percentage, second date percentage, ...]
    --Y3: Carbohydrate Percentages--
        [first date percentage, second date percentage, ...]

    Macronutrient proportions are displayed in a stack plot.

    :param diet_objects: The user's Diet record objects
    :type diet_objects: dict
    :param first_date: The earliest Diet date to process
    :type first_date: QDate
    :param last_date: The latest Diet date to process
    :type last_date: QDate
    :return: Clean data in the format: (Diet dates list, protein percentages
        list, fat percentages list, carbohydrate percentages list)
    :rtype: tuple
    """
    # Convert first/last dates to datetime.date strings to compare with Diet
    # record item IDs, then convert back to datetime.date for use of mdates.
    first = first_date.toPyDate().strftime("%Y-%m-%d")
    last = last_date.toPyDate().strftime("%Y-%m-%d")
    result_dates = []
    result_p = []
    result_f = []
    result_c = []
    sorted_diet_dates = sorted(diet_objects.keys())
    for date in sorted_diet_dates:
        if first <= date <= last:
            result_dates.append(
                datetime.datetime.strptime(date, "%Y-%m-%d").date())
            # Convert weights to energy values and find total energy value.
            # Note that prot/fat/carb calories per gram are 4/9/4 respectively.
            weights = diet_objects[date].macro_weights()
            p_energy = weights["203"] * 4
            f_energy = weights["204"] * 9
            c_energy = weights["205"] * 4
            total_energy = float(p_energy + f_energy + c_energy)
            # Check for zero total energy and DO NOT divide by zero. Save all
            # proportions as zero and move onto the next date.
            if total_energy <= 0:
                for result_list in [result_p, result_f, result_c]:
                    result_list.append(0)
                continue
            # Calculate percentages for prot and fat from their energies. Find
            # carb % by difference--typical method of doing so in the lab, plus
            # ensures that all % values equal 100.
            p_pct = (p_energy / total_energy) * 100
            f_pct = (f_energy / total_energy) * 100
            c_pct = max(100 - p_pct - f_pct, 0)
            result_p.append(p_pct)
            result_f.append(f_pct)
            result_c.append(c_pct)
    return result_dates, result_p, result_f, result_c


def process_meal_times(diet_objects, first_date, last_date):
    """
    Return a Meal times data set that can be plotted.

    This function iterates over the user's Diet record objects to find all
    record IDs (Diet dates) between the first_date and last_date args, calls
    each applicable Diet's meal_times method to determine Meal times, and
    converts each time to a float in the half-open interval [0, 24). Meal times
    are initially time strings in 24-hour clock time, such as '13:45' (the same
    as 1:45 PM), in a list with the format:

        [earliest Meal time, next Meal time, ..., latest Meal time]

    Returns a tuple with an x-coord list with all applicable Diet dates, as
    datetime.date objects, and a y-coord list with lists of converted Meal
    times for each Diet. These lists are in the format:

    --X: Diet Dates--
        [first Diet date, second Diet date, ...]
    --Y: Meal Times--
        [[first date first time, first date second time, ...],
         [second date first time, second date second time, ...], ...]

    Meal times are displayed in a series of separated line plots, one per date.

    :param diet_objects: The user's Diet record objects
    :type diet_objects: dict
    :param first_date: The earliest Diet date to process
    :type first_date: QDate
    :param last_date: The latest Diet date to process
    :type last_date: QDate
    :return: Clean data in the format: (Diet dates list, Meal times list of
        lists)
    :rtype: tuple
    """
    # Convert first/last dates to datetime.date strings to compare with Diet
    # record item IDs, then convert back to datetime.date for use of mdates.
    first = first_date.toPyDate().strftime("%Y-%m-%d")
    last = last_date.toPyDate().strftime("%Y-%m-%d")
    result_dates = []
    result_times = []
    sorted_diet_dates = sorted(diet_objects.keys())
    for date in sorted_diet_dates:
        if first <= date <= last:
            result_dates.append(
                datetime.datetime.strptime(date, "%Y-%m-%d").date())
            result_times.append(
                [time_float(time) for time in diet_objects[date].meal_times()])
    return result_dates, result_times


def process_nutrient_values(diet_objects, first_date, last_date, nutrient_id):
    """
    Return a nutrient values data set that can be plotted.

    This function iterates over the user's Diet record objects to find all
    record IDs (Diet dates) between the first_date and last_date arg and calls
    each applicable Diet's nutrient_value method to determine the value of the
    nutrient_id arg for that Diet. Returns a tuple with an x-coord list with
    all applicable Diet dates, as datetime.date objects, and a y-coord list
    with corresponding nutrient values. These lists are in the format:

    --X: Diet Dates--
        [first Diet date, second Diet date, ...]
    --Y: Nutrient Values--
        [first date value, second date value, ...]

    Nutrient values are displayed in a line plot.

    :param diet_objects: The user's Diet record objects
    :type diet_objects: dict
    :param first_date: The earliest Diet date to process
    :type first_date: QDate
    :param last_date: The latest Diet date to process
    :type last_date: QDate
    :param nutrient_id: A nutrient ID
    :type nutrient_id: str
    :return: Clean data in the format: (Diet dates list, nutrient values list)
    :rtype: tuple
    """
    # Convert first/last dates to datetime.date strings to compare with Diet
    # record item IDs, then convert back to datetime.date for use of mdates.
    first = first_date.toPyDate().strftime("%Y-%m-%d")
    last = last_date.toPyDate().strftime("%Y-%m-%d")
    result_dates = []
    result_values = []
    sorted_diet_dates = sorted(diet_objects.keys())
    for date in sorted_diet_dates:
        if first <= date <= last:
            result_dates.append(
                datetime.datetime.strptime(date, "%Y-%m-%d").date())
            result_values.append(
                diet_objects[date].nutrient_value(nutrient_id))
    return result_dates, result_values


def process_performance_results(
        program_objects, first_date, last_date, results_type,
        exercise_property, property_value):
    """
    Return a performance results data set that can be plotted.

    This function iterates over the user's Program record objects to find all
    Programs with constituent Workout period began dates between the first_date
    and last_date args. Calls each applicable Program's performance_results
    method with the results_type and exercise_property args to determine the
    performance results. Determines which results apply to only the Exercise
    property value specified by the property_value arg. The performance results
    dict is in the format:

        {Workout period began: {
            Exercise property: result value for all Sessions, ...}, ...}

    Returns a tuple with an x-coord list with all applicable Workout period
    began dates, a y-coord list with corresponding performance result values
    for the specified Exercise property value, and an x-coord list with all
    Program start dates found within the specified date range. These lists are
    n the format:

    --X: Workout Period Began Dates--
        [first Workout began date, second Workout began date, ...]
    --Y: Performance Result Values--
        [first date value, second date value, ...]
    --X(vertical lines): Program Start Dates--
        [first Program start, second Program start, ...]

    Performance results are displayed in a line plot. Program start dates are
    shown as vertical lines intersecting the corresponding x-axis date values.

    :param program_objects: The user's Program record objects
    :type program_objects: dict
    :param first_date: The earliest constituent Workout began date to process
    :type first_date: QDate
    :param last_date:The latest constituent Workout began date to process
    :type last_date: QDate
    :param results_type: The type of performance results: 'effort' for total
        effort sum, 'intensity' for maximum intensity, 'magnitude' for total
        magnitude sum
    :type results_type: str
    :param exercise_property: The Exercise property to which performance
        results are mapped: 'itemid' for Exercise item ID, 'focusmuscle' for
        focus muscle, 'tags' for tags
    :type exercise_property: str
    :param property_value: An Exercise ID, focus muscle, or tag
    :type property_value: str
    :return: Clean data in the format: (Workout began dates list, performance
        results for property value list, Program start dates list)
    :rtype: tuple
    """
    # Convert first/last dates to datetime.date strings to compare with Program
    # record item IDs and Workout period began dates, then convert back to
    # datetime.date for use of mdates.
    first = first_date.toPyDate().strftime("%Y-%m-%d")
    last = last_date.toPyDate().strftime("%Y-%m-%d")
    result_dates = []
    result_values = []
    result_starts = []
    sorted_starts = sorted(program_objects.keys())
    for start in sorted_starts:
        if first <= start <= last:
            result_starts.append(
                datetime.datetime.strptime(start, "%Y-%m-%d").date())
        perf_results = program_objects[start].performance_results(
            results_type, exercise_property)
        sorted_begans = sorted(perf_results.keys())
        for began in sorted_begans:
            began_date = began[:10]
            if (first <= began_date <= last and
               property_value in perf_results[began]):
                result_dates.append(
                    datetime.datetime.strptime(began_date, "%Y-%m-%d").date())
                result_values.append(perf_results[began][property_value])
    return result_dates, result_values, result_starts


def process_workout_periods(program_objects, first_date, last_date):
    """
    Return a Workout periods data set that can be plotted.

    This function iterates over the user's Program record objects to find all
    record IDs (Program start dates) between the first_date and last_date args,
    calls each applicable Program's workout_periods method to determine Workout
    periods, and converts each period's began and ended time to floats in the
    closed interval [0, 24]. Workout periods are initially datetime strings in
    24-hour clock time, such as '2017-02-14 13:45' (the same as 1:45 PM on
    February 14, 2017), in a dict with the format:

        {Workout began datetime: Workout ended datetime, ...}

    Returns a tuple with an x-coord list with all applicable Workout period
    began dates--added once for each began and ended time linked to that date,
    a y-coord list with converted began and ended times for each Workout, and
    an x-coord list with all Program start dates found within the specified
    date range. These lists are in the format:

    --X: Workout Period Began Dates--
        [first Workout began date, first Workout began date,
         second Workout began date, second Workout began date...]
    --Y: Workout Periods--
        [first date began time, first date ended time,
         second date began time, second date ended time, ...]
    --X(vertical lines): Program Start Dates--
        [first Program start, second Program start, ...]

    Workout periods are displayed in a series of separated line plots, one per
    period or partial period. If a period spans multiple dates, such as one
    beginning prior to and ended after 12:00 AM, an additional set of began and
    ended times is calculated--this behavior is extended for all dates over
    which a period occurs. Program start dates are shown as vertical lines
    intersecting the corresponding x-axis date values.

    :param program_objects: The user's Program record objects
    :type program_objects: dict
    :param first_date: The earliest constituent Workout began date to process
    :type first_date: QDate
    :param last_date: The latest constituent Workout began date to process
    :type last_date: QDate
    :return: Clean data in the format: (Workout period began dates list,
        Workout period began and ended times list, Program start dates list)
    :rtype: tuple
    """
    # Convert first/last dates to datetime.date strings to compare with Program
    # record item IDs, then convert back to datetime.date for use of mdates.
    first = first_date.toPyDate().strftime("%Y-%m-%d")
    last = last_date.toPyDate().strftime("%Y-%m-%d")
    result_dates = []
    result_times = []
    result_starts = []
    sorted_starts = sorted(program_objects.keys())
    for start in sorted_starts:
        if first <= start <= last:
            result_starts.append(
                datetime.datetime.strptime(start, "%Y-%m-%d").date())
        periods = program_objects[start].workout_periods()
        sorted_begans = sorted(periods.keys())
        for began in sorted_begans:
            began_date = began[:10]
            if first <= began_date <= last:
                # Determine began and ended dates and times, create equivalent
                # datetime.date objects, collect first set of data points.
                began_time = began[11:]
                ended_date = periods[began][:10]
                ended_time = periods[began][11:]
                began_date_obj = datetime.datetime.strptime(
                    began_date, "%Y-%m-%d")
                ended_date_obj = datetime.datetime.strptime(
                    ended_date, "%Y-%m-%d")
                result_dates.append(began_date_obj)
                result_times.append(time_float(began_time))
                # Determine for how many days this period spans and append
                # the appropriate number of 24/0 time values, linked to the
                # applicable dates, to the data sets.
                num_days = (ended_date_obj - began_date_obj).days
                if num_days == 0:
                    result_dates.append(began_date_obj)
                    result_times.append(time_float(ended_time))
                else:
                    result_dates.append(began_date_obj)
                    result_times.append(24)
                    next_date = began_date_obj + datetime.timedelta(1)
                    result_dates.append(next_date)
                    result_times.append(0)
                    for day in range(num_days - 1):
                        result_dates.append(next_date)
                        result_times.append(24)
                        next_date += datetime.timedelta(1)
                        result_dates.append(next_date)
                        result_times.append(0)
                    result_dates.append(next_date)
                    result_times.append(time_float(ended_time))
    return result_dates, result_times, result_starts


def time_float(time_string):
    """
    Returns the float value of a time string.

    :param time_string: A time string in the format 'HH:MM'
    :type time_string str
    :return: Float value of the time string
    :rtype: float
    """
    time_split = time_string.split(":")
    hour = int(time_split[0])
    minute = int(time_split[1]) / 60.0
    return hour + minute


# -----------------------------------------------------------------------------
# Plotting Classes ------------------------------------------------------------

class CustomNav(NavigationToolbar):
    """
    Class to build a plot navigation toolbar with custom buttons.

    CustomNav is used by the EasyPlot class to display a custom set of plot
    navigation toolbar buttons: pan and save. All other toolbar buttons are
    removed to provide additional space in the toolbar for custom fields. A
    method is implemented to remove all actions from the toolbar.
    """

    def __init__(self, canvas, parent):
        """
        Initialize a CustomNav object.

        Iterates over the navigation toolbar actions and removes all but the
        pan and save.

        :param canvas: Figure canvas for which the toolbar is implemented
        :type canvas: FigureCanvas
        :param parent: Parent EasyPlot object
        :type parent: EasyPlot
        """
        NavigationToolbar.__init__(self, canvas, parent)
        actions = self.findChildren(QtGui.QAction)
        for action in actions:
            idx = actions.index(action)
            if idx in range(6) + range(7, 11):
                self.removeAction(action)

    def clear_actions(self):
        """Remove all actions from the toolbar."""
        for action in self.findChildren(QtGui.QAction):
            self.removeAction(action)


class EasyPlot(organs.EasyDialog):
    """
    Base class for plotting processed data sets.

    EasyPlot presents a dialog to the user with input fields for data plotting
    customization. Each subclass of EasyPlot implements its own input fields
    based on the type of data being plotted. These fields are:

    --All Subclasses--
        First Date: The earliest date in the source data to process
        Last Date: The latest date in the source data to process
    --PlotHealthDiary--
        Health Metric: The health metric for which to plot measurements
    --PlotNutrientGuide--
        Nutrient: The nutrient for which to plot target values
    --PlotNutrientValues--
        Nutrient: The nutrient for which to plot values
    --PlotPerformance--
        Results Type: The type of performance results to plot
        --Exercise Property 'itemid'--
            Exercise: The Exercise for which results are plotted
        --Exercise Property 'focusmuscle'--
            Focus Muscle: The focus muscle for which results are plotted
        --Exercise Property 'tags'--
            Tag: The tag for which results are plotted

    EasyPlot inherits all attributes and methods from its superclass. Its
    constructor is passed the parent GUI, source data, and a processor function
    from this module. The source_data arg is one of the user's primary data
    sets: Health Diary, Nutrient Guide, Diet record objects, and Program record
    objects. The processor_func arg is the function that specifically handles
    that source data to return the relevant processed data.

    EasyPlot implements a sourcedata attribute to store the source_data arg and
    passes the processor_func arg to the DataProcessor object assigned to its
    processor attribute. Additional attributes are implemented to store the
    figure, canvas, toolbar, processing message dialog, First Date Field, Last
    Last Date Field, and Plot button. Subclasses will add the Plot button to
    the toolbar only after all other fields have been added. This ensures that
    the Plot button is located in the same place--to the far right--in every
    subclass's toolbar. Slot methods are implemented to verify that the date
    range is valid, process the source data based on the field inputs, and plot
    the processed data emitted by the processor attribute. Placeholder methods
    clear_plots and update_processor are overridden by subclasses. An ondraw
    method is implemented to check for a valid minimum date (an arbitrary date
    in early 1900s) and avoid Year Zero plotting errors by closing the window.
    """

    def __init__(self, parent, source_data, processor_func):
        """
        Initialize an EasyPlot object.

        Assigns the source_data arg to the sourcedata attribute, a Figure
        object to the figure attribute, a FigureCanvas object to the canvas
        attribute, a CustomNav object to the toolbar attribute, a
        DataProcessor object to the processor attribute, and None to the
        proc_msg attribute. Builds the dialog components and connects input
        field signals to slot methods.

        :param parent: Parent QMainWindow
        :type parent: QMainWindow
        :param source_data: Source data from the user: Health Diary, Nutrient
            Guide, Diet record objects, Program record objects
        :type source_data: dict
        :param processor_func: Function to process source data and return data
            sets with x- and y-coordinate values that can be plotted
        :type processor_func: function
        """
        organs.EasyDialog.__init__(self, parent)
        # Delete on close to clear from memory.
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.sourcedata = source_data
        self.figure = Figure(facecolor="#F0F0F0")
        self.canvas = FigureCanvas(self.figure)
        self.canvas.mpl_connect('draw_event', self.ondraw)
        self.toolbar = CustomNav(self.canvas, self)
        self.processor = organs.DataProcessor(self, processor_func)
        self.proc_msg = None
        # Window properties and vertical layout with toolbar and canvas.
        self.setMinimumSize(1300, 800)
        self.setWindowIcon(organs.EasyIcon(dna.ICONS["plot"]))
        vbox = QtGui.QVBoxLayout(self)
        vbox.addWidget(self.toolbar)
        vbox.addWidget(self.canvas)
        self.setLayout(vbox)
        # Plot button (do not add to toolbar yet).
        self.plot_bn = organs.EasyToolButton(
            self, [-100, -100, 120, 24], fixed_size=True, text="PLOT DATA",
            font=FONT_ACTION, button_type="action")
        # Find min and max possible dates in source data. All potential sources
        # have date strings ("2017-01-01") as keys.
        first_date = datetime.datetime.strptime(
            organs.min_key(source_data), "%Y-%m-%d").date()
        last_date = datetime.datetime.strptime(
            organs.max_key(source_data), "%Y-%m-%d").date()
        # First Date section.
        first_tag = organs.EasyLabel(
            self, [0, 0, 80, 26], fixed_size=True, text="First Date:",
            font=FONT_TAG)
        self.first_field = organs.EasyDateEdit(
            self, [0, 0, 100, 22], display_format="yyyy-MM-dd",
            date=[first_date.year, first_date.month, first_date.day],
            minimum_date=[first_date.year, first_date.month, first_date.day],
            maximum_date=[last_date.year, last_date.month, last_date.day],
            calendar_on=True)
        self.toolbar.addWidget(first_tag)
        self.toolbar.addWidget(self.first_field)
        space = organs.EasyLabel(self, [0, 0, 10, 26], fixed_size=True)
        self.toolbar.addWidget(space)
        # Last Date section.
        last_tag = organs.EasyLabel(
            self, [0, 0, 80, 26], fixed_size=True, text="Last Date:",
            font=FONT_TAG)
        self.last_field = organs.EasyDateEdit(
            self, [0, 0, 100, 22], display_format="yyyy-MM-dd",
            date=[last_date.year, last_date.month, last_date.day],
            minimum_date=[first_date.year, first_date.month, first_date.day],
            maximum_date=[last_date.year, last_date.month, last_date.day],
            calendar_on=True)
        self.toolbar.addWidget(last_tag)
        self.toolbar.addWidget(self.last_field)
        space = organs.EasyLabel(self, [0, 0, 10, 26], fixed_size=True)
        self.toolbar.addWidget(space)
        # Connect signals to slots.
        self.first_field.dateChanged.connect(self.check_dates)
        self.last_field.dateChanged.connect(self.check_dates)
        self.plot_bn.clicked.connect(self.process_data)
        self.processor.data_processed.connect(self.plot_processed_data)

    def check_dates(self):
        """
        Verify that the date range is valid and toggle the Plot button.

        Verifies that the Last Date Field input occurs on a date after the
        First Date Field input. Enables the Plot button if the date range is
        valid, otherwise disables it and warns the user.
        """
        if self.first_field.date() > self.last_field.date():
            self.plot_bn.setEnabled(False)
            QtGui.QMessageBox.information(
                self, "Invalid Date Range",
                "The First Date must occur before or on the Last Date!")
        else:
            self.plot_bn.setEnabled(True)

    def process_data(self):
        """
        Process the source data to determine all relevant x- and y-coordinates.

        Clears all current plots from the canvas, updates processor kwargs with
        input field values, and starts the processor. Displays a message dialog
        to indicate that data is being processed. The processed data set will
        be emitted by the process attribute when processing has been completed.
        """
        self.clear_plots()
        self.update_processor()
        self.proc_msg = organs.MessageDialog(
            self, "Processing Data", "CRUNCHING NUMBERS NOW...")
        self.proc_msg.show()
        self.processor.start()

    def plot_processed_data(self, processed_data):
        """
        Plot processed data on the canvas.

        This method is a placeholder for overriding subclass methods.

        :param processed_data: Processed data sets containing x- and
            y-coordinates to be plotted
        :type processed_data: tuple
        """
        pass

    def clear_plots(self):
        """
        Clear plots from the canvas.

        This method is a placeholder for overriding subclass methods.
        """
        pass

    def update_processor(self):
        """
        Update the processor's kwargs with current field inputs.

        This method is a placeholder for overriding subclass methods.
        """
        pass

    def ondraw(self, event):
        """Check minimum x-axis date on zoom out to avoid Year Zero errors."""
        xlim = self.figure.gca().get_xlim()
        if xlim[0] != 0 and xlim[0] < 700000:
            QtGui.QMessageBox.warning(
                self, "Zoom Warning", "You are zooming out too far too " +
                "fast! The plot cannot handle dates occurring before " +
                "Year Zero. The window is closing...")
            self.close()
        if self.figure.gca().get_ylim()[0] < 0:
            self.figure.gca().axhline(y=0, linewidth=0.5, color="#FFA916")


class PlotHealthDiary(EasyPlot):
    """
    Class to plot health metric measurements.

    PlotHealthDiary presents a dialog to the user with input fields for
    plotting a set of health metric measurements. These fields are:

        First Date: The earliest Health Diary entry date for which to find
            health metric measurements
        Last Date: The latest Health Diary entry date for which to find health
            metric measurements
        Health Metric: The health metric for which to plot measurements

    PlotHealthDiary inherits all attributes and methods from its superclass.
    The parent GUI and the user's User object are passed to the constructor.
    The user's Health Diary and the process_health_metrics function are
    passed to the superclass constructor as the source data and processor
    function, respectively. It implements a sub attribute to store the subplot
    added to the figure attribute.

    The inherited methods clear_plots, plot_processed_data, and
    update_processor are overridden to handle this object's subplot, and a
    selected_metric method is implemented to return the name of the health
    metric selected in the Health Metric Field.
    """

    def __init__(self, parent, user):
        """
        Initialize a PlotHealthDiary object.

        Assigns a subplot to the sub attribute. Builds the dialog components
        and connects input field signals to slot methods.

        :param parent: Parent QMainWindow
        :type parent: QMainWindow
        :param user: The current user's User object
        :type user: User
        """
        EasyPlot.__init__(
            self, parent, user.health_diary(), process_health_metrics)
        self.setWindowTitle("Plot Health Metric Measurements")
        # Add and hide new subplot. Adjust figure layout.
        self.sub = self.figure.add_subplot(111)
        self.figure.tight_layout()
        self.clear_plots()
        # Health Metric section.
        metric_tag = organs.EasyLabel(
            self, [0, 0, 110, 26], fixed_size=True, text="Health Metric:",
            font=FONT_TAG)
        health_metrics = organs.unique_keys(user.health_diary(), 1)
        self.metric_field = organs.EasyComboBox(
            self, [0, 0, 260, 22], fixed_size=True, items=health_metrics)
        self.toolbar.addWidget(metric_tag)
        self.toolbar.addWidget(self.metric_field)
        space = organs.EasyLabel(self, [0, 0, 10, 26], fixed_size=True)
        self.toolbar.addWidget(space)
        # Add plot button to toolbar.
        self.toolbar.addWidget(self.plot_bn)
        space = organs.EasyLabel(self, [0, 0, 10, 26], fixed_size=True)
        self.toolbar.addWidget(space)
        # Connect signals to slots.
        self.metric_field.currentIndexChanged.connect(self.update_processor)

    def clear_plots(self):
        """
        Clear the plot from the canvas.

        Overrides EasyPlot.clear_plots to clear the sub attribute's plot.
        """
        self.sub.clear()
        self.sub.axes.get_xaxis().set_visible(False)
        self.sub.axes.get_yaxis().set_visible(False)

    def plot_processed_data(self, processed_data):
        """
        Plot processed data on the canvas.

        Overrides EasyPlot.plot_processed_data to plot processed health metric
        measurements. The processed_data arg is a tuple of x- and y-coordinate
        lists returned by the process_health_metrics function. These lists are
        in the format:

        --X: Entry Dates--
            [first entry date, second entry date, ...]
        --Y: Health Metric Measurements--
            [first date measurement, second date measurement, ...]

        Health metric measurements are displayed in a line plot. X-axis values
        are entry dates and y-axis values are measurements.

        :param processed_data: Processed data in the format: (entry dates list,
            health metric measurements list)
        :type processed_data: tuple
        """
        # Check for no data points to plot.
        if not processed_data[0]:
            self.proc_msg.finish()
            self.clear_plots()
            self.canvas.draw()
            QtGui.QMessageBox.information(
                self, "No Data Points", "There are no data points to plot!")
            return
        # Convert dates to mdate numbers.
        dates = mdates.date2num(processed_data[0])
        values = processed_data[1]
        # Add a horiz line at y=0 (behind line plot) if neg vals are shown.
        adjuster = (max(values) - min(values)) * 0.1
        adjuster = adjuster if adjuster > 0 else 10
        if min(values) - adjuster < 0:
            self.sub.axhline(y=0, linewidth=1, color="#FFA916")
        # Plot data and set the title.
        self.sub.plot(
            dates, values, color=COLOR_LINES, linestyle="-", linewidth=1,
            marker=".", markersize=7)
        title = str(self.selected_metric()).upper() + " BY DATE"
        self.sub.set_title(title, fontsize=16, fontweight="bold")
        # Clean up x and y axes and show them.
        self.sub.set_xlabel("Date", fontsize=13, fontweight="bold")
        self.sub.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))
        self.sub.set_xlim(min(dates) - 1, max(dates) + 1)
        self.sub.set_ylabel(
            str(self.selected_metric()), fontsize=13, fontweight="bold")
        self.sub.set_ylim(min(values) - adjuster, max(values) + adjuster)
        self.sub.axes.get_xaxis().set_visible(True)
        self.sub.axes.get_yaxis().set_visible(True)
        # Clean up figure and canvas and close processing message.
        self.figure.autofmt_xdate()
        self.figure.tight_layout()
        self.canvas.draw()
        self.proc_msg.finish()

    def update_processor(self):
        """
        Update the processor kwargs with current field inputs.

        Overrides EasyPlot.update_processor to update the processor attribute
        with custom kwargs for its processing function process_health_metrics.
        The processor is updated with source data, First Date Field input, Last
        Date Field input, and the Health Metric Field input string.
        """
        self.processor.set_kwargs(
            health_diary=self.sourcedata,
            first_date=self.first_field.date(),
            last_date=self.last_field.date(),
            metric=self.selected_metric())

    def selected_metric(self):
        """
        Return the selected health metric.

        :return: The health metric selected in the Health Metric Field
        :rtype: str
        """
        return str(self.metric_field.currentText())


class PlotNutrientGuide(EasyPlot):
    """
    Class to plot nutrient targets.

    PlotNutrientGuide presents a dialog to the user with input fields for
    plotting a set of target nutrient values. These fields are:

        First Date: The earliest Nutrient Guide effective date for which to
            find nutrient targets
        Last Date: The latest Nutrient Guide effective date for which to find
            nutrient targets
        Nutrient: The nutrient for which to plot targets

    PlotNutrientGuide inherits all attributes and methods from its superclass.
    The parent GUI and the user's User object are passed to the constructor.
    The user's Nutrient Guide and the process_nutrient_targets function are
    passed to the superclass constructor as source data and processor function,
    respectively. It implements a sub attribute to store the subplot added to
    the figure attribute.

    The inherited methods clear_plots, plot_processed_data, and
    update_processor are overridden to handle this object's subplot, and a
    selected_nid method is implemented to return the nutrient ID of the
    nutrient selected in the Nutrient Field.
    """

    def __init__(self, parent, user):
        """
        Initialize a PlotNutrientGuide object.

        Assigns a subplot to the sub attribute. Builds the dialog components
        and connects input field signals to slot methods.

        :param parent: Parent QMainWindow
        :type parent: QMainWindow
        :param user: The current user's User object
        :type user: User
        """
        EasyPlot.__init__(
            self, parent, user.nutrient_guide(), process_nutrient_targets)
        self.setWindowTitle("Plot Nutrient Targets")
        # Add and hide new subplot. Adjust figure layout.
        self.sub = self.figure.add_subplot(111)
        self.figure.tight_layout()
        self.clear_plots()
        # Nutrient section.
        nutrient_tag = organs.EasyLabel(
            self, [0, 0, 72, 26], fixed_size=True, text="Nutrient:",
            font=FONT_TAG)
        nutrient_ids = organs.unique_keys(user.nutrient_guide(), 1)
        nutrient_names = []
        for nid in dna.GUI_NUTRIENTS:
            if nid in nutrient_ids:
                nutrient_names.append(dna.NUTRIENTS[nid][0])
        self.nutrient_field = organs.EasyComboBox(
            self, [0, 0, 210, 22], fixed_size=True, items=nutrient_names)
        self.toolbar.addWidget(nutrient_tag)
        self.toolbar.addWidget(self.nutrient_field)
        space = organs.EasyLabel(self, [0, 0, 10, 26], fixed_size=True)
        self.toolbar.addWidget(space)
        # Add plot button to toolbar.
        self.toolbar.addWidget(self.plot_bn)
        space = organs.EasyLabel(self, [0, 0, 10, 26], fixed_size=True)
        self.toolbar.addWidget(space)
        # Connect signals to slots.
        self.nutrient_field.currentIndexChanged.connect(self.update_processor)

    def clear_plots(self):
        """
        Clear the plot from the canvas.

        Overrides EasyPlot.clear_plots to clear the sub attribute's plot.
        """
        self.sub.clear()
        self.sub.axes.get_xaxis().set_visible(False)
        self.sub.axes.get_yaxis().set_visible(False)

    def plot_processed_data(self, processed_data):
        """
        Plot processed data on the canvas.

        Overrides EasyPlot.plot_processed_data to plot processed nutrient
        target values. The processed_data arg is a tuple of x- and y-coordinate
        lists returned by the process_nutrient_targets function. These lists
        are in the format:

        --X: Effective Dates--
            [first effective date, second effective date, ...]
        --Y: Target Nutrient Values--
            [first date target, second date target, ...]

        Nutrient targets are displayed in a line plot. X-axis values are
        effective dates and y-axis values are targets.

        :param processed_data: Processed data in the format: (effective dates
            list, target nutrient values list)
        :type processed_data: tuple
        """
        # Check for no data points to plot.
        if not processed_data[0]:
            self.proc_msg.finish()
            self.clear_plots()
            self.canvas.draw()
            QtGui.QMessageBox.information(
                self, "No Data Points", "There are no data points to plot!")
            return
        # Convert dates to mdate numbers.
        dates = mdates.date2num(processed_data[0])
        values = processed_data[1]
        # Plot data and set the title.
        self.sub.plot(
            dates, values, color=COLOR_TARGET, linestyle="-", linewidth=1,
            marker=".", markersize=7)
        nutrient_name = dna.NUTRIENTS[self.selected_nid()][0]
        title = nutrient_name.upper() + " TARGETS BY EFFECTIVE DATE"
        self.sub.set_title(title, fontsize=16, fontweight="bold")
        # Clean up x and y axes and show them.
        self.sub.set_xlabel("Date", fontsize=13, fontweight="bold")
        self.sub.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))
        self.sub.set_xlim(min(dates) - 1, max(dates) + 1)
        nutrient_unit = dna.NUTRIENTS[self.selected_nid()][2]
        y_label = nutrient_name + " (" + nutrient_unit + ")"
        self.sub.set_ylabel(y_label, fontsize=13, fontweight="bold")
        self.sub.set_ylim(0, max(values) * 1.1)
        self.sub.axes.get_xaxis().set_visible(True)
        self.sub.axes.get_yaxis().set_visible(True)
        # Clean up figure and canvas and close processing message.
        self.figure.autofmt_xdate()
        self.figure.tight_layout()
        self.canvas.draw()
        self.proc_msg.finish()

    def update_processor(self):
        """
        Update the processor kwargs with current field inputs.

        Overrides EasyPlot.update_processor to update the processor attribute
        with custom kwargs for its processing function
        process_nutrient_targets. The processor is updated with source data,
        First Date Field input, Last Date Field input, and the nutrient ID
        of the Nutrient Field input.
        """
        self.processor.set_kwargs(
            nutrient_guide=self.sourcedata,
            first_date=self.first_field.date(),
            last_date=self.last_field.date(),
            nutrient_id=self.selected_nid())

    def selected_nid(self):
        """
        Return the nutrient ID of the selected nutrient.

        :return: The nutrient ID of the nutrient selected in the Nutrient Field
        :rtype: str
        """
        nutrient_name = str(self.nutrient_field.currentText())
        for nid in dna.NUTRIENTS:
            if dna.NUTRIENTS[nid][0] == nutrient_name:
                return nid


class PlotMacroProportions(EasyPlot):
    """
    Class to plot macronutrient proportions.

    PlotMacroProportions presents a dialog to the user with input fields for
    plotting a set of macronutrient proportions. These fields are:

        First Date: The earliest Diet record date for which to find
            macronutrient proportions
        Last Date: The latest Diet record date for which to find macronutrient
            proportions

    PlotMacroProportions inherits all attributes and methods from its
    superclass. The parent GUI and the user's User object are passed to the
    constructor. The user's Diet record objects and the
    process_macro_proportions function are passed to the superclass constructor
    as the source data and processor function, respectively. It implements a
    sub attribute to store the subplot added to the figure attribute. The
    inherited methods clear_plots, plot_processed_data, and update_processor
    are overridden to handle this object's subplot, and ondraw is extended to
    reset y-axis limits on zoom out.
    """

    def __init__(self, parent, user):
        """
        Initialize a PlotMacroProportions object.

        Assigns a subplot to the sub attribute. Builds the dialog components.

        :param parent: Parent QMainWindow
        :type parent: QMainWindow
        :param user: The current user's User object
        :type user: User
        """
        EasyPlot.__init__(
            self, parent, user.record_objects("D"), process_macro_proportions)
        self.setWindowTitle("Plot Macronutrient Proportions")
        # Add and hide new subplot. Adjust figure layout.
        self.sub = self.figure.add_subplot(111)
        self.figure.tight_layout()
        self.clear_plots()
        # Check for at least two constituent Quantities.
        num_qty = 0
        for diet in self.sourcedata.values():
            if diet.has_quantity():
                num_qty += 1
                if num_qty == 2:
                    break
        if num_qty != 2:
            self.toolbar.clear_actions()
            QtGui.QMessageBox.information(
                self, "Not Enough Quantity Data", "You must have at least " +
                "two Diet records with Ingredient Quantities added to " +
                "them in order to use this plot!")
            return
        # Add plot button to toolbar.
        self.toolbar.addWidget(self.plot_bn)
        space = organs.EasyLabel(self, [0, 0, 10, 26], fixed_size=True)
        self.toolbar.addWidget(space)

    def clear_plots(self):
        """
        Clear the plot from the canvas.

        Overrides EasyPlot.clear_plots to clear the sub attribute's plot.
        """
        self.sub.clear()
        self.sub.axes.get_xaxis().set_visible(False)
        self.sub.axes.get_yaxis().set_visible(False)

    def plot_processed_data(self, processed_data):
        """
        Plot processed data on the canvas.

        Overrides EasyPlot.plot_processed_data to plot processed macronutrient
        proportions. The processed_data_arg is a tuple of x- and y-coordinate
        lists returned by the process_macro_proportions function. These lists
        are in the format:

        --X: Diet Dates--
            [first Diet date, second Diet date, ...]
        --Y1: Protein Percentages--
            [first date percentage, second date percentage, ...]
        --Y2: Fat Percentages--
            [first date percentage, second date percentage, ...]
        --Y3: Carbohydrate Percentages--
            [first date percentage, second date percentage, ...]

        Macronutrient proportions are displayed in a stack plot. X-axis values
        are Diet record dates and y-axis values are each Diet's protein, fat,
        and carbohydrate percentages of its total caloric value.

        :param processed_data: Processed data in the format: (Diet dates list,
            protein percentages list, fat percentages list, carbohydrate
            percentages list)
        :type processed_data: tuple
        """
        # Check for no data points to plot.
        if not processed_data[0] or len(processed_data[0]) == 1:
            self.proc_msg.finish()
            self.clear_plots()
            self.canvas.draw()
            if not processed_data[0]:
                title = "No Data Points"
                message = "There are no data points to plot!"
            else:
                title = "Only One Data Point"
                message = "There must be at least two data points to plot!"
            QtGui.QMessageBox.information(self, title, message)
            return
        # Convert dates to mdate numbers.
        dates = mdates.date2num(processed_data[0])
        p_vals = processed_data[1]
        f_vals = processed_data[2]
        c_vals = processed_data[3]
        # Plot data, set title, and show legend.
        self.sub.stackplot(
            dates, p_vals, f_vals, c_vals, colors=COLOR_MACROPROP,
            labels=["Protein", "Fat", "Carbs"])
        self.sub.set_title(
            "MACRONUTRIENT DISTRIBUTION BY DATE", fontsize=16,
            fontweight="bold")
        self.sub.legend(loc="upper left")
        # Clean up x and y axes and show them.
        self.sub.set_xlabel("Date", fontsize=13, fontweight="bold")
        self.sub.set_xlim(min(dates) - 1, max(dates) + 1)
        self.sub.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))
        self.sub.set_ylabel("Percent", fontsize=13, fontweight="bold")
        self.sub.set_ylim(0, 100)
        self.sub.set_yticks(range(0, 101, 10), minor=False)
        self.sub.yaxis.grid(True, which="major")
        self.sub.axes.get_xaxis().set_visible(True)
        self.sub.axes.get_yaxis().set_visible(True)
        # Clean up figure and canvas and close processing message.
        self.figure.autofmt_xdate()
        self.figure.tight_layout()
        self.canvas.draw()
        self.proc_msg.finish()

    def update_processor(self):
        """
        Update the processor kwargs with current field inputs.

        Overrides EasyPlot.update_processor to update the processor attribute
        with custom kwargs for its processing function
        process_macro_proportions. The processor is updated with source data,
        First Date Field input, and Last Date Field input.
        """
        self.processor.set_kwargs(
            diet_objects=self.sourcedata,
            first_date=self.first_field.date(),
            last_date=self.last_field.date())

    def ondraw(self, event):
        """Extends EasyPlot.ondraw to check y-axis limits."""
        EasyPlot.ondraw(self, event)
        ylim = self.sub.get_ylim()
        if ylim[0] < 0 or ylim[1] > 100:
            self.sub.set_ylim(0, 100)


class PlotMealTimes(EasyPlot):
    """
    Class to plot Meal times.

    PlotMealTimes presents a dialog to the user with input fields for plotting
    a set of Meal times. These fields are:

        First Date: The earliest Diet record date for which to find Meal times
        Last Date: The latest Diet record date for which to find Meal times

    PlotMealTimes inherits all attributes and methods from its superclass. The
    parent GUI and the user's User object are passed to the constructor. The
    user's Diet record objects and the process_meal_times function are passed
    to the superclass constructor as the source data and processor function,
    respectively. It implements a sub attribute to store the subplot added to
    the figure attribute. The inherited methods clear_plots,
    plot_processed_data, and update_processor are overridden to handle this
    object's subplot, and ondraw is extended to reset y-axis limits on zoom
    out.
    """

    def __init__(self, parent, user):
        """
        Initialize a PlotMacroProportions object.

        Assigns a subplot to the sub attribute. Builds the dialog components.

        :param parent: Parent QMainWindow
        :type parent: QMainWindow
        :param user: The current user's User object
        :type user: User
        """
        EasyPlot.__init__(
            self, parent, user.record_objects("D"), process_meal_times)
        self.setWindowTitle("Plot Meal Times")
        # Add and hide new subplot. Adjust figure layout.
        self.sub = self.figure.add_subplot(111)
        self.figure.tight_layout()
        self.clear_plots()
        # Check for at least one child Meal.
        meal_found = False
        for diet in self.sourcedata.values():
            if len(diet.container()) > 0:
                meal_found = True
                break
        if not meal_found:
            self.toolbar.clear_actions()
            QtGui.QMessageBox.information(
                self, "No Meal Time Data", "None of your Diet records has " +
                "a Meal added to it! You must have at least one Meal to use " +
                "this plot.")
            return
        # Add plot button to toolbar.
        self.toolbar.addWidget(self.plot_bn)
        space = organs.EasyLabel(self, [0, 0, 10, 26], fixed_size=True)
        self.toolbar.addWidget(space)

    def clear_plots(self):
        """
        Clear the plot from the canvas.

        Overrides EasyPlot.clear_plots to clear the sub attribute's plot.
        """
        self.sub.clear()
        self.sub.axes.get_xaxis().set_visible(False)
        self.sub.axes.get_yaxis().set_visible(False)

    def plot_processed_data(self, processed_data):
        """
        Plot processed data on the canvas.

        Overrides EasyPlot.plot_processed_data to plot processed Meal times.
        The processed_data arg is a tuple of x- and y-coordinate lists returned
        by the process_meal_times function. These lists are in the format:

        --X: Diet Dates--
            [first Diet date, second Diet date, ...]
        --Y: Meal Times--
            [[first date first time, first date second time, ...],
             [second date first time, second date second time, ...], ...]

        Meal times are displayed in a series of separated line plots, one per
        Diet date. X-axis values are Diet record dates and y-axis values are
        each Diet's Meal times converted to floats in the half-open interval
        [0, 24).

        :param processed_data: Processed data in the format: (Diet dates list,
            Meal times list of lists)
        :type processed_data: tuple
        """
        # Check for no data points to plot.
        if not processed_data[0]:
            self.proc_msg.finish()
            self.clear_plots()
            self.canvas.draw()
            QtGui.QMessageBox.information(
                self, "No Data Points", "There are no data points to plot!")
            return
        # Convert dates to mdate numbers.
        dates = mdates.date2num(processed_data[0])
        values = processed_data[1]
        # Plot data and set title. Keep same line color for every 7 days. Cycle
        # after 63 days. 9 colors are in same order as visible spectrum.
        colors = ["#F42A12", "#F39B13", "#D3D600", "#37DC0F", "#009E15",
                  "#1FD1D9", "#1F79D9", "#651FD9", "#C51FD9"]
        day = week = 0
        for x_coord, y_coords in zip(dates, values):
            color_idx = week % 9
            self.sub.plot(
                [x_coord] * len(y_coords), y_coords, color=colors[color_idx],
                linestyle="-", linewidth=1, marker=".", markersize=6)
            day += 1
            if day % 7 == 0:
                week += 1
        self.sub.set_title(
            "MEAL TIMES BY DATE", fontsize=16, fontweight="bold")
        # Clean up x and y axes and show them.
        self.sub.set_xlabel("Date", fontsize=13, fontweight="bold")
        self.sub.set_xlim(min(dates) - 1, max(dates) + 1)
        self.sub.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))
        self.sub.set_ylabel("Time (hour)", fontsize=13, fontweight="bold")
        self.sub.set_ylim(0, 24)
        self.sub.set_yticks(range(0, 25, 1), minor=False)
        y_ticks_labs = ["12 AM"] + [str(num) + " AM" for num in range(1, 12)]
        y_ticks_labs += ["12 PM"] + [str(num) + " PM" for num in range(1, 12)]
        y_ticks_labs += ["12 AM"]
        self.sub.set_yticklabels(y_ticks_labs)
        self.sub.yaxis.grid(True, which="major")
        self.sub.axes.get_xaxis().set_visible(True)
        self.sub.axes.get_yaxis().set_visible(True)
        # Clean up figure and canvas and close processing message.
        self.figure.autofmt_xdate()
        self.figure.tight_layout()
        self.canvas.draw()
        self.proc_msg.finish()

    def update_processor(self):
        """
        Update the processor kwargs with current field inputs.

        Overrides EasyPlot.update_processor to update the process attribute
        with custom kwargs for its processing function process_meal_times. The
        processor is updated with the source data, First Date Field input, and
        Last Date Field input.
        """
        self.processor.set_kwargs(
            diet_objects=self.sourcedata,
            first_date=self.first_field.date(),
            last_date=self.last_field.date())

    def ondraw(self, event):
        """Extends EasyPlot.ondraw to check y-axis limits."""
        EasyPlot.ondraw(self, event)
        ylim = self.sub.get_ylim()
        if ylim[0] < 0 or ylim[1] > 24:
            self.sub.set_ylim(0, 24)


class PlotNutrientValues(EasyPlot):
    """
    Class to plot nutrient values.

    PlotNutrientValues presents a dialog to the user with input fields for
    plotting a set of nutrient values. These fields are:

        First Date: The earliest Diet record date for which to find nutrient
            values
        Last Date: The latest Diet record date for which to find nutrient
            values
        Nutrient: The nutrient for which to plot values

    PlotNutrientValues inherits all attributes and methods from its superclass.
    The parent GUI and the user's User object are passed to the constructor.
    The user's Diet record objects and the process_nutrient_values function are
    passed to the superclass constructor as the source data and processor
    function, respectively. It implements a sub attribute to store the subplot
    added to the figure attribute and a targets attribute to store the most
    recent nutrient targets from the Nutrient Guide--or an empty dict if no
    latest targets exist.

    The inherited methods clear_plots, plot_processed_data, and
    update_processor are overridden to handle this object's subplot, and a
    selected_nid method is implemented to return the nutrient ID of the
    nutrient selected in the Nutrient Field.
    """

    def __init__(self, parent, user):
        """
        Initialize a PlotNutrientValues object.

        Assigns a subplot to the sub attribute. Builds the dialog components
        and connects input fields to slot methods.

        :param parent: Parent QMainWindow
        :type parent: QMainWindow
        :param user: The current user's User object
        :type user: User
        """
        EasyPlot.__init__(
            self, parent, user.record_objects("D"), process_nutrient_values)
        self.setWindowTitle("Plot Nutrient Values")
        # Add and hide new subplot. Adjust figure layout.
        self.sub = self.figure.add_subplot(111)
        self.figure.tight_layout()
        self.clear_plots()
        # Store latest targets from the user's Nutrient Guide, or {}.
        latest = organs.max_key(user.nutrient_guide())
        self.targets = {} if latest is None else user.nutrient_guide()[latest]
        # Nutrient section.
        nutrient_tag = organs.EasyLabel(
            self, [0, 0, 72, 26], fixed_size=True, text="Nutrient:",
            font=FONT_TAG)
        nut_names = [
            dna.NUTRIENTS[nid][0] for nid in dna.GUI_NUTRIENTS]
        self.nutrient_field = organs.EasyComboBox(
            self, [0, 0, 210, 22], fixed_size=True, items=nut_names)
        self.toolbar.addWidget(nutrient_tag)
        self.toolbar.addWidget(self.nutrient_field)
        space = organs.EasyLabel(self, [0, 0, 10, 26], fixed_size=True)
        self.toolbar.addWidget(space)
        # Add plot button to toolbar.
        self.toolbar.addWidget(self.plot_bn)
        space = organs.EasyLabel(self, [0, 0, 10, 26], fixed_size=True)
        self.toolbar.addWidget(space)
        # Connect signals to slots.
        self.nutrient_field.currentIndexChanged.connect(self.update_processor)

    def clear_plots(self):
        """
        Clear the plot from the canvas.

        Overrides EasyPlot.clear_plots to clear the sub attribute's plot.
        """
        self.sub.clear()
        self.sub.axes.get_xaxis().set_visible(False)
        self.sub.axes.get_yaxis().set_visible(False)

    def plot_processed_data(self, processed_data):
        """
        Plot processed data on the canvas.

        Overrides EasyPlot.plot_processed_data to plot processed nutrient
        values. The processed_data arg is a tuple of x- and y-coordinate lists
        returned by the process_nutrient_values function. These lists are in
        the format:

        --X: Diet Dates--
            [first Diet date, second Diet date, ...]
        --Y: Nutrient Values--
            [first date value, second date value, ...]

        Nutrient values are displayed in a line plot. X-axis values are Diet
        record dates and y-axis values are each Diet's nutrient value. If
        targets are found for the selected nutrient, the most recent target is
        displayed as a horizontal line intersecting the y-axis at the target
        value.

        :param processed_data: Processed data in the format: (Diet dates list,
            nutrient values list)
        :type processed_data: tuple
        """
        # Check for no data points to plot.
        if not processed_data[0]:
            self.proc_msg.finish()
            self.clear_plots()
            self.canvas.draw()
            QtGui.QMessageBox.information(
                self, "No Data Points", "There are no data points to plot!")
            return
        # Convert dates to mdate numbers.
        dates = mdates.date2num(processed_data[0])
        values = processed_data[1]
        # Determine target if it exists in the latest targets (default 0).
        nid = self.selected_nid()
        target = 0 if nid not in self.targets else self.targets[nid]
        # Add horiz line (behind plot) at y=target if target != 0.
        if target != 0:
            self.sub.axhline(
                y=target, linewidth=1, color=COLOR_TARGET, label="Target")
            self.sub.legend(loc="upper left")
        # Plot data and set title.
        self.sub.plot(
            dates, values, color=COLOR_LINES, linestyle="-", linewidth=1,
            marker=".", markersize=7)
        nutrient_name = dna.NUTRIENTS[nid][0]
        title = nutrient_name.upper() + " VALUES BY DATE"
        self.sub.set_title(title, fontsize=16, fontweight="bold")
        # Clean up x and y axes and show them.
        self.sub.set_xlabel("Date", fontsize=13, fontweight="bold")
        self.sub.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))
        self.sub.set_xlim(min(dates) - 1, max(dates) + 1)
        nutrient_unit = dna.NUTRIENTS[self.selected_nid()][2]
        y_label = nutrient_name + " (" + nutrient_unit + ")"
        self.sub.set_ylabel(y_label, fontsize=13, fontweight="bold")
        y_max = max(target, max(values)) * 1.1
        y_max = y_max if y_max > 0 else 10
        self.sub.set_ylim(0, y_max)
        self.sub.axes.get_xaxis().set_visible(True)
        self.sub.axes.get_yaxis().set_visible(True)
        # Clean up figure and canvas and close processing message.
        self.figure.autofmt_xdate()
        self.figure.tight_layout()
        self.canvas.draw()
        self.proc_msg.finish()

    def update_processor(self):
        """
        Update the processor kwargs with current field inputs.

        Overrides EasyPlot.update_processor to update the processor attribute
        with custom kwargs for its processing function process_nutrient_values.
        The processor is updated with source data, First Date Field input, Last
        Date Field input, and the nutrient ID of the Nutrient Field input.
        """
        self.processor.set_kwargs(
            diet_objects=self.sourcedata,
            first_date=self.first_field.date(),
            last_date=self.last_field.date(),
            nutrient_id=self.selected_nid())

    def selected_nid(self):
        """
        Return the nutrient ID of the selected nutrient.

        :return: The nutrient ID of the nutrient selected in the Nutrient Field
        :rtype: str
        """
        nutrient_name = str(self.nutrient_field.currentText())
        for nid in dna.NUTRIENTS:
            if dna.NUTRIENTS[nid][0] == nutrient_name:
                return nid


class PlotPerformance(EasyPlot):
    """
    Class to plot performance results for an Exercise property.

    PlotPerformance presents a dialog to the user with input fields for
    plotting a set of performance result values for an Exercise property. Some
    fields are specific to certain Exercise properties. These fields are:

    --All Properties--
        First Date: The earliest Workout period began date for which to find
            performance results
        Last Date: The latest Workout period began date for which to find
            performance results
        Results Type: The type of performance results to plot
    --Exercise Property 'itemid'--
        Exercise: The Exercise for which results are plotted
    --Exercise Property 'focusmuscle'--
        Focus Muscle: The focus muscle for which results are plotted
    --Exercise Property 'tags'--
        Tag: The tag for which results are plotted

    PlotPerformance inherits all attributes and methods from its superclass.
    The parent GUI and the user's User object are passed to the constructor.
    The user's Program record objects and the process_performance_results
    function are passed to the superclass constructor as the source data and
    processor function, respectively. It implements a sub attribute to store
    the subplot added to the figure attribute, an exprop attribute to store the
    Exercise property that the dialog handles, and an edref attribute to store
    the user's Exercise Details reference dict. The minimum First Date and
    maximum Last Date are changed to reflect the minimum/maximum period began
    dates for the constituent Workouts of all Programs.

    The inherited methods clear_plots, plot_processed_data, and
    update_processor are overridden to handle this object's subplot, and
    a selected_type method is implemented to return the selected option in the
    Results Type Field as an appropriate arg for the processor function.
    Additional methods are implemented to handle the fields created for each
    Exercise property.
    """

    def __init__(self, parent, user, exercise_property):
        """
        Initialize a PlotPerformance object.

        Assigns a subplot to the sub attribute, the exercise_property arg to
        the exprop attribute, and the user's Exercise Details reference dict
        to the edref attribute. Builds the dialog components and connects input
        fields to slot methods.

        :param parent: Parent QMainWindow
        :type parent: QMainWindow
        :param user: The current user's User object
        :type user: User
        :param exercise_property: The Exercise property this dialog handles:
            'itemid', 'focusmuscle', or 'tags'
        :type exercise_property: str
        """
        EasyPlot.__init__(
            self, parent, user.record_objects("P"),
            process_performance_results)
        props = {"itemid": "Exercise", "focusmuscle": "Muscle", "tags": "Tag"}
        window_title = "Plot " + props[exercise_property] + " Performance"
        self.setWindowTitle(window_title)
        # Add and hide new subplot. Adjust figure layout.
        self.sub = self.figure.add_subplot(111)
        self.figure.tight_layout()
        self.clear_plots()
        # Store Exercise property and EDREF (to look up Exercise descriptions).
        self.exprop = exercise_property
        self.edref = user.exercise_details()
        # Find min/max Workout began dates across all Programs.
        all_periods = {}
        for program in user.record_objects("P").values():
            all_periods.update(program.workout_periods())
        min_date = organs.min_key(all_periods)
        max_date = organs.max_key(all_periods)
        # Check for at least one constituent Workout across all Programs.
        # Without it, First and Last Date Fields can't be updated.
        if None in [min_date, max_date]:
            self.toolbar.clear_actions()
            QtGui.QMessageBox.information(
                self, "No Workout Data", "None of your Program records has " +
                "a Workout added to it! You must have at least one Workout " +
                "to use this plot.")
            return
        first_args = [int(num) for num in min_date[:10].split("-")]
        last_args = [int(num) for num in max_date[:10].split("-")]
        # Update First/Last Date Fields with new min/max.
        self.first_field.setMinimumDate(QtCore.QDate(*first_args))
        self.first_field.setMaximumDate(QtCore.QDate(*last_args))
        self.first_field.setDate(QtCore.QDate(*first_args))
        self.last_field.setMinimumDate(QtCore.QDate(*first_args))
        self.last_field.setMaximumDate(QtCore.QDate(*last_args))
        self.last_field.setDate(QtCore.QDate(*last_args))
        # Check for at least one constituent Activity across all Programs.
        # Without it, property field options can't be updated.
        has_activity = False
        for program in self.sourcedata.values():
            if program.has_activity():
                has_activity = True
                break
        if not has_activity:
            self.toolbar.clear_actions()
            QtGui.QMessageBox.information(
                self, "No Activity Data", "None of your Programs records " +
                "has a Workout Activity added to it! You must have at least " +
                "one Activity to use this plot.")
            return
        # Results Type section.
        results_tag = organs.EasyLabel(
            self, [0, 0, 72, 26], fixed_size=True, text="Results:",
            font=FONT_TAG)
        self.results_field = organs.EasyComboBox(
            self, [0, 0, 120, 22], fixed_size=True,
            items=["Total Effort", "Max Intensity", "Total Magnitude"])
        self.toolbar.addWidget(results_tag)
        self.toolbar.addWidget(self.results_field)
        space = organs.EasyLabel(self, [0, 0, 10, 26], fixed_size=True)
        self.toolbar.addWidget(space)
        # Item ID property--find all unique Exercises for all Programs, sort
        # by description, prepend with item ID to differentiate.
        if exercise_property == "itemid":
            exercise_tag = organs.EasyLabel(
                self, [0, 0, 74, 26], fixed_size=True, text="Exercise:",
                font=FONT_TAG)
            unique_ids = set()
            for program in self.sourcedata.values():
                unique_ids.update(program.unique_exercises())
            items = [(itemid, self.edref[itemid][0]) for itemid in unique_ids]
            items.sort(key=lambda x: x[1].lower())
            exercises = [info[0] + ": " + info[1] for info in items]
            self.exercise_field = organs.EasyComboBox(
                self, [0, 0, 320, 22], fixed_size=True, items=exercises)
            self.toolbar.addWidget(exercise_tag)
            self.toolbar.addWidget(self.exercise_field)
            space = organs.EasyLabel(self, [0, 0, 10, 26], fixed_size=True)
            self.toolbar.addWidget(space)
            self.exercise_field.currentIndexChanged.connect(
                self.update_processor)
        # Focus muscle property--find all unique focus muscles for all Programs
        # and sort by name.
        if exercise_property == "focusmuscle":
            muscle_tag = organs.EasyLabel(
                self, [0, 0, 62, 26], fixed_size=True, text="Muscle:",
                font=FONT_TAG)
            unique_muscles = set()
            for program in self.sourcedata.values():
                unique_muscles.update(program.unique_focusmuscles())
            muscles = sorted(list(unique_muscles))
            self.muscle_field = organs.EasyComboBox(
                self, [0, 0, 100, 22], fixed_size=True, items=muscles)
            self.toolbar.addWidget(muscle_tag)
            self.toolbar.addWidget(self.muscle_field)
            space = organs.EasyLabel(self, [0, 0, 10, 26], fixed_size=True)
            self.toolbar.addWidget(space)
            self.muscle_field.currentIndexChanged.connect(
                self.update_processor)
        # Tags property--find all unique tags for all Programs, sort by name.
        if exercise_property == "tags":
            unique_tags = set()
            for program in self.sourcedata.values():
                unique_tags.update(program.unique_tags())
            # Check for at least one unique tag. Remove subplot in addition to
            # clearing the toolbar of actions.
            if not unique_tags:
                self.toolbar.clear_actions()
                self.figure.delaxes(self.sub)
                QtGui.QMessageBox.information(
                    self, "No Tag Data", "None of your Program records has " +
                    "an Activity added to it which references an Exercise " +
                    "item with tags! You cannot use this plot.")
                return
            tags = sorted(list(unique_tags))
            tag_tag = organs.EasyLabel(
                self, [0, 0, 40, 26], fixed_size=True, text="Tag:",
                font=FONT_TAG)
            self.tag_field = organs.EasyComboBox(
                self, [0, 0, 200, 22], fixed_size=True, items=tags)
            self.toolbar.addWidget(tag_tag)
            self.toolbar.addWidget(self.tag_field)
            space = organs.EasyLabel(self, [0, 0, 10, 26], fixed_size=True)
            self.toolbar.addWidget(space)
            self.tag_field.currentIndexChanged.connect(self.update_processor)
        # Add plot button to toolbar.
        self.toolbar.addWidget(self.plot_bn)
        space = organs.EasyLabel(self, [0, 0, 10, 26], fixed_size=True)
        self.toolbar.addWidget(space)
        # Connect Results Type Field signal to slot after all checks finished.
        self.results_field.currentIndexChanged.connect(self.update_processor)

    def clear_plots(self):
        """
        Clear the plot from the canvas.

        Overrides EasyPlot.clear_plots to clear the sub attribute's plot.
        """
        self.sub.clear()
        self.sub.axes.get_xaxis().set_visible(False)
        self.sub.axes.get_yaxis().set_visible(False)

    def plot_processed_data(self, processed_data):
        """
        Plot processed data set on the canvas.

        Overrides EasyPlot.plot_processed_data to plot processed performance
        results for the Exercise property. The processed_data arg is a tuple of
        x- and y-coordinate lists returned by the process_performance_results
        function. The type of data in the returned coord list is dependent on
        which Exercise property is handled by this object. These lists are in
        the format:

        --X: Workout Period Began Dates--
            [first Workout began date, second Workout began date, ...]
        --Y: Performance Result Values--
            [first date Value, second date Value, ...]
        --X(vertical lines): Program Start Dates--
            [first Program start, second Program start, ...]

        Performance results are displayed in a line plot. X-axis values are
        Workout period began dates and y-axis values are each Workout's
        performance result for the selected Exercise, muscle, or tag. If
        Program start dates are found within the date range, each Program's
        start is displayed as a vertical line intersecting the x-axis at its
        date.

        :param processed_data: Processed data in the format: (Workout began
            dates list, performance results for property value list, Program
            start dates list)
        :type processed_data: tuple
        """
        # Check for no data points to plot.
        if not processed_data[0]:
            self.proc_msg.finish()
            self.clear_plots()
            self.canvas.draw()
            QtGui.QMessageBox.information(
                self, "No Data Points", "There are no data points to plot!")
            return
        # Convert dates to mdate numbers.
        dates = mdates.date2num(processed_data[0])
        values = processed_data[1]
        starts = mdates.date2num(processed_data[2])
        # Determine if any start dates. Assign label to only first one.
        # first program start so that the legend has only one element.
        program_label = False
        for start in starts:
            if not program_label:
                self.sub.axvline(
                    x=start, linewidth=0.75, color=COLOR_PROGRAM,
                    label="Program Start")
                program_label = True
            else:
                self.sub.axvline(x=start, linewidth=0.75, color=COLOR_PROGRAM)
        if program_label:
            self.sub.legend(loc="upper left")
        # Plot data.
        self.sub.plot(
            dates, values, color=COLOR_LINES, linestyle="-", linewidth=1,
            marker=".", markersize=7)
        # Determine title and y-label.
        title = y_label = ""
        results_name = str(self.results_field.currentText()).upper()
        if self.exprop == "itemid":
            desc = self.edref[self.selected_itemid()][0].upper()
            desc = desc[:40] + "..." if len(desc) > 40 else desc
            title = desc + ": " + results_name + " BY DATE"
            metrics = self.edref[self.selected_itemid()][2]
            ylabs = {
                0: "Effort (" + metrics[0] + ")",
                1: "Intensity (" + metrics[1] + ")", 2: "Magnitude (no unit)"}
            y_label = ylabs[self.results_field.currentIndex()]
        if self.exprop == "focusmuscle":
            muscle = self.selected_muscle().upper()
            title = muscle + ": " + results_name + " BY DATE"
            y_label = results_name.split(" ")[1].title() + " (no unit)"
        if self.exprop == "tags":
            tag = self.selected_tag().upper()
            tag = tag[:40] + "..." if len(tag) > 40 else tag
            title = tag + ": " + results_name + " BY DATE"
            y_label = results_name.split(" ")[1].title() + " (no unit)"
        # Set title, clean up x and y axes and show them.
        self.sub.set_title(title, fontsize=16, fontweight="bold")
        self.sub.set_xlabel("Date", fontsize=13, fontweight="bold")
        self.sub.set_xlim(min(dates) - 1, max(dates) + 1)
        self.sub.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))
        self.sub.set_ylabel(y_label, fontsize=13, fontweight="bold")
        y_max = max(values) * 1.1
        y_max = y_max if y_max > 0 else 10
        self.sub.set_ylim(0, y_max)
        # Clean up figure and canvas and close processing message.
        self.sub.axes.get_xaxis().set_visible(True)
        self.sub.axes.get_yaxis().set_visible(True)
        self.figure.autofmt_xdate()
        self.figure.tight_layout()
        self.canvas.draw()
        self.proc_msg.finish()

    def update_processor(self):
        """
        Update the processor kwargs with current field inputs.

        Overrides EasyPlot.update_processor to update the processor attribute
        with custom kwargs for its processing function
        process_performance_results. The processor is updated with source data,
        First Date Field input, Last Date Field input, the results_type arg
        which corresponds with the option selected in the Results Type Field,
        the Exercise property name stored in the exprop attribute, and the
        Exercise property value. The Exercise property value can be the item
        ID of the selected Exercise in the Exercise Field, the selected muscle
        in the Focus Muscle Field, or the selected tag in the Tag Field.
        """
        if self.exprop == "itemid":
            propval = self.selected_itemid()
        elif self.exprop == "focusmuscle":
            propval = self.selected_muscle()
        else:
            propval = self.selected_tag()
        self.processor.set_kwargs(
            program_objects=self.sourcedata,
            first_date=self.first_field.date(),
            last_date=self.last_field.date(),
            results_type=self.selected_type(),
            exercise_property=self.exprop,
            property_value=propval)

    def selected_type(self):
        """
        Return the selected performance results type.

        :return: The results type selected in the Results Type Field as a
            suitable arg for the results_type parameter of the
            process_performance_results function
        :rtype: str
        """
        selected_results = str(self.results_field.currentText())
        if selected_results == "Total Effort":
            return "effort"
        elif selected_results == "Max Intensity":
            return "intensity"
        else:
            return "magnitude"

    def selected_itemid(self):
        """
        Return the item ID of the selected Exercise.

        :return: The item ID of the Exercise selected in the Exercise Field.
        :rtype: str
        """
        exercise_name = str(self.exercise_field.currentText())
        return exercise_name[:5]

    def selected_muscle(self):
        """
        Return the selected focus muscle.

        :return: The muscle selected in the Focus Muscle Field.
        :rtype: str
        """
        return str(self.muscle_field.currentText())

    def selected_tag(self):
        """
        Return the selected tag.

        :return: The tag selected in the Tag Field.
        :rtype: str
        """
        return str(self.tag_field.currentText())


class PlotWorkoutPeriods(EasyPlot):
    """
    Class to plot Workout periods.

    PlotWorkoutPeriods presents a dialog to the user with input fields for
    plotting a set of Workout periods. These fields are:

        First Date: The earliest Workout period began date for which to find
            Workout periods
        Last Date: The latest Workout period began date for which to find
            Workout periods

    PlotWorkoutPeriods inherits all attributes and methods from its superclass.
    The parent GUI and the user's User object are passed to the constructor.
    The user's Program records and the process_workout_periods are passed to
    the superclass constructor as the source data and processor function,
    respectively. It implements a sub attribute to store the subplot added to
    the figure attribute. The inherited methods clear_plots,
    plot_processed_data, and update_processor are overridden to handle this
    object's subplot, and ondraw is extended to reset y-axis limits on zoom
    out.
    """

    def __init__(self, parent, user):
        """
        Initialize a PlotWorkoutPeriods object.

        Assigns a subplot to the sub attribute. Builds the dialog components.

        :param parent: Parent QMainWindow
        :type parent: QMainWindow
        :param user: The current user's User object
        :type user: User
        """
        EasyPlot.__init__(
            self, parent, user.record_objects("P"), process_workout_periods)
        self.setWindowTitle("Plot Workout Periods")
        # Add and hide new subplot. Adjust figure layout.
        self.sub = self.figure.add_subplot(111)
        self.figure.tight_layout()
        self.clear_plots()
        # Find min/max Workout began dates across all Programs.
        all_periods = {}
        for program in user.record_objects("P").values():
            all_periods.update(program.workout_periods())
        min_date = organs.min_key(all_periods)
        max_date = organs.max_key(all_periods)
        # Check for at least one constituent Workout across all Programs.
        # Without it, First and Last Date Fields can't be updated.
        if None in [min_date, max_date]:
            self.toolbar.clear_actions()
            QtGui.QMessageBox.information(
                self, "No Workout Data", "None of your Program records has " +
                "a Workout added to it! You must have at least one Workout " +
                "to use this plot.")
            return
        first_args = [int(num) for num in min_date[:10].split("-")]
        last_args = [int(num) for num in max_date[:10].split("-")]
        # Update First/Last Date Fields with new min/max.
        self.first_field.setMinimumDate(QtCore.QDate(*first_args))
        self.first_field.setMaximumDate(QtCore.QDate(*last_args))
        self.first_field.setDate(QtCore.QDate(*first_args))
        self.last_field.setMinimumDate(QtCore.QDate(*first_args))
        self.last_field.setMaximumDate(QtCore.QDate(*last_args))
        self.last_field.setDate(QtCore.QDate(*last_args))
        # Add plot button to toolbar.
        self.toolbar.addWidget(self.plot_bn)
        space = organs.EasyLabel(self, [0, 0, 10, 26], fixed_size=True)
        self.toolbar.addWidget(space)

    def clear_plots(self):
        """
        Clear the plot from the canvas.

        Overrides EasyPlot.clear_plots to clear the sub attribute's plot.
        """
        self.sub.clear()
        self.sub.axes.get_xaxis().set_visible(False)
        self.sub.axes.get_yaxis().set_visible(False)

    def plot_processed_data(self, processed_data):
        """
        Plot processed data on the canvas.

        Overrides EasyPlot.plot_processed_data to plot processed Workout
        periods. The processed_data arg is a tuple of x- and y-coordinate lists
        returned by the process_workout_periods function. These lists are in
        the format:

        --X: Workout Period Began Dates--
            [first Workout began date, first Workout began date,
             second Workout began date, second Workout began date...]
        --Y: Workout Periods--
            [first date began time, first date ended time,
             second date began time, second date ended time, ...]
        --X(vertical lines): Program Start Dates--
            [first Program start, second Program start, ...]

        Workout periods are displayed in a series of separated line plots, one
        per period or partial period (if the period spans multiple dates).
        X-axis values are Workout period began dates and y-axis values are each
        Workout's period converted to floats in the closed interval [0, 24]. If
        Program start dates are found within the date range, each Program's
        start is displayed as a vertical line intersecting the x-axis at its
        date.

        :param processed_data: Processed data in the format: (Workout period
            began dates list, Workout period began and ended times list,
            Program start dates list)
        :type processed_data: tuple
        """
        # Check for no data points to plot.
        if not processed_data[0]:
            self.proc_msg.finish()
            self.clear_plots()
            self.canvas.draw()
            QtGui.QMessageBox.information(
                self, "No Data Points", "There are no data points to plot!")
            return
        # Convert dates to mdate numbers.
        dates = mdates.date2num(processed_data[0])
        values = processed_data[1]
        starts = mdates.date2num(processed_data[2])
        # Determine if any start dates. Assign label to only first one.
        # first program start so that the legend has only one element.
        program_label = False
        for start in starts:
            if not program_label:
                self.sub.axvline(
                    x=start, linewidth=0.75, color=COLOR_PROGRAM,
                    label="Program Start")
                program_label = True
            else:
                self.sub.axvline(x=start, linewidth=0.75, color=COLOR_PROGRAM)
        if program_label:
            self.sub.legend(loc="upper left")
        # Plot data and set title. Connect every two pairs of data points.
        for idx in range(0, len(dates), 2):
            self.sub.plot(
                dates[idx:idx + 2], values[idx: idx + 2], color=COLOR_LINES,
                linestyle="-", linewidth=2, marker="_", markersize=5)
        self.sub.set_title(
            "WORKOUT PERIODS BY DATE", fontsize=16, fontweight="bold")
        # Clean up x and y axes and show them.
        self.sub.set_xlabel("Date", fontsize=13, fontweight="bold")
        self.sub.set_xlim(min(dates) - 1, max(dates) + 1)
        self.sub.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))
        self.sub.set_ylabel("Time (hour)", fontsize=13, fontweight="bold")
        self.sub.set_ylim(0, 24)
        self.sub.set_yticks(range(0, 25, 1), minor=False)
        y_ticks_labs = ["12 AM"] + [str(num) + " AM" for num in range(1, 12)]
        y_ticks_labs += ["12 PM"] + [str(num) + " PM" for num in range(1, 12)]
        y_ticks_labs += ["12 AM"]
        self.sub.set_yticklabels(y_ticks_labs)
        self.sub.yaxis.grid(True, which="major")
        self.sub.axes.get_xaxis().set_visible(True)
        self.sub.axes.get_yaxis().set_visible(True)
        # Clean up figure and canvas and close processing message.
        self.figure.autofmt_xdate()
        self.figure.tight_layout()
        self.canvas.draw()
        self.proc_msg.finish()

    def update_processor(self):
        """
        Update the processor kwargs with current field inputs.

        Overrides EasyPlot.update_processor to update the processor attribute
        with custom kwargs for its processing function process_workout_periods.
        The processor is updated with the source data, First Date Field input,
        and Last Date Field input.
        """
        self.processor.set_kwargs(
            program_objects=self.sourcedata,
            first_date=self.first_field.date(),
            last_date=self.last_field.date())

    def ondraw(self, event):
        """Extends EasyPlot.ondraw to check y-axis limits."""
        EasyPlot.ondraw(self, event)
        ylim = self.sub.get_ylim()
        if ylim[0] < 0 or ylim[1] > 24:
            self.sub.set_ylim(0, 24)

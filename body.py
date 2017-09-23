#!/usr/bin/env python2.7
"""
This module contains classes to manage and analyze nutrition and fitness data.
----------
The user will follow nutrition and fitness routines to track and manage any
foods consumed and exercises performed. The Build Manager tool allows the user
to create a 'build', which is a representation of such a routine. Each build is
made up of one or more 'build elements', or the individual components that
represent different levels within the routine, which relate to each other using
an inherent size or duration property.

The build element classes in this module represent the components of each type
of routine. Their class names should clearly indicate their sizes relative to
other nutrition or fitness build elements, as well as hint at which additional
properties they hold. In this application, the size-based relationship
structure is called a 'build hierarchy'. Build element classes inherit a
'_container' list attribute from the base class BuildCenter, and 8 out of 10
of them can contain within that list other build element class objects that
fall somewhere within their respective build hierarchy. Build hierarchies for
each type of routine are:

--Nutrition Build Elements--
    Diet > Meal > Recipe > Ingredient > Quantity
--Fitness Build Elements--
    Program > Cycle > Workout > Activity > Session

Nutrition build elements represent edibles that the user consumes in a given
period of time. This hierarchy is based on the size of the edible or collection
of edibles. Fitness build elements represent actions that the user completes
in a given period of time for the purpose of physical fitness. The hierarchy is
based on the duration of an action or series of actions. Below is a table of
each build element, its properties, and the child build elements it can store
in its _container attribute (aka container) as a parent.

Name        Properties              Child Element(s)
------------------------------------------------------
Diet        description, date       Meal
Meal        description, time       Recipe, Ingredient
Recipe      description, portion    Recipe, Ingredient
Ingredient  itemid                  Quantity
Quantity    itemid                  -NA-
------------------------------------------------------
Program     description, start      Cycle
Cycle       description             Workout
Workout     description, period     Activity
Activity    itemid                  Session
Session     itemid                  -NA-

There are clear differences between the top three elements in each hierarchy
and the bottom two. For brevity, they will be referred to as 'T3' and 'B2'.
T3s all have 'description' properties, can store elements one level below them
as children in their containers, and can also be saved as template inventory
items--elements with pre-loaded properties that can be reused. Regarding child
elements, Meal and Recipe are unique in that they can each store one additional
element type in their containers. A Meal can also store an Ingredient, since
real world meals might consist of either a portion of a recipe or an individual
quantity of an ingredient (i.e. food). A Recipe can also store other Recipe
elements, since the components of a real world recipe could be individual
quantities of ingredients or portions of another recipe (e.g. using separately
prepared pie crust as a component of a pie recipe). The case with Recipes gives
the user an extra level of flexibility when creating realistic builds.

B2s all have one property, an 'itemid', that is assigned an existing reference
item ID. Ingredients and Quantities are assigned a Food reference item ID, and
Activities and Sessions are assigned an Exercise reference item ID. These item
IDs must be passed to the B2 element constructors--unlike T3 elements, which do
not require any properties to be passed to their constructors. B2 elements
essentially extend the functionality of reference items so that they can be
added to a build. A Food in a build is called an Ingredient, and its portion
data is expressed by a Quantity. An Exercise in a build is called an Activity,
and its performance data is expressed by a Session. Although Ingredient and
Activity elements hold the same properties as Food and Exercise reference
items, the names are kept different to clarify how each type is used and where
it can be found in the application.

Bottom level B2 elements Quantity and Session cannot store other elements in
their containers. Instead, each stores a single data set in a list. A Quantity
stores a portion size of an Ingredient/Food consisting of a numeric amount and
its associated unit of measure (e.g. [1, 'cup']). A Session stores performance
measurements of an Activity/Exercise consisting of a numeric effort amount, a
numeric intensity amount, and an optional note (e.g. [5, 125, 'superset']).
In this context, 'effort' is the amount of work that one does (e.g. 5 reps),
and 'intensity' is how hard one is pushed to do that work (e.g. 125 lb).

The base class of all build element classes is BuildCenter. It itself is a
subclass of QTreeWidgetItem, which allows it to be displayed in the Build
Viewer--a QTreeWidget. It has three class attributes that point to the user's
Exercise Details, Food Details, and Food Nutrients reference dictionaries.
When a User object is constructed, user reference data is loaded into its _data
dictionary attribute and a new BuildCenter object is assigned to its
_buildcenter attribute. The three reference dicts within _data are then passed
to _buildcenter's update_references method. This allows all build element
classes instantiated past that point to look up that user's reference items.

BuildCenter has one instance attribute, _container. The _container attribute
(aka 'the container') stores other build element objects, or data sets, as
described above. All methods to modify the container are implemented by the
base class. An additional method, widgetize, is implemented to update a build
element class object's text and children attributes that it inherits from the
QTreeWidgetItem superclass. BuildCenter has two subclasses, Lunchbox and
Gymbag, which implement specialized data analysis methods for their nutrition
and fitness build element subclasses, respectively.

A single function is included in this module: build_element. It provides a
convenient way for the application to instantiate build element class objects
by passing it a class ID and, if instantiating a B2 element class, reference
item ID. All build element classes have a class ID (aka 'cid'), which is just
the first letter of the class name. For example, a Diet class ID is 'D'. This
is not a conventional build element property as described above, but rather a
shortcut attribute used by the application to efficiently identify each build
element type before handling them accordingly.

This module also includes a Reference class that can store the properties of
a Food or Exercise reference item. It enables the GUI and input dialogs to pass
reference items back and forth, such as when the user is editing an existing
reference item, while keeping track of any changes made to its properties. The
Reference object, with its changed properties, can be passed to a User method
to make updates to the user's file data.
----------
Build Element Function: function to create new build elements.
    build_element: function to return a new build element class object

Build Element Base Class: base class for all build element classes.
    BuildCenter: QTreeWidgetItem subclass to manage all build elements

Nutrition Build Element Classes: classes to manage nutrition build elements.
    Lunchbox: BuildCenter subclass and nutrition build element superclass
    Quantity: Lunchbox subclass to manage Quantity build elements
    Ingredient: Lunchbox subclass to manage Ingredient build elements
    Recipe: Lunchbox subclass to manage Recipe build elements
    Meal: Lunchbox subclass to manage Meal build elements
    Diet: Lunchbox subclass to manage Diet build elements

Fitness Build Elements Classes: classes to manage fitness build elements.
    Gymbag: BuildCenter subclass and fitness build element superclass
    Session: Gymbag subclass to manage Session build elements
    Activity: Gymbag subclass to manage Activity build elements
    Workout: Gymbag subclass to manage Workout build elements
    Cycle: Gymbag subclass to manage Cycle build elements
    Program: Gymbag subclass to manage Program build elements

Reference Class: class to manage Food and Exercise reference item data.
    Reference: class to store and modify reference data
"""


import datetime

from PyQt4.QtGui import QTreeWidgetItem

import dna
import organs


# -----------------------------------------------------------------------------
# Build Element Function ------------------------------------------------------

def build_element(cid, item_id=None):
    """
    Return a new build element class object.

    This function returns a new instance of the build element class specified
    by the cid (class ID) arg. An optional item_id arg can be passed when a
    Quantity, Ingredient, Session, or Activity object is to be returned. This
    function provides a shorthand way of explicitly calling build element
    constructors each time a new build element class object is needed. Item IDs
    are validated by the GUI before being passed to this function. None is
    returned if the cid arg is not a valid class ID, or if the cid arg is 'Q',
    'I', 'S', or 'A' and item_id=None.

    :param cid: Class ID of the returned build element class object
    :type cid: str
    :param item_id: Reference item ID necessary to construct a Quantity,
        Ingredient, Session, or Activity object
    :type item_id: str
    :return: A new build element class object or None
    :rtype: Quantity, Ingredient, Recipe, Meal, Diet, Session, Activity,
            Workout, Cycle, Program, None
    """
    if cid in ["Q", "I", "S", "A"] and item_id is None:
        return None
    if cid == "Q":
        return Quantity(item_id)
    elif cid == "I":
        return Ingredient(item_id)
    elif cid == "R":
        return Recipe()
    elif cid == "M":
        return Meal()
    elif cid == "D":
        return Diet()
    elif cid == "S":
        return Session(item_id)
    elif cid == "A":
        return Activity(item_id)
    elif cid == "W":
        return Workout()
    elif cid == "C":
        return Cycle()
    elif cid == "P":
        return Program()
    else:
        return None


# -----------------------------------------------------------------------------
# Build Element Base Class ----------------------------------------------------

class BuildCenter(QTreeWidgetItem):
    """
    Base class for build element classes.

    BuildCenter inherits all attributes and methods from the QTreeWidgetItem
    superclass so that its build element subclass objects can be added to the
    Build Viewer, a QTreeWidget object. It implements class attributes which
    store references to the user's Exercise Details, Food Details, and Food
    Nutrients reference dictionaries. It implements a _container instance
    attribute (aka 'the container') to store one or more children--which vary
    depending on the build element subclass. Methods are implemented to assign
    user reference dicts to the class attributes, return the build element
    class ID, modify the children in the container, and update the inherited
    text and children attributes.
    """

    _edref = {}
    _fdref = {}
    _fnref = {}

    @classmethod
    def update_references(cls, **kwargs):
        """
        Assign the user's reference dictionaries to class attributes.

        The Exercise Details (edref), Food Details (fdref), and Food Nutrients
        (fnref) reference dictionaries are passed as keyword arguments to this
        method. Reference dictionaries have the formats:

            --Exercise Details ('edref')--
            {item ID: [description, focus muscle, [metric units], [tags]], ...}
            --Food Details ('fdref')--
            {item ID: [description, group ID, [unit sequences]], ...}
            --Food Nutrients ('fnref')--
            {item ID: {nutrient ID: value for 100 grams of Food, ...}, ...}

        :param kwargs: Exercise Details ('edref'), Food Details ('fdref'), and
               Food Nutrients ('fnref') reference dictionaries
        :param kwargs: dict
        """
        cls._edref = kwargs["edref"]
        cls._fdref = kwargs["fdref"]
        cls._fnref = kwargs["fnref"]

    @classmethod
    def edref(cls):
        """
        Return the user's Exercise Details reference dictionary.

        :return: Exercise Details reference dict
        :rtype: dict
        """
        return cls._edref

    @classmethod
    def fdref(cls):
        """
        Return the user's Food Details reference dictionary.

        :return: Food Details reference dict
        :rtype: dict
        """
        return cls._fdref

    @classmethod
    def fnref(cls):
        """
        Return the user's Food Nutrients reference dictionary.

        :return: Food Nutrients reference dict
        :rtype: dict
        """
        return cls._fnref

    def __init__(self):
        """
        Initialize a BuildCenter object.

        Assigns an empty list to the _container attribute.
        """
        QTreeWidgetItem.__init__(self)
        self._container = []

    def cid(self):
        """
        Return the build element class ID--the first letter of the class name.

        :return: The build element class ID
        :rtype: str
        """
        return self.__class__.__name__[0]

    def container(self):
        """Return the container."""
        return self._container

    def clear_container(self):
        """Assign an empty list to the container."""
        self._container = []

    def add_child(self, child):
        """
        Add a child to the container.

        The child arg is appended to the _container attribute. It must be a
        valid child for the build element subclass. The GUI does not allow an
        invalid child to be passed to this method.

        :param child: A valid nutrition build element class object child
        :type child: Quantity, Ingredient, Recipe, Meal, Session, Activity,
            Workout, Cycle
        """
        self._container.append(child)

    def move_child(self, child, direction):
        """
        Reassign the index of a child object in the container.

        The child arg is a child existing in the _container attribute. Its
        index is incremented or decremented by the number specified by the
        direction arg. The GUI does not allow invalid moves that attempt to
        place the child outside of the container.

        :param child: A child object in the container
        :type child: Quantity, Ingredient, Recipe, Meal, Session, Activity,
            Workout, Cycle
        :param direction: The increment or decrement at which to move the
            child's index within the container
        :type direction: int
        """
        current_index = self._container.index(child)
        new_index = current_index + direction
        self._container.insert(new_index, self._container.pop(current_index))

    def remove_child(self, child):
        """
        Remove a child object from the container.

        The child arg is removed from the container. The GUI does not allow a
        nonexistent child to be passed to this method.

        :param child: A child object in the container
        :type child: Quantity, Ingredient, Recipe, Meal, Session, Activity,
            Workout, Cycle
        """
        self._container.remove(child)

    def widgetize(self):
        """
        Update this object's inherited text and children attributes.

        Methods inherited from the QTreeWidgetItem superclass are called to
        update the--also inherited--text and children attributes. The text
        attribute is assigned the informal string representation of the object.
        The children attribute is cleared of its children and each child object
        in the container is itself widgetized and then added to children. This
        process ensures that all child objects in the container are displayed
        as children in the Build Viewer, and that children and container
        attributes both point to the same set of child objects.
        """
        self.setText(0, str(self))
        self.takeChildren()
        for child in self._container:
            child.widgetize()
            self.addChild(child)


# -----------------------------------------------------------------------------
# Nutrition Build Element Classes ---------------------------------------------

class Lunchbox(BuildCenter):
    """
    Base class for nutrition build element classes.

    Lunchbox inherits all attributes and methods from the BuildCenter
    superclass. It implements data analysis methods that are used by all
    nutrition build element subclasses.
    """

    def __init__(self):
        """Initialize a Lunchbox object."""
        BuildCenter.__init__(self)

    def has_ingredient(self):
        """
        Return True if this element has a constituent Ingredient, else False.

        :return: True if this build element has a constituent Ingredient, else
            False.
        :rtype: bool
        """
        for child in self.container():
            if child.has_ingredient():
                return True
        return False

    def has_quantity(self):
        """
        Return True if this element has a constituent Quantity, else False.

        :return: True if this build element has a constituent Quantity, else
            False
        :rtype: bool
        """
        for child in self.container():
            if child.has_quantity():
                return True
        return False

    def macro_weights(self):
        """
        Return macronutrient gram weights for this object.

        Returns a dictionary with three USDA nutrient IDs as keys: '203' for
        protein, '204' for fat, and '205' for carbohydrate. The gram weight of
        each macronutrient is computed for all constituent Quantities. The
        macro gram weight values are summed and mapped to their respective
        nutrient ID keys in the returned dictionary.

        :return: Gram weights of macronutrients for all constituent Quantities
        :rtype: dict
        """
        total_macro_weights = {"203": 0, "204": 0, "205": 0}
        for child in self.container():
            total_macro_weights = organs.summed_dicts(
                total_macro_weights, child.macro_weights())
        return total_macro_weights

    def nutrient_value(self, nutrient_id):
        """
        Return the total value of the specified nutrient for this object.

        Returns the total numeric value for the nutrient specified by the
        nutrient_id arg for all constituent Quantities.

        :param nutrient_id: A nutrient ID
        :type nutrient_id: str
        :return: Total value of the nutrient for all constituent Quantities
        :rtype: float, int
        """
        total_value = 0
        for child in self.container():
            total_value += child.nutrient_value(nutrient_id)
        return total_value

    def unique_foods(self):
        """
        Return the set of unique Food item IDs referenced by Ingredients.

        :return: All unique Food item IDs referenced by constituent Ingredients
        :rtype: set
        """
        all_foods = set()
        for child in self.container():
            all_foods.update(child.unique_foods())
        return all_foods


class Quantity(Lunchbox):
    """
    Class to store properties of a Quantity build element.

    Quantity inherits all attributes and methods from the Lunchbox superclass.
    Its container stores a single portion size data set--the amount of an
    Ingredient and the unit of measure--rather than another element. Its
    _itemid attribute stores the item ID of the Food item referenced by it and
    its parent Ingredient. The inherited methods add_child, has_quantity,
    macro_weights, nutrient_value, and unique_foods are overridden, and
    additional methods are implemented to return Quantity amount, unit, and
    gram weight, as well as to set and return its state.
    """

    def __init__(self, item_id):
        """
        Initialize a Quantity object.

        Assigns the item_id arg to the _itemid attribute.

        :param item_id: The item ID of the Food referenced by this Quantity
        :type item_id: str
        """
        Lunchbox.__init__(self)
        self._itemid = item_id

    def __str__(self):
        """
        Return the informal string representation of this Quantity.

        :return: The class ID 'Q', the portion amount, and the unit in the
            format: 'Q: <AMOUNT> <UNIT>'
        :rtype: str
        """
        return "Q: " + str(self.amount()) + " " + self.unit()

    def itemid(self):
        """
        Return the referenced Food item ID.

        :return: The referenced Food item ID
        :rtype: str
        """
        return self._itemid

    def add_child(self, child):
        """
        Add a portion size list to this Quantity's container.

        Extends BuildCenter.add_child to clear the container before adding the
        child arg to it. Only one child can be stored by a Quantity at a time.
        The child arg is a portion size data set rather than another nutrition
        build element class object. This list contains two elements: a numeric
        amount as a float or int, and the associated unit of measure string.
        The GUI does not allow an invalid child to be passed to this method.

        :param child: A portion size in the format: [amount, unit]
        :type child: list
        """
        self.clear_container()
        BuildCenter.add_child(self, child)

    def amount(self):
        """
        Return the amount of this Quantity's portion size.

        :return: Numeric amount of this Quantity's portion size, or zero if
            the container is empty
        :rtype: float, int
        """
        return self.container()[0][0] if self.container() else 0

    def unit(self):
        """
        Return the unit of measure of this Quantity's portion size.

        :return: Unit of measure of this Quantity's portion size, or 'no unit'
            if the container is empty
        :rtype: str
        """
        return self.container()[0][1] if self.container() else "no unit"

    def weight(self):
        """
        Return the gram weight of this Quantity's portion size.

        If the container is empty or the portion size unit is not found in the
        unit sequences of the referenced Food item, zero is returned. If the
        portion size unit is 'g', indicating grams, the gram weight of the
        portion size is the same as the numeric amount, and so the amount is
        returned.

        :return: Weight in grams (g) of this Quantity's portion size
        :rtype: float, int
        """
        amount = self.amount()
        unit = self.unit()
        if amount == 0:
            return 0
        if unit == "g":
            return amount
        else:
            for sequence in self.fdref()[self._itemid][2]:
                seq_unit = sequence[1]
                if seq_unit == unit:
                    seq_amount = sequence[0]
                    seq_weight = sequence[2]
                    return (amount / float(seq_amount)) * seq_weight
        return 0

    def has_quantity(self):
        """
        Return True since this build element is indeed a Quantity.

        :return: True
        :rtype: bool
        """
        return True

    def macro_weights(self):
        """
        Return macronutrient gram weights for this Quantity.

        Overrides Lunchbox.macro_weights to compute macronutrient gram weights
        for only this Quantity. Calls the nutrient_value method on each of the
        three macronutrient IDs to compute its gram weight.

        :return: Gram weights of macronutrients for all constituent Quantities
        :rtype: dict
        """
        macro_weights = {"203": 0, "204": 0, "205": 0}
        for nutrient_id in macro_weights:
            macro_weights[nutrient_id] = self.nutrient_value(nutrient_id)
        return macro_weights

    def nutrient_value(self, nutrient_id):
        """
        Return the value of the specified nutrient for this Quantity.

        Overrides Lunchbox.nutrient_value to compute a nutrient value for only
        this Quantity. If a nutrient value is not found for the referenced Food
        item ID in the Food Nutrients reference dict, zero is returned. Note
        that the value found for a nutrient in the Food Nutrients reference
        dict is for 100 grams of the Food item.

        :param nutrient_id: A nutrient ID
        :type nutrient_id: str
        :return: Value of the nutrient for this Quantity
        :rtype: float, int
        """
        try:
            hectogram_value = self.fnref()[self._itemid][nutrient_id]
            return (self.weight() / 100.0) * hectogram_value
        except KeyError:
            return 0

    def unique_foods(self):
        """
        Return a set with the referenced Food item ID.

        Overrides Lunchbox.unique_foods to return a set with the _itemid
        attribute, i.e. the only Food item referenced by this Quantity.

        :return: A set with the referenced Food item ID
        :rtype: set
        """
        return {self._itemid}

    def set_state(self, new_state):
        """
        Set the state of this Quantity.

        The new_state arg is a list with the format:

            ['Q', amount_number, unit_str]

        -where 'Q' is the Quantity class ID, amount_number is the portion size
        amount float or int, and unit_str is the portion size unit of measure
        string. The _itemid attribute is not included in a Quantity state list
        because its set_state method is only called by the parent Ingredient's
        set_state method and the Ingredient's own _itemid attribute can be
        passed to the Quantity constructor. The GUI does not allow invalid
        new_state args to be passed to this method.

        :param new_state: Quantity state with the format: ['Q', portion size
            amount, portion size unit]
        :type new_state: list
        """
        self.add_child(new_state[1:])

    def state(self):
        """
        Return the state of this Quantity.

        The state is returned with the format:

            ['Q', amount_number, unit_str]

        -where 'Q' is the Quantity class ID, amount_number is the portion size
        amount float or int, and unit_str is the portion size unit of measure
        string. The _itemid attribute is not included in a Quantity state list
        because its set_state method is only called by the parent Ingredient's
        set_state method and the Ingredient's own _itemid attribute can be
        passed to the Quantity constructor.

        :return: Quantity state with the format: ['Q', portion size amount,
            portion size unit]
        :rtype: list
        """
        return ["Q", self.amount(), self.unit()]


class Ingredient(Lunchbox):
    """
    Class to store properties of an Ingredient build element.

    Ingredient inherits all attributes and methods from the Lunchbox
    superclass. Its container stores Quantity objects. Its _itemid attribute
    stores the item ID of the Food item referenced by it and its child
    Quantities. The inherited methods has_ingredient, unique_foods, and
    widgetize are overridden, and additional methods are implemented to return
    Food reference item properties and set and return its state.
    """

    def __init__(self, item_id):
        """
        Initialize an Ingredient object.

        Assigns the item_id arg to the _itemid attribute.

        :param item_id: The item ID of the Food referenced by this Ingredient
        :type item_id: str
        """
        Lunchbox.__init__(self)
        self._itemid = item_id

    def __str__(self):
        """
        Return the informal string representation of this Ingredient.

        :return: The class ID 'I' and the description of the referenced Food
            item in the format: 'I: <DESCRIPTION>'
        :rtype: str
        """
        return "I: " + self.description()

    def itemid(self):
        """
        Return the referenced Food item ID.

        :return: The referenced Food item ID
        :rtype: str
        """
        return self._itemid

    def description(self):
        """
        Return the description of the referenced Food item.

        :return: The description of the referenced Food item
        :rtype: str
        """
        return self.fdref()[self._itemid][0]

    def groupid(self):
        """
        Return the food group ID of the referenced Food item.

        :return: The food group ID of the referenced Food item
        :rtype: str
        """
        return self.fdref()[self._itemid][1]

    def unitsequences(self):
        """
        Return the unit sequences of the referenced Food item.

        :return: The unit sequences of the referenced Food item
        :rtype: list
        """
        return self.fdref()[self._itemid][2]

    def nutrientcontent(self):
        """
        Return nutrient content of the referenced Food item.

        :return: The nutrient content of the referenced Food item
        :rtype: dict
        """
        return self.fnref()[self._itemid]

    def has_ingredient(self):
        """
        Return True since this build element is indeed an Ingredient.

        :return: True
        :rtype: bool
        """
        return True

    def unique_foods(self):
        """
        Return a set with the referenced Food item ID.

        Overrides Lunchbox.unique_foods to return a set with the _itemid
        attribute, i.e. the only Food item referenced by this Ingredient.

        :return: A set with the referenced Food item ID
        :rtype: set
        """
        return {self._itemid}

    def widgetize(self):
        """
        Update this object's text and children in the Build Viewer.

        Overrides BuildCenter.widgetize to update this object without calling
        widgetize on the Quantity objects in its container. Instead, the
        inherited setText method is called on each child so that its text
        is updated in the Build Viewer.
        """
        self.setText(0, str(self))
        self.takeChildren()
        for child in self.container():
            child.setText(0, str(child))
            self.addChild(child)

    def set_state(self, new_state):
        """
        Set the state of this Ingredient.

        The new_state arg is a list with the format:

            ['I', [quantity_state_list, ...], itemid_str]

        -where 'I' is the Ingredient class ID, quantity_state_list is the state
        of each Quantity to add to the container, and itemid_str is the
        referenced Food item ID. This method does not assign itemid_str to the
        _itemid attribute after instantiation, as it assumes that the same item
        ID has already been passed to the Ingredient constructor by the parent
        Recipe or Meal that is executing its own set_state method. The GUI does
        not allow invalid new_state args to be passed to this method.

        :param new_state: Ingredient state with the format: ['I',
            [quantity state, ...], Food item ID]
        :type new_state: list
        """
        self.clear_container()
        for quantity_state in new_state[1]:
            quantity = Quantity(self._itemid)
            quantity.set_state(quantity_state)
            self.add_child(quantity)

    def state(self):
        """
        Return the state of this Ingredient.

        The state is returned with the format:

            ['I', [quantity_state_list, ...], itemid_str]

        -where 'I' is the Ingredient class ID, quantity_state_list is the state
        of each Quantity in the container, and itemid_str is the referenced
        Food item ID.

        :return: Ingredient state with the format: ['I', [quantity state, ...],
            Food item ID]
        :rtype: list
        """
        quantity_states = [quantity.state() for quantity in self.container()]
        return ["I", quantity_states, self._itemid]


class Recipe(Lunchbox):
    """
    Class to store properties of a Recipe build element.

    Recipe inherits all attributes and methods from the Lunchbox superclass.
    Its container stores Recipe and Ingredient objects. Its _description
    attribute stores a description of the Recipe, and its _portion attribute
    stores its portion size list. The inherited methods macro_weights and
    nutrient_value are extended, and additional methods are implemented to set
    and return its _description and _portion attributes, set and return its
    state, and return its template state.
    """

    def __init__(self):
        """
        Initialize a Recipe object.

        Assigns placeholder text '(unnamed)' to the _description attribute and
        default portion size [1, 1, 'piece'] to the _portion attribute.
        """
        Lunchbox.__init__(self)
        self._description = "(unnamed)"
        self._portion = [1, 1, "piece"]

    def __str__(self):
        """
        Return the informal string representation of this Recipe.

        :return: The class ID 'R', the description, and the portion size
            components in the format:
            'R: <DESCRIPTION> -> <CONSUMED AMOUNT> of <PREPARED AMOUNT> <UNIT>'
        :rtype: str
        """
        string = self._description + " -> " + str(self.consumed()) + " of "
        string += str(self.prepared()) + " " + self.unit()
        return "R: " + string

    def description(self):
        """
        Return the description.

        :return: The Recipe description
        :rtype: str
        """
        return self._description

    def set_description(self, new_description):
        """
        Set the description.

        :param new_description: A new Recipe description
        :type new_description: str
        """
        self._description = new_description

    def portion(self):
        """
        Return the portion.

        :return: The Recipe portion list in the format: [consumed amount,
            prepared amount, unit of measure]
        :rtype: list
        """
        return self._portion

    def set_portion(self, new_portion):
        """
        Set the portion.

        The new_portion arg is a list with three elements: the numeric amount
        of the Recipe that was consumed by the user, the numeric amount of the
        Recipe that was prepared, and the unit of measure associated with both
        amounts. For example, [25.5, 350, 'grams'] would be a valid new_portion
        arg, indicating that the prepared Recipe weighed 350 grams and the user
        consumed 25.5 grams of it during a Meal. The GUI prevents invalid
        new_portion args from being passed to this method. The consumed and
        prepared amounts are restricted to positive values to prevent the
        storage of useless Recipe data and division by zero, respectively.

        :param new_portion: A new portion list in the format: [consumed amount,
            prepared amount, unit of measure]
        :type new_portion: list
        """
        self._portion = new_portion

    def consumed(self):
        """
        Return the portion consumed amount.

        :return: The amount of the Recipe that the user consumed
        :rtype: float, int
        """
        return self._portion[0]

    def prepared(self):
        """
        Return the portion prepared amount.

        :return: The amount of the Recipe that the user prepared
        :rtype: float, int
        """
        return self._portion[1]

    def unit(self):
        """
        Return the portion unit.

        :return: The unit of measure associated with consumed and prepared
            amounts
        :rtype: str
        """
        return self._portion[2]

    def macro_weights(self):
        """
        Return macronutrient gram weights for this Recipe.

        Extends Lunchbox.macro_weights to adjust the gram weight values for
        the portion size of this Recipe.

        :return: Gram weights of macronutrients for all constituent Quantities
        :rtype: dict
        """
        total_macro_weights = Lunchbox.macro_weights(self)
        multiplier = self.consumed() / float(self.prepared())
        for macro_id in total_macro_weights:
            total_macro_weights[macro_id] *= multiplier
        return total_macro_weights

    def nutrient_value(self, nutrient_id):
        """
        Return the total value of the specified nutrient for this Recipe.

        Extends Lunchbox.nutrient_value to adjust the nutrient value for the
        portion size of this Recipe.

        :param nutrient_id: Nutrient ID for which the total value is returned
        :type nutrient_id: str
        :return: Total value of the nutrient for this Recipe
        :rtype: float, int
        """
        multiplier = self.consumed() / float(self.prepared())
        return Lunchbox.nutrient_value(self, nutrient_id) * multiplier

    def set_state(self, new_state):
        """
        Set the state of this Recipe.

        The new_state arg is a list with the format:

            ['R', [child_state_list, ...], description_str,
             [consumed_number, prepared_number, unit_str]]

        -where 'R' is the Recipe class ID, child_state_list is the state of
        each Recipe or Ingredient to add to the container, description_str is
        the description, consumed_number is the portion consumed amount,
        prepared_number is the portion prepared amount, and unit_str is the
        portion unit of measure. The GUI does not allow invalid new_state args
        to be passed to this method.

        :param new_state: Recipe state with the format: ['R',
            [child state, ...], description, [consumed amount, prepared amount,
            unit of measure]]
        :type new_state: list
        """
        self.clear_container()
        for child_state in new_state[1]:
            item_id = None if child_state[0] == "R" else child_state[2]
            child_object = build_element(child_state[0], item_id)
            child_object.set_state(child_state)
            self.add_child(child_object)
        self.set_description(new_state[2])
        self.set_portion(new_state[3])

    def state(self):
        """
        Return the state of this Recipe.

        The state is returned with the format:

            ['R', [child_state_list, ...], description_str,
             [consumed_number, prepared_number, unit_str]]

        -where 'R' is the Recipe class ID, child_state_list is the state of
        each Recipe or Ingredient in the container, description_str is the
        description, consumed_number is the portion consumed amount,
        prepared_number is the portion prepared amount, and unit_str is the
        portion unit of measure.

        :return: Recipe state with the format: ['R', [child state, ...],
            description, [consumed amount, prepared amount, unit of measure]]
        :rtype: list
        """
        child_states = [child.state() for child in self.container()]
        return ["R", child_states, self._description, self._portion]

    def template_state(self):
        """
        Return the template state of this Recipe.

        The template state is returned with the format:

            ['R', [child_state_list, ...], description_str,
             [consumed_number, prepared_number, unit_str]]

        -where 'R' is the Recipe class ID, child_state_list is the state of
        each Recipe or Ingredient in the container, description_str is the
        description, consumed_number is the portion consumed amount,
        prepared_number is the portion prepared amount, and unit_str is the
        portion unit of measure. The template state is the same as the state.

        :return: Recipe template state with the format: ['R',
            [child state, ...], description, [consumed amount, prepared amount,
            unit of measure]]
        :rtype: list
        """
        return self.state()


class Meal(Lunchbox):
    """
    Class to store properties of a Meal build element.

    Meal inherits all attributes and methods from the Lunchbox superclass. Its
    container stores Recipe and Ingredient objects. Its _description attribute
    stores a description of the Meal, and its _time attribute stores the time
    at which it was consumed. Methods are implemented to set and return its
    _description and _time attributes, set and return its state, and return its
    template state.
    """

    def __init__(self):
        """
        Initialize a Meal object.

        Assigns placeholder text '(unnamed)' to the _description attribute and
        default datetime.time object datetime.time(0) (12:00 AM) to the _time
        attribute.
        """
        Lunchbox.__init__(self)
        self._description = "(unnamed)"
        self._time = datetime.time(0)

    def __str__(self):
        """
        Return the informal string representation of this Meal.

        :return: The class ID 'M', the description, and the time in the format:
            'M: <DESCRIPTION> -> <TIME(H:M)>'
        :rtype: str
        """
        return "M: " + self._description + " -> " + str(self._time)[:-3]

    def description(self):
        """
        Return the description.

        :return: The Meal description
        :rtype: str
        """
        return self._description

    def set_description(self, new_description):
        """
        Set the description.

        :param new_description: A new Meal description
        :type new_description: str
        """
        self._description = new_description

    def time(self):
        """
        Return the time.

        :return: The Meal time
        :rtype: datetime.time
        """
        return self._time

    def set_time(self, new_time):
        """
        Set the time.

        The GUI prevents invalid new_time args from being passed to this
        method.

        :param new_time: A new Meal time
        :type new_time: datetime.time
        """
        self._time = new_time

    def set_state(self, new_state):
        """
        Set the state of this Meal.

        The new_state arg is a list with the format:

            ['M', [child_state_list, ...], description_str, time_str]

        -where 'M' is the Meal class ID, child_state_list is the state of each
        Recipe or Ingredient to add to the container, description_str is the
        description, and time_str is the time as a string with the time format
        '%H:%M' (hours and minutes in 24-hour clock time). The GUI does not
        allow invalid new_state args to be passed to this method.

        :param new_state: Meal state with the format: ['M', [child state, ...],
            description, time]
        :type new_state: list
        """
        self.clear_container()
        for child_state in new_state[1]:
            item_id = None if child_state[0] == "R" else child_state[2]
            child_object = build_element(child_state[0], item_id)
            child_object.set_state(child_state)
            self.add_child(child_object)
        self.set_description(new_state[2])
        self.set_time(datetime.datetime.strptime(new_state[3], "%H:%M").time())

    def state(self):
        """
        Return the state of this Meal.

        The state is returned with the format:

            ['M', [child_state_list, ...], description_str, time_str]

        -where 'M' is the Meal class ID, child_state_list is the state of each
        Recipe or Ingredient in the container, description_str is the
        description, and time_str is the time as a string with the time format
        '%H:%M' (hours and minutes in 24-hour clock time).

        :return: Meal state with the format: ['M', [child state, ...],
            description, time]
        :rtype: list
        """
        child_states = [child.state() for child in self.container()]
        return ["M", child_states, self._description,
                self._time.strftime("%H:%M")]

    def template_state(self):
        """
        Return the template state of this Meal.

        The template state is returned with the format:

            ['M', [child_state_list, ...], description_str, '00:00']

        -where 'M' is the Meal class ID, child_state_list is the state of each
        Recipe or Ingredient in the container, and description_str is the
        description. The states of the Recipe and Ingredient objects in the
        container remain unchanged (each object's template state is the same as
        its state), however, the time string is replaced with '00:00', the
        default time value when a Meal is constructed. Saving Meal templates
        with default times forces the user to reenter the time property each
        time a Meal template is used.

        :return: Meal template state with the format: ['M', [child state, ...],
            description, '00:00']
        :rtype: list
        """
        return self.state()[:3] + ["00:00"]


class Diet(Lunchbox):
    """
    Class to store properties of a Diet build element.

    Diet inherits all attributes and methods from the Lunchbox superclass. Its
    container stores Meal objects. Its _description attribute stores a
    description of the Diet, and its _date attribute stores the date on which
    it was consumed. Methods are implemented to return child Meal times, set
    and return its _description and _date attributes, set and return its state,
    and return its template state.
    """

    def __init__(self):
        """
        Initialize a Diet object.

        Assign placeholder text '(unnamed)' to the _description attribute and
        the default date datetime.date.now().date() to the _date attribute.
        """
        Lunchbox.__init__(self)
        self._description = "(unnamed)"
        self._date = datetime.datetime.now().date()

    def __str__(self):
        """
        Return the informal string representation of this Diet.

        :return: The class ID 'D', the description, and the date in the format:
            'D: <DESCRIPTION> -> <DATE(Y-m-d)>'
        :rtype: str
        """
        return "D: " + self._description + " -> " + str(self._date)

    def description(self):
        """
        Return the description.

        :return: The Diet description
        :rtype: str
        """
        return self._description

    def set_description(self, new_description):
        """
        Set the description.

        :param new_description: A new Diet description
        :type new_description: str
        """
        self._description = new_description

    def date(self):
        """
        Return the date.

        :return: The Diet date
        :rtype: datetime.date
        """
        return self._date

    def set_date(self, new_date):
        """
        Set the date.

        The GUI prevents invalid new_date args from being passed to this
        method.

        :param new_date: A new Diet date
        :type new_date: datetime.date
        """
        self._date = new_date

    def meal_times(self):
        """
        Return a sorted list of all child Meal times.

        :return: A sorted list of Meal times, each in the format 'HH:MM'
        :rtype: list
        """
        return sorted([str(meal.time())[:-3] for meal in self.container()])

    def set_state(self, new_state):
        """
        Set the state of this Diet.

        The new_state arg is a list with the format:

            ['D', [meal_state_list, ...], description_str, date_str_or_None]

        -where 'D' is the Diet class ID, meal_state_list is the state of each
        Meal to add to the container, description_str is the description, and
        date_str_or_None is the date as a string with the date format
        '%Y-%m-%d' or, if the new_state arg is a template state, None. If the
        date is None, the default datetime.datetime.now().date() value is
        assigned to the _date attribute. The GUI does not allow invalid
        new_state args to be passed to this method.

        :param new_state: Diet state with the format: ['D', [meal state, ...],
            description, date]
        :type new_state: list
        """
        self.clear_container()
        for meal_state in new_state[1]:
            meal = Meal()
            meal.set_state(meal_state)
            self.add_child(meal)
        self.set_description(new_state[2])
        if new_state[3] is None:
            new_date = datetime.datetime.now().date()
        else:
            new_date = datetime.datetime.strptime(
                new_state[3], "%Y-%m-%d").date()
        self.set_date(new_date)

    def state(self):
        """
        Return the state of this Diet.

        The state is returned with the format:

            ['D', [meal_state_list, ...], description_str, date_str]

        -where 'D' is the Diet class ID, meal_state_list is the state of each
        Meal in the container, description_str is the description, and date_str
        is the date as a string with the date format '%Y-%m-%d'.

        :return: Diet state with the format: ['D', [meal state, ...],
            description, date]
        :rtype: list
        """
        meal_states = [meal.state() for meal in self.container()]
        return ["D", meal_states, self._description,
                self._date.strftime("%Y-%m-%d")]

    def template_state(self):
        """
        Return the template state of this Diet.

        The template state is returned with the format:

            ['D', [meal_template_state_list, ...], description_str, None]

        -where 'D' is the Diet class ID, meal_template_state_list is the
        template state of each Meal in the container, and description_str is
        the description. The date string is replaced with None, which
        indicates to the set_state method that the _date attribute is to be
        assigned a datetime.datetime.now().date() object, the default date
        value when a Diet is constructed. Saving Diet templates with None
        instead of dates forces the user to reenter the date property each time
        a Diet template is used. It also assumes that a Diet template loaded
        into the Build Viewer will be used for the current date, which is
        generally the case.

        :return: Diet template state with the format: ['D',
            [meal template state, ...], description, None]
        :rtype: list
        """
        meal_tem_states = [meal.template_state() for meal in self.container()]
        return ["D", meal_tem_states, self._description, None]


# -----------------------------------------------------------------------------
# Fitness Build Element Classes

class Gymbag(BuildCenter):
    """
    Base class for fitness build element classes.

    Gymbag inherits all attributes and methods from the BuildCenter superclass.
    It implements data analysis methods that are used by all fitness build
    element subclasses.
    """

    def __init__(self):
        """Initialize a Gymbag object."""
        BuildCenter.__init__(self)

    def has_activity(self):
        """
        Return True if this element has a constituent Activity, else False.

        :return: True if this build element has a constituent Activity, else
            False.
        :rtype: bool
        """
        for child in self.container():
            if child.has_activity():
                return True
        return False

    def has_session(self):
        """
        Return True if this element has a constituent Session, else False.

        :return: True if this build element has a constituent Session, else
            False
        :rtype: bool
        """
        for child in self.container():
            if child.has_session():
                return True
        return False

    def muscle_sessions(self):
        """
        Return the total number of Sessions per focus muscle.

        :return: Total Sessions per focus muscle for all constituent Sessions
        :rtype: dict
        """
        sessions_per_muscle = dict()
        for child in self.container():
            sessions_per_muscle = organs.summed_dicts(
                sessions_per_muscle, child.muscle_sessions())
        return sessions_per_muscle

    def performance_results(self, results_type, exercise_property):
        """
        Return performance results per Exercise property per Workout.

        Returns a performance results dictionary with constituent Workout
        period began datetime strings as keys mapped to individual Workout
        performance results dicts. Each Workout performance results dict has
        as its keys all properties, as specified by the exercise_property arg,
        of Exercise items referenced by its constituent Sessions. Each key is
        mapped to the performance result value specified by the results_type
        arg. Result values are calculated for all constituent Sessions that
        reference Exercise items with that property value. The basic format is:

            {Workout period began: {
                Exercise property: result value for all Sessions, ...}, ...}

        The results_type arg is either 'effort', 'intensity', or 'magnitude'.
        Effort and magnitude results are calculated by summing the effort and
        magnitude values of all applicable constituent Sessions. The intensity
        result is calculated by finding the maximum intensity value among all
        applicable constituent Sessions. The exercise_property arg is either
        'itemid', 'focusmuscle', or 'tags'. Result values are, respectively,
        mapped to the item ID, focus muscle, or all tags of the Exercise item.

        :param results_type: The type of performance results: 'effort' for
            total effort sum, 'intensity' for maximum intensity, 'magnitude'
            for total magnitude sum
        :type results_type: str
        :param exercise_property: The Exercise property to which performance
            results are mapped: 'itemid' for Exercise item ID, 'focusmuscle'
            for focus muscle, 'tags' for tags
        :type exercise_property: str
        :return: Performance results per Exercise property per constituent
            Workout
        :rtype: dict
        """
        total_performance = dict()
        for child in self.container():
            total_performance.update(
                child.performance_results(results_type, exercise_property))
        return total_performance

    def unique_exercises(self):
        """
        Return the set of unique Exercise item IDs referenced by Activities.

        :return: All unique Exercise item IDs referenced by constituent
            Activities
        :rtype: set
        """
        all_exercises = set()
        for child in self.container():
            all_exercises.update(child.unique_exercises())
        return all_exercises

    def unique_focusmuscles(self):
        """
        Return the set of unique focus muscles referenced by Activities.

        :return: All unique focus muscles for Exercise items referenced by
            constituent Activities
        :rtype: set
        """
        all_muscles = set()
        for child in self.container():
            all_muscles.update(child.unique_focusmuscles())
        return all_muscles

    def unique_tags(self):
        """
        Return the set of unique tags referenced by Activities.

        :return: All unique tags for Exercise items referenced by constituent
            Activities
        :rtype: set
        """
        all_tags = set()
        for child in self.container():
            all_tags.update(child.unique_tags())
        return all_tags


class Session(Gymbag):
    """
    Class to store properties of a Session build element.

    Session inherits all attributes and methods from the Gymbag superclass. Its
    container stores a single performance measurement data set--the effort
    amount, intensity amount, and optional note--rather than another element.
    Its _itemid attribute stores the item ID of the Exercise item referenced by
    it and its parent Activity. The inherited methods add_child, has_session,
    muscle_sessions, performance_results, unique_exercises,
    unique_focusmuscles, and unique_tags are overridden, and additional methods
    are implemented to return Session effort, intensity, note, and magnitude,
    return Exercise reference item properties, and set and return its state.
    """

    def __init__(self, item_id):
        """
        Initialize a Session object.

        Assigns the item_id arg to the _itemid attribute.

        :param item_id: The item ID of the Exercise referenced by this Session
        :type item_id: str
        """
        Gymbag.__init__(self)
        self._itemid = item_id

    def __str__(self):
        """
        Return the informal string representation of this Session.

        If the Session note is an empty string, the string returned by this
        method ends at the intensity unit. If not, the note is appended to
        the returned string as ' -> <NOTE>'.

        :return: The class ID 'S', the effort amount, the intensity amount,
            and the note in the format:
            'S: <EFFORT> <EFF.UNIT> at <INTENSITY> <INT.UNIT> -> <NOTE>'
        :rtype: str
        """
        # Example string: '4 rep at 200 lb -> superset'
        units = self.edref()[self._itemid][2]
        result_string = str(self.effort()) + " " + units[0] + " at "
        result_string += str(self.intensity()) + " " + units[1]
        note_string = " -> " + self.note() if self.note() != "" else ""
        return "S: " + result_string + note_string

    def itemid(self):
        """
        Return the referenced Exercise item ID.

        :return: The referenced Exercise item ID
        :rtype: str
        """
        return self._itemid

    def add_child(self, child):
        """
        Add a performance measurement list to this Session's container.

        Extends BuildCenter.add_child to clear the container before adding the
        child arg to it. Only one child can be stored by a Session at a time.
        The child arg is a performance measurement data set rather than another
        fitness build element class object. This list contains three elements:
        a numeric effort amount, a numeric intensity amount, and a note string.
        The GUI does not allow an invalid child to be passed to this method.

        :param child: A performance measurement in the format:
            [effort amount, intensity amount, note]
        :type child: list
        """
        self.clear_container()
        BuildCenter.add_child(self, child)

    def effort(self):
        """
        Return the effort amount of this Session's performance measurement.

        :return: Numeric effort amount of this Session's performance
            measurement, or zero if the container is empty
        :rtype: float, int
        """
        return self.container()[0][0] if self.container() else 0

    def intensity(self):
        """
        Return the intensity amount of this Session's performance measurement.

        :return: Numeric intensity amount of this Session's performance
            measurement, or zero if the container is empty
        :rtype: float, int
        """
        return self.container()[0][1] if self.container() else 0

    def note(self):
        """
        Return the note of this Session's performance measurement.

        :return: Textual note of this Session's performance measurement, or an
            empty string if the container is empty
        :rtype: str
        """
        return self.container()[0][2] if self.container() else ""

    def magnitude(self):
        """
        Return the magnitude of this Session's performance measurement.

        :return: Numeric magnitude of this Session's performance measurement
            calculated by multiplying effort times intensity, or zero if the
            container is empty
        :rtype: float, int
        """
        return self.effort() * self.intensity()

    def description(self):
        """
        Return the description of the referenced Exercise item.

        :return: The description of the referenced Exercise item
        :rtype: str
        """
        return self.edref()[self._itemid][0]

    def focusmuscle(self):
        """
        Return the focus muscle of the referenced Exercise item.

        :return: The focus muscle of the referenced Exercise item
        :rtype: str
        """
        return self.edref()[self._itemid][1]

    def units(self):
        """
        Return performance metric units of the referenced Exercise item.

        :return: The performance metric units of the referenced Exercise item
        :rtype: list
        """
        return self.edref()[self._itemid][2]

    def tags(self):
        """
        Return the tags of the referenced Exercise item.

        :return: The tags of the referenced Exercise item
        :rtype: list
        """
        return self.edref()[self._itemid][3]

    def has_session(self):
        """
        Return True since this build element is indeed a Session.

        :return: True
        :rtype: bool
        """
        return True

    def muscle_sessions(self):
        """
        Return the number of Sessions per focus muscle.

        Overrides Gymbag.muscle_sessions to return a dict with the focus muscle
        of the referenced Exercise item as a key mapped to the value 1.

        :return: A dictionary with the referenced Exercise item's focus muscle
            mapped to the value 1
        :rtype: dict
        """
        return {self.focusmuscle(): 1}

    def performance_results(self, results_type, exercise_property):
        """
        Return performance results for the referenced Exercise item.

        Overrides Gymbag.performance_results to return a performance results
        dictionary with the referenced Exercise item's property, as specified
        by the exercise_property arg, as a key mapped to the performance result
        value, as specified by the results_type arg, for this Session. The
        basic format is:

            {Exercise property: result value for this Session}

        The results_type arg is either 'effort', 'intensity', or 'magnitude'.
        The former two results correspond to this Session's analogous
        attributes which return elements of the performance measurement stored
        in the container. The magnitude value is calculated by multiplying the
        effort and intensity values. The exercise_property arg is either
        'itemid', 'focusmuscle', or 'tags'. The result value is, respectively,
        mapped to the item ID, focus muscle, or all tags of the referenced
        Exercise item.

        :param results_type: The type of performance results: 'effort' for
            total effort sum, 'intensity' for maximum intensity, 'magnitude'
            for total magnitude sum
        :type results_type: str
        :param exercise_property: The Exercise property to which performance
            results are mapped: 'itemid' for Exercise item ID, 'focusmuscle'
            for focus muscle, 'tags' for tags
        :type exercise_property: str
        :return: Performance result per property of referenced Exercise item
        :rtype: dict
        """
        if not self.container():
            return {}
        performance = getattr(self, results_type)()
        ex_property = getattr(self, exercise_property)()
        keys = ex_property if exercise_property == "tags" else [ex_property]
        return {key: performance for key in keys}

    def unique_exercises(self):
        """
        Return a set with the referenced Exercise item ID.

        Overrides Gymbag.unique_exercises to return a set with the _itemid
        attribute, i.e. the only Exercise item referenced by this Session.

        :return: A set with the referenced Exercise item ID
        :rtype: set
        """
        return {self._itemid}

    def unique_focusmuscles(self):
        """
        Return a set with the focus muscle of the referenced Exercise item.

        Overrides Gymbag.unique_focusmuscles to return a set with the focus
        muscle of the referenced Exercise item.

        :return: A set with the focus muscle of the referenced Exercise item
        :rtype: set
        """
        return {self.focusmuscle()}

    def unique_tags(self):
        """
        Return a set with the tags of the referenced Exercise item.

        Overrides Gymbag.unique_tags to return a set with the tags of the
        referenced Exercise item.

        :return: A set with the tags of the referenced Exercise item
        :rtype: set
        """
        return set(self.tags())

    def set_state(self, new_state):
        """
        Set the state of this Session.

        The new_state arg is a list with the format:

            ['S', effort_number, intensity_number, note_str]

        -where 'S' is the Session class ID, effort_number is the performance
        measurement effort amount float or int, intensity_number is the
        performance measurement intensity amount float or int, and note_str is
        the performance measurement note string. The _itemid attribute is not
        included in a Session state list because its set_state method is only
        called by the parent Activity's set_state method and the Activity's
        own _itemid attribute can be passed to the Session constructor. The GUI
        does not allow invalid new_state args to be passed to this method.

        :param new_state: Session state with the format: ['S', performance
            measurement effort, performance measurement intensity, performance
            measurement note]
        :type new_state: list
        """
        self.add_child(new_state[1:])

    def state(self):
        """
        Return the state of this Session.

        The state is returned with the format:

            ['S', effort_number, intensity_number, note_str]

        -where 'S' is the Session class ID, effort_number is the performance
        measurement effort amount float or int, intensity_number is the
        performance measurement intensity amount float or int, and note_str is
        the performance measurement note string. The _itemid attribute is not
        included in a Session state list because its set_state method is only
        called by the parent Activity's set_state method and the Activity's
        own _itemid attribute can be passed to the Session constructor.

        :return: Session state with the format: ['S', performance measurement
            effort, performance measurement intensity, performance measurement
            note]
        :rtype: list
        """
        return ["S", self.effort(), self.intensity(), self.note()]


class Activity(Gymbag):
    """
    Class to store properties of an Activity build element.

    Activity inherits all attributes and methods from the Gymbag superclass.
    Its container stores Session objects. Its _itemid attribute stores the
    item ID of the Exercise item referenced by it and its child Sessions. The
    inherited methods has_activity, muscle_sessions, performance_results,
    unique_exercises, unique_focusmuscles, unique_tags, and widgetize are
    overridden, and additional methods are implemented to return Exercise
    reference item properties, set and return its state, and return its
    template state.
    """

    def __init__(self, item_id):
        """
        Initialize an Activity object.

        Assigns the item_id arg to the _itemid attribute.

        :param item_id: The item ID of the Exercise referenced by this Activity
        :type item_id: str
        """
        Gymbag.__init__(self)
        self._itemid = item_id

    def __str__(self):
        """
        Return the informal string representation of this Activity.

        :return: The class ID 'A' and the description of the referenced
            Exercise item in the format: 'A: <DESCRIPTION>'
        :rtype: str
        """
        return "A: " + self.description()

    def itemid(self):
        """
        Return the referenced Exercise item ID.

        :return: The referenced Exercise item ID
        :rtype: str
        """
        return self._itemid

    def description(self):
        """
        Return the description of the referenced Exercise item.

        :return: The description of the referenced Exercise item
        :rtype: str
        """
        return self.edref()[self._itemid][0]

    def focusmuscle(self):
        """
        Return the focus muscle of the referenced Exercise item.

        :return: The focus muscle of the referenced Exercise item
        :rtype: str
        """
        return self.edref()[self._itemid][1]

    def units(self):
        """
        Return the performance metric units of the referenced Exercise item.

        :return: The performance metric units of the referenced Exercise item
        :rtype: list
        """
        return self.edref()[self._itemid][2]

    def tags(self):
        """
        Return the tags of the referenced Exercise item.

        :return: The info tags of the referenced Exercise item
        :rtype: list
        """
        return self.edref()[self._itemid][3]

    def has_activity(self):
        """
        Return True since this build element is indeed an Activity.

        :return: True
        :rtype: bool
        """
        return True

    def muscle_sessions(self):
        """
        Return the number of Sessions per focus muscle.

        Overrides Gymbag.muscle_sessions to return a dict with the focus muscle
        of the referenced Exercise item as a key mapped to the number of child
        Sessions.

        :return: A dictionary with the referenced Exercise item's focus muscle
            mapped to the number of child Sessions
        :rtype: dict
        """
        if self.container():
            return {self.focusmuscle(): len(self.container())}
        else:
            return {}

    def performance_results(self, results_type, exercise_property):
        """
        Return performance result for the referenced Exercise item.

        Overrides Gymbag.performance_results to return a performance results
        dictionary with the referenced Exercise item's property, as specified
        by the exercise_property arg, as a key mapped to the performance result
        value, as specified by the results_type arg, for all child Sessions.
        The basic format is:

            {Exercise property: result value for all child Sessions}

        The results_type arg is either 'effort', 'intensity', or 'magnitude'.
        Effort and magnitude results are calculated by summing the effort and
        magnitude values of all child Sessions. The intensity result is
        calculated by finding the maximum intensity value of all child
        Sessions. The exercise_property arg is either 'itemid', 'focusmuscle',
        or 'tags'. The result value is, respectively, mapped to the item ID,
        focus muscle, or all tags of the referenced Exercise item.

        :param results_type: The type of performance results: 'effort' for
            total effort sum, 'intensity' for maximum intensity, 'magnitude'
            for total magnitude sum
        :type results_type: str
        :param exercise_property: The Exercise property to which performance
            results are mapped: 'itemid' for Exercise item ID, 'focusmuscle'
            for focus muscle, 'tags' for tags
        :type exercise_property: str
        :return: Performance result per property of referenced Exercise item
        :rtype: dict
        """
        if not self.container():
            return {}
        performance = 0
        for session in self.container():
            if results_type in ["effort", "magnitude"]:
                performance += getattr(session, results_type)()
            elif results_type == "intensity":
                if session.intensity() > performance:
                    performance = session.intensity()
        ex_property = getattr(self, exercise_property)()
        keys = ex_property if exercise_property == "tags" else [ex_property]
        return {key: performance for key in keys}

    def unique_exercises(self):
        """
        Return a set with the referenced Exercise item ID.

        Overrides Gymbag.unique_exercises to return a set with the _itemid
        attribute, i.e. the only Exercise item referenced by this Activity.

        :return: A set with the referenced Exercise item ID
        :rtype: set
        """
        return {self._itemid}

    def unique_focusmuscles(self):
        """
        Return a set with the focus muscle of the referenced Exercise item.

        Overrides Gymbag.unique_focusmuscles to return a set with the focus
        muscle of the referenced Exercise item.

        :return: A set with the focus muscle of the referenced Exercise item
        :rtype: set
        """
        return {self.focusmuscle()}

    def unique_tags(self):
        """
        Return a set with the tags of the referenced Exercise item.

        Overrides Gymbag.unique_tags to return a set with the tags of the
        referenced Exercise item.

        :return: A set with the tags of the referenced Exercise item
        :rtype: set
        """
        return set(self.tags())

    def widgetize(self):
        """
        Update this object's text and children in the Build Viewer.

        Overrides BuildCenter.widgetize to update this object without calling
        widgetize on the Session objects in its container. Instead, the
        inherited setText method is called on each child so that its text
        is updated in the Build Viewer.
        """
        self.setText(0, str(self))
        self.takeChildren()
        for child in self.container():
            child.setText(0, str(child))
            self.addChild(child)

    def set_state(self, new_state):
        """
        Set the state of this Activity.

        The new_state arg is a list with the format:

            ['A', [session_state_list, ...], itemid_str]

        -where 'A' is the Activity class ID, session_state_list is the state of
        each Session to add to the container, and itemid_str is the referenced
        Exercise item ID. This method does not assign itemid_str to the _itemid
        attribute after instantiation, as it assumes that the same item ID has
        already been passed to the Activity constructor by the parent Workout
        that is executing its own set_state method. The GUI does not allow
        invalid new_state args to be passed to this method.

        :param new_state: Activity state with the format: ['A',
            [session state, ...], Exercise item ID]
        :type new_state: list
        """
        self.clear_container()
        for session_state in new_state[1]:
            session = Session(self._itemid)
            session.set_state(session_state)
            self.add_child(session)

    def state(self):
        """
        Return the state of this Activity.

        The state is returned with the format:

            ['A', [session_state_list, ...], itemid_str]

        -where 'A' is the Activity class ID, session_state_list is the state of
        each Session to add to the container, and itemid_str is the referenced
        Exercise item ID.

        :return: Activity state with the format: ['A', [session state, ...],
            Exercise item ID]
        :rtype: list
        """
        session_states = [session.state() for session in self.container()]
        return ["A", session_states, self._itemid]

    def template_state(self):
        """
        Return the template state of this Activity.

        The template state is returned with the format:

            ['A', [], itemid_str]

        -where 'A' is the Activity class ID and itemid_str is the referenced
        Exercise item ID. The list of child states is left empty. This forces
        the user to reenter new Sessions each time a Workout, Cycle, or Program
        template is used, as Session data will rarely remain the same for each
        instance of an Activity.

        :return: Activity template state with the format: ['A', [], Exercise
            item ID]
        :rtype: list
        """
        return ["A", [], self._itemid]


# noinspection PyMethodMayBeStatic
class Workout(Gymbag):
    """
    Class to store properties of a Workout build element.

    Workout inherits all attributes and methods from the Gymbag superclass. Its
    container stores Activity objects. Its _description attribute stores a
    description of the Workout, and its _period attribute stores its period
    'began' and 'ended' datetimes to capture its duration. The inherited
    method performance_results is overridden, and additional methods are
    implemented to set and return its _description and _period attributes,
    set and return its state, and return its template state.
    """

    def __init__(self):
        """
        Initialize a Workout object.

        Assigns placeholder text '(unnamed)' to the _description attribute and
        a list containing the default began and ended datetime.datetime objects
        to the _period attribute. The default began datetime is the current
        date at 00:00 (12:00 AM), and the default ended datetime is the current
        date at 01:00 (1:00 AM).
        """
        Gymbag.__init__(self)
        self._description = "(unnamed)"
        now = datetime.datetime.now()
        self._period = [
            datetime.datetime(now.year, now.month, now.day),
            datetime.datetime(now.year, now.month, now.day, 1)
        ]

    def __str__(self):
        """
        Return the informal string representation of this Workout.

        :return: The class ID 'W', the description, and the period components
            in the format:
            'W: <DESCRIPTION> -> <BEGAN(Y-m-d H:M)> to <ENDED(Y-m-d H:M)>
        :rtype: str
        """
        string = self._description + " -> " + str(self.began())[:-3]
        string += " to " + str(self.ended())[:-3]
        return "W: " + string

    def description(self):
        """
        Return the description.

        :return: The Workout description
        :rtype: str
        """
        return self._description

    def set_description(self, new_description):
        """
        Set the description.

        :param new_description: A new Workout description
        :type new_description:  str
        """
        self._description = new_description

    def period(self):
        """
        Return the period.

        :return: The Workout period list in the format: [began datetime,
            ended datetime]
        :rtype: list
        """
        return self._period

    def set_period(self, new_period):
        """
        Set the period.

        The new_period arg is a list with two datetime.datetime objects. The
        first is for when the Workout began, and the second is for when it
        ended. The GUI prevents invalid new_period args from begin passed to
        this method. The ended datetime must occur after the began datetime.

        :param new_period: A new period list in the format: [began datetime,
            ended datetime]
        :type new_period: list
        """
        self._period = new_period

    def began(self):
        """
        Return the period began datetime.

        :return: The datetime at which the Workout period began
        :rtype: datetime.datetime
        """
        return self._period[0]

    def ended(self):
        """
        Return the period ended datetime.

        :return: The datetime at which the Workout period ended
        :rtype: datetime.datetime
        """
        return self._period[1]

    def performance_results(self, results_type, exercise_property):
        """
        Return performance results per Exercise property for this Workout.

        Overrides Gymbag.performance_results to return a performance results
        dictionary with this Workout's period began datetime string as a key
        mapped to a performance results dict. This performance result dict has
        as its keys all properties, as specified by the exercise_property arg,
        of Exercise items referenced by constituent Sessions. Each key is
        mapped to the performance result value specified by the results_type
        arg. Result values are calculated for all constituent Sessions that
        reference Exercise items with that property value. The basic format is:

            {period began: {
                Exercise property: result value for all Sessions, ...}}

        The results_type arg is either 'effort', 'intensity', or 'magnitude'.
        Effort and magnitude results are calculated by summing the effort and
        magnitude values of all applicable constituent Sessions. The intensity
        result is calculated by finding the maximum intensity value among all
        applicable constituent Sessions. The exercise_property arg is either
        'itemid', 'focusmuscle', or 'tags'. Result values are, respectively,
        mapped to the item ID, focus muscle, or all tags of the Exercise item.

        :param results_type: The type of performance results: 'effort' for
            total effort sum, 'intensity' for maximum intensity, 'magnitude'
            for total magnitude sum
        :type results_type: str
        :param exercise_property: The Exercise property to which performance
            results are mapped: 'itemid' for Exercise item ID, 'focusmuscle'
            for focus muscle, 'tags' for tags
        :type exercise_property: str
        :return: Performance results per Exercise property per this Workout
        :rtype: dict
        """
        performance = {}
        began_string = self.began().strftime("%Y-%m-%d %H:%M")
        for activity in self.container():
            act_performance = activity.performance_results(
                results_type, exercise_property)
            if results_type in ["effort", "magnitude"]:
                performance = organs.summed_dicts(performance, act_performance)
            elif results_type == "intensity":
                performance = organs.maxed_dicts(performance, act_performance)
        return {began_string: performance} if performance else {}

    def set_state(self, new_state):
        """
        Set the state of this Workout.

        The new_state arg is a list with the format:

            ['W', [activity_state_list, ...], description_str,
             [began_str_or_None, ended_str_or_None]]

        -where 'W' is the Workout class ID, activity_state_list is the state of
        each Activity to add to the container, description_str is the
        description, began_str_or_None is a period began datetime string or
        None, and ended_str_or_None is a period ended datetime string or None.
        Both period values are None when the new_state arg is a Workout
        template state. In this case, the Workout period is set to the default
        list, with the current date at 00:00 (12:00 AM) as the began datetime,
        and the current date at 01:00 (1:00 AM) as the ended datetime. The GUI
        does not allow invalid new_state args to be passed to this method.

        :param new_state: Workout state with the format: ['W',
            [activity state, ...], description, [began datetime, ended
            datetime]]
        :type new_state: list
        """
        self.clear_container()
        for activity_state in new_state[1]:
            activity = Activity(activity_state[2])
            activity.set_state(activity_state)
            self.add_child(activity)
        self.set_description(new_state[2])
        if None in new_state[3]:
            now = datetime.datetime.now()
            new_period = [
                datetime.datetime(now.year, now.month, now.day),
                datetime.datetime(now.year, now.month, now.day, 1)
            ]
        else:
            new_period = [
                datetime.datetime.strptime(new_state[3][0], "%Y-%m-%d %H:%M"),
                datetime.datetime.strptime(new_state[3][1], "%Y-%m-%d %H:%M")
            ]
        self.set_period(new_period)

    def state(self):
        """
        Return the state of this Workout.

            ['W', [activity_state_list, ...], description_str,
             [began_str, ended_str]]

        -where 'W' is the Workout class ID, activity_state_list is the state of
        each Activity in the container, description_str is the description,
        began_str is the period began datetime, and ended_str is the period
        ended datetime. Period began and ended datetime strings are in the
        format 'Y-m-d H:M'.

        :return: Workout state with the format: ['W', [activity state, ...],
            description, [began datetime, ended datetime]]
        :rtype: list
        """
        activity_states = [activity.state() for activity in self.container()]
        period_strings = [
            self.began().strftime("%Y-%m-%d %H:%M"),
            self.ended().strftime("%Y-%m-%d %H:%M")
        ]
        return ["W", activity_states, self._description, period_strings]

    def template_state(self):
        """
        Return the template state of this Workout.

        The template state is returned with the format:

            ['W', [activity_template_state_list, ...], description_str,
             [None, None]]

        -where 'W' is the Workout class ID, activity_template_state_list is the
        template state of each Activity in the container, and description_str
        is the description. The period datetimes are both replaced with None.
        This forces the user to reenter a new period each time a Workout
        template is used, as the period will always be different. The GUI does
        not allow more than one Workout in a Program to have the same period
        began datetime.

        :return: Workout template state with the format: ['W',
            [activity template state, ...], description, [None, None]]
        :rtype: list
        """
        act_tem_states = [act.template_state() for act in self.container()]
        return ["W", act_tem_states, self._description, [None, None]]


class Cycle(Gymbag):
    """
    Class to store properties of a Cycle build element.

    Cycle inherits all attributes and methods from the Gymbag superclass. Its
    container stores Workout objects. Its _description attribute stores a
    description of the Cycle. Methods are implemented to set and return its
    _description attribute, return constituent Workout periods, set and return
    its state, and return its template state.
    """

    def __init__(self):
        """
        Initialize a Cycle object.

        Assigns placeholder text '(unnamed)' to the _description attribute.
        """
        Gymbag.__init__(self)
        self._description = "(unnamed)"

    def __str__(self):
        """
        Return the informal string representation of this Cycle.

        :return: The class ID 'C' and the description in the format:
            'C: <DESCRIPTION>'
        :rtype: str
        """
        return "C: " + self._description

    def description(self):
        """
        Return the description.

        :return: The Cycle description
        :rtype: str
        """
        return self._description

    def set_description(self, new_description):
        """
        Set the description.

        :param new_description: A new Cycle description
        :type new_description:  str
        """
        self._description = new_description

    def workout_periods(self):
        """
        Return a dictionary with all Workout periods.

        Returns a dictionary with child Workout period began datetime strings
        as keys, each mapped to its corresponding period ended datetime string.
        The basic format is:

            {period began: period ended, ...}

        :return: All constituent Workout periods
        :rtype: dict
        """
        all_workout_periods = {}
        for workout in self.container():
            began = workout.began().strftime("%Y-%m-%d %H:%M")
            ended = workout.ended().strftime("%Y-%m-%d %H:%M")
            all_workout_periods[began] = ended
        return all_workout_periods

    def set_state(self, new_state):
        """
        Set the state of this Cycle.

        The new_state arg is a list with the format:

            ['C', [workout_state_list, ...], description_str]

        -where 'C' is the Cycle class ID, workout_state_list is the state of
        each Workout to add to the container, and description_str is the
        description. The GUI does not allow invalid new_state args to be passed
        to this method.

        :param new_state: Cycle state with the format: ['C',
            [workout state, ...], description]
        :type new_state: list
        """
        self.clear_container()
        for workout_state in new_state[1]:
            workout = Workout()
            workout.set_state(workout_state)
            self.add_child(workout)
        self.set_description(new_state[2])

    def state(self):
        """
        Return the state of this Cycle.

        The state is returned with the format:

            ['C', [workout_state_list, ...], description_str]

        -where 'C' is the Cycle class ID, workout_state_list is the state of
        each Workout in the container, and description_str is the description.

        :return: Cycle state with the format: ['C', [workout state, ...],
            description]
        :rtype: list
        """
        workout_states = [workout.state() for workout in self.container()]
        return ["C", workout_states, self._description]

    def template_state(self):
        """
        Return the template state of this Cycle.

        The template state is returned with the format:

            ['C', [workout_template_state_list, ...], description_str]

        -where 'C' is the Cycle class ID, workout_template_state_list is the
        template state of each Workout in the container, and description_str is
        the description. Only the Cycle's children are affected when returning
        its template state rather than its actual state.

        :return: Cycle template state with the format: ['C',
            [workout template state, ...], description]
        :rtype: list
        """
        wor_tem_states = [wor.template_state() for wor in self.container()]
        return ["C", wor_tem_states, self._description]


class Program(Gymbag):
    """
    Class to store properties of a Program build element.

    Program inherits all attributes and methods from the Gymbag superclass. Its
    container stores Cycle objects. Its _description attribute stores a
    description of the Program, and its _start attribute stores the date on
    which it started. Methods are implemented to set and return its
    _description and _start attributes, return constituent Workout periods,
    set and return its state, and return its template state.
    """

    def __init__(self):
        """
        Initialize a Program object.

        Assign placeholder text '(unnamed)' to the _description attribute and
        the default date datetime.datetime.now().date() to the _start
        attribute.
        """
        Gymbag.__init__(self)
        self._description = "(unnamed)"
        self._start = datetime.datetime.now().date()

    def __str__(self):
        """
        Return the informal string representation of this Program.

        :return: The class ID 'P', the description, and the start date in the
            format: 'P: <DESCRIPTION> -> <START(Y-m-d)>'
        :rtype: str
        """
        return "P: " + self._description + " -> " + str(self._start)

    def description(self):
        """
        Return the description.

        :return: The Program description
        :rtype: str
        """
        return self._description

    def set_description(self, new_description):
        """
        Set the description.

        :param new_description: A new Program description
        :type new_description: str
        """
        self._description = new_description

    def start(self):
        """
        Return the start.

        :return: The Program start date
        :rtype: datetime.date
        """
        return self._start

    def set_start(self, new_start):
        """
        Set the start.

        The GUI prevents invalid new_start args from being passed to this
        method.

        :param new_start: A new Program start date
        :type new_start: datetime.date
        """
        self._start = new_start

    def workout_periods(self):
        """
        Return a dictionary with all Workout periods.

        Returns a dictionary with constituent Workout period began datetime
        strings as keys, each mapped to its corresponding period ended
        datetime string. The basic format is:

            {period began: period ended, ...}

        :return: All constituent Workout periods
        :rtype: dict
        """
        all_workout_periods = {}
        for cycle in self.container():
            all_workout_periods.update(cycle.workout_periods())
        return all_workout_periods

    def set_state(self, new_state):
        """
        Set the state of this Program.

        The new_state arg is a list with the format:

            ['P', [cycle_state_list, ...], description_str, start_str_or_None]

        -where 'P' is the Program class ID, cycle_state_list is the state of
        each Cycle to add to the container, description_str is the description,
        and start_str_or_None is the start as a string with the date format
        '%Y-%m-%d' or, if the new_state arg is a template state, None. If the
        date is None, the default datetime.datetime.now().date() value is
        assigned to the _start attribute. The GUI does not allow invalid
        new_state args to be passed to this method.

        :param new_state: Program state with the format: ['P',
            [cycle state, ...], description, start]
        :type new_state: list
        """
        self.clear_container()
        for cycle_state in new_state[1]:
            cycle = Cycle()
            cycle.set_state(cycle_state)
            self.add_child(cycle)
        self.set_description(new_state[2])
        if new_state[3] is None:
            new_start = datetime.datetime.now().date()
        else:
            new_start = datetime.datetime.strptime(
                new_state[3], "%Y-%m-%d").date()
        self.set_start(new_start)

    def state(self):
        """
        Return the state of this Program.

        The state is returned with the format:

            ['P', [cycle_state_list, ...], description_str, start_str]

        -where 'P' is the Program class ID, cycle_state_list is the state of
        each Cycle in the container, description_str is the description, and
        start_str is the start as a string with the date format '%Y-%m-%d'.

        :return: Program state with the format: ['P', [cycle state, ...],
            description, start]
        :rtype: list
        """
        cycle_states = [cycle.state() for cycle in self.container()]
        return ["P", cycle_states, self._description,
                self._start.strftime("%Y-%m-%d")]

    def template_state(self):
        """
        Return the template state of this Program.

        The template state is returned with the format:

            ['P', [cycle_template_state_list, ...], description_str, None]

        -where 'P' is the Program class ID, cycle_template_state_list is the
        template state of each Cycle in the container, and description_str is
        the description. The start string is replaced with None, which
        indicates to the set_state method that the _start attribute is to be
        assigned a datetime.datetime.now().date() object, the default date
        value when a Program is constructed. Saving Program templates with None
        instead of start dates forces the user to reenter the start property
        each time a Program template is used.

        :return: Program template state with the format: ['P',
            [cycle template state, ...], description, None]
        :rtype: list
        """
        cyc_tem_states = [cyc.template_state() for cyc in self.container()]
        return ["P", cyc_tem_states, self._description, None]


# -----------------------------------------------------------------------------
# Reference Class

class Reference:
    """
    Class to store properties of a Food or Exercise reference item.

    Each Reference object has an _info attribute, which is a dict that can be
    modified to fit the purpose of a new or existing Food or Exercise reference
    item. This attribute's values can be accessed and modified with instance
    methods. Reference provides a simple, consistent, and explicit way of
    handling reference item data. The property names--keys in the _info dict--
    and corresponding values for each reference type are:

    --Food Reference Item--
        'reftype': 'Food'
        'isdatacapsule': bool indicating if loaded from a data capsule
        'isfavorite': bool indicating if item is a favorite
        'itemid': reference item ID string
        'description': description string
        'groupid': food group ID string
        'unitsequences': unit sequences list
        'nutrientcontent': nutrient content dictionary
    --Exercise Reference Item--
        'reftype': 'Exercise'
        'isdatacapsule': bool indicating if loaded from a data capsule
        'isfavorite': bool indicating if item is a favorite
        'itemid': reference item ID string
        'description': description string
        'focusmuscle': focus muscle string
        'units': performance metric units list
        'tags': info tags list of strings
    """

    def __init__(self, ref_type, item_id=None, user=None, data_capsule=None):
        """
        Initialize a Reference object.

        Assigns a dict with 'reftype' mapped to ref_type arg and 'isfavorite'
        mapped to 'isfavorite' (the default favorite value) to the _info
        attribute. If ref_type='Food', all Food properties are added as keys
        to the info dictionary and each is assigned a null value with the same
        type as a valid value of that property. The same procedure is executed
        but for Exercise properties if ref_type='Exercise'.

        A current Food or Exercise reference item ID can be assigned to the
        item_id parameter to update this object's properties with those of the
        existing reference item. If the item_id arg is an existing item ID, the
        user's User object must be assigned to the user parameter to afford
        access to the applicable reference dictionaries and favorites list.

        A data capsule can also be passed to this constructor, assigned to the
        data_capsule parameter. If data_capsule is assigned a data capsule
        list, its properties are mapped to the applicable property name keys
        in the _info dictionary. Data capsule elements are thoroughly validated
        before this object's info attribute is updated. If invalid data is
        found, an exception is raised, to be handled by the function which
        instantiated this object.

        :param ref_type: 'Food' or 'Exercise' reference item type
        :type ref_type: str
        :param item_id: The item ID of an existing Food or Exercise
        :type item_id: str
        :param user: The user's User object
        :type user: User
        :param data_capsule: A data capsule with reference item properties
        :type data_capsule: list
        """
        # Basic info properties.
        self._info = {
            "reftype": ref_type, "isdatacapsule": False, "isfavorite": False}
        # Remaining properties with null values.
        if ref_type == "Food":
            self._info.update({
                "itemid": "", "description": "", "groupid": "",
                "unitsequences": [], "nutrientcontent": {}})
        elif ref_type == "Exercise":
            self._info.update({
                "itemid": "", "description": "", "focusmuscle": "",
                "units": [], "tags": []})
        # Existing Food reference item property value assignments.
        if item_id is not None and user is not None:
            self.set_property("itemid", item_id)
            if item_id in user.settings()["favorites"][ref_type[0]]:
                self.set_property("isfavorite", True)
            if ref_type == "Food":
                details = user.food_details()[item_id]
                nutrients = user.food_nutrients()[item_id]
                self.update_info({
                    "description": details[0], "groupid": details[1],
                    "unitsequences": details[2], "nutrientcontent": nutrients})
            else:
                details = user.exercise_details()[item_id]
                self.update_info({
                    "description": details[0], "focusmuscle": details[1],
                    "units": details[2], "tags": details[3]})
        # Data capsule property value assignments.
        elif data_capsule is not None:
            self.set_property("isdatacapsule", True)
            # Check data capsule element types.
            index_types = {
                1: (str, unicode), 2: (str, unicode), 3: list,
                4: dict if ref_type == "Food" else list}
            for index in index_types:
                if not isinstance(data_capsule[index], index_types[index]):
                    raise TypeError
            if ref_type == "Food":
                # Check elements for valid data.
                if str(data_capsule[2]) not in dna.FOOD_GROUPS:
                    raise ValueError
                for sequence in data_capsule[3]:
                    if not isinstance(sequence, list):
                        raise TypeError
                    if len(sequence) != 3:
                        raise IndexError
                    float(sequence[0])
                    if not isinstance(sequence[1], (str, unicode)):
                        raise TypeError
                    float(sequence[2])
                for nutrientid in data_capsule[4]:
                    if nutrientid not in dna.NUTRIENTS:
                        raise KeyError
                    float(data_capsule[4][nutrientid])
                # Update info after checks are passed.
                self.update_info({
                    "description": data_capsule[1], "groupid": data_capsule[2],
                    "unitsequences": data_capsule[3],
                    "nutrientcontent": data_capsule[4]})
            else:
                # Check elements for valid data.
                if str(data_capsule[2]) not in dna.MUSCLE:
                    raise ValueError
                if len(data_capsule[3]) != 2:
                    raise IndexError
                for unit in data_capsule[3]:
                    if not isinstance(unit, (str, unicode)):
                        raise TypeError
                for tag in data_capsule[4]:
                    if not isinstance(tag, (str, unicode)):
                        raise TypeError
                # Update info after checks are passed
                self.update_info({
                    "description": data_capsule[1],
                    "focusmuscle": data_capsule[2], "units": data_capsule[3],
                    "tags": data_capsule[4]})

    def info(self, property_name=None):
        """
        Return the value of the specified property or all reference info.

        Returns the value of the property specified by the property_name arg
        and found in the _info attribute. If property_name=None, the _info
        dictionary is returned. The GUI prevents invalid property_name args
        from being passed to this method.

        :param property_name: The name of a Food or Exercise property found
            in the _info attribute, or None
        :type property_name: str, None
        :return: The value of a property in the _info attribute, or the entire
            _info attribute
        :rtype: dict, list, str
        """
        if property_name is None:
            return self._info
        return self._info[property_name]

    def update_info(self, updated_info):
        """
        Update the reference item's properties with new values.

        Calls the dict.update method on the _info attribute and passes it the
        updated_info arg. The GUI prevents invalid updated_info args from being
        passed to this method.

        :param updated_info: A dictionary with Food or Exercise property names
            mapped to corresponding property values
        :type updated_info: dict
        """
        self._info.update(updated_info)

    def set_property(self, property_name, new_value):
        """
        Set the value of a specific property.

        Maps the property_name arg key in the _info attribute to the new_value
        arg. The GUI prevents invalid property_name and new_value args from
        being passed to this method.

        :param property_name: The name of a Food or Exercise property found
            in the _info attribute
        :type property_name: str
        :param new_value: The value of the specified property
        :type new_value: dict, list, str
        """
        self._info[property_name] = new_value

    def details(self):
        """
        Return the reference item's details.

        Returns a details list that can be used by the add_reference method of
        a User object. The property values are returned in a structured format
        for each reference item type:

        --Food Details--
            [description, groupid, [unitsequences]]
        --Exercise Details--
            [description, focusmuscle, [units], [tags]]

        :return: Food or Exercise reference item details
        :rtype: dict
        """
        if self._info["reftype"] == "Food":
            details = [
                self._info["description"], self._info["groupid"],
                self._info["unitsequences"]]
        else:
            details = [
                self._info["description"], self._info["focusmuscle"],
                self._info["units"], self._info["tags"]]
        return details

    def datacapsule(self):
        """
        Return the reference item's data capsule.

        Returns a list that can be saved in a JSON formatted file as a 'data
        capsule'. A data capsule can be loaded into Reference objects to set
        all property values. The data capsule is returned in a structured
        format for each reference item type:

        --Food Data Capsule--
            ['Food', description, groupid, [unitsequences], {nutrientcontent}]
        --Exercise Data Capsule--
            ['Exercise', description, focusmuscle, [units], [tags]]

        :return: A list with Food or Exercise property values that can be saved
            as a JSON formatted file
        :rtype: list
        """
        reftype = self._info["reftype"]
        capsule = [reftype]
        if reftype == "Food":
            capsule += [
                self._info["description"], self._info["groupid"],
                self._info["unitsequences"], self._info["nutrientcontent"]]
        else:
            capsule += [
                self._info["description"], self._info["focusmuscle"],
                self._info["units"], self._info["tags"]]
        return capsule

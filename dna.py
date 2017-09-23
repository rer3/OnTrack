#!/usr/bin/env python2.7
"""
This module contains application constants.
----------
Constants used by this application have been collected in one location for
convenient modification. Source data URLs and Exercise details are used to
construct pre-launch data sets, while all remaining constants are used by the
application during runtime. This module also contains the __author__,
__project__, and __version__ attributes for this application.
----------
Source URLs: URL strings for all data sets provided by the USDA National
Nutrient Database for Standard Reference (release 28). These data sets were
parsed and reconfigured for use by this application.
    URL_USDA_NNDSR: URL for NNDSR home page
    URL_USDA_BASE: base URL for source data
    URL_FOOD_DES: URL for food descriptions file
    URL_WEIGHT: URL for food weights file
    URL_NUT_DATA: URL for food nutrient data file

Initial Exercise Details: source data for initial ExerciseDetails.json
reference master file.
    EXERCISES: tuple of tuples with Exercise reference item details

Supplementary Food Reference Data: reference data for food groups and food
nutrients from the USDA NNDSR.
    FOOD_GROUPS: dict with food group IDs mapped to food group names
    AMINOS: dict with nutrient IDs mapped to tuples of amino acid properties
    CARBS: dict with nutrient IDs mapped to tuples of carbohydrate properties
    LIPIDS: dict with nutrient IDs mapped to tuples of lipid properties
    MACROS: dict with nutrient IDs mapped to tuples of macronutrient properties
    MINERALS: dict with nutrient IDs mapped to tuples of mineral properties
    VITAMINS: dict with nutrient IDs mapped to tuples of vitamin properties
    NUTRIENTS: dict merged from AMINOS, CARBS, LIPIDS, MACROS, MINERALS, and
        VITAMINS dicts
    GUI_NUTRIENTS: tuple with default nutrient IDs and their order
    FDA_RDV: dict with nutrient IDs mapped to tuples of recommended values

Supplementary Exercise Reference Data: reference data for exercise focus
muscles. The focus muscles presented to the user are 18 common specific muscle
groups, 3 general muscle groups, and 1 'NA' for exercises that are not
applicable to focus muscle identification.
    MUSCLES: tuple with default focus muscle strings and their order (A-Z)

File Names: reference source dir name and all reference and user file names.
    REF_DIR: string name of reference directory
    REF_FILES: dict with file IDs mapped to reference filename strings
    USER_FILES: dict with file IDs mapped to user filename strings
    ALL_FILES: dict with merged dicts REF_FILES and USER_FILES

Build Elements: build element class properties such as name and which other
build elements may be added to them as children.
    NUTRITION_BUILD_ELEMENTS: dict with nutrition class IDs mapped to tuples
        of build element properties
    FITNESS_BUILD_ELEMENTS: dict with fitness class IDs mapped to tuples of
        build element properties
    BUILD_ELEMENTS: dict merged from NUTRITION_BUILD_ELEMENTS and
        FITNESS_BUILD_ELEMENTS dicts

Style Sheets: CSS strings used by the GUI to modify its components. Some style
sheets are reused by multiple GUI components, while others are uniquely used.
    STYLE_ACTION: action QToolButton
    STYLE_BUILDMANAGERTAG: Build Manager tag QLabel
    STYLE_COMBOBOX: eye-catching QComboBox
    STYLE_COPYTAG: Copied Item tag QLabel
    STYLE_GUIDETAG: Guide tag QLabel
    STYLE_INVENTORYMANAGERTAG: Inventory Manager tag QLabel
    STYLE_LOGINFRAME: Login Menu QFrame
    STYLE_MAINFRAME: Main Menu QFrame
    STYLE_HOMEMESSAGE: Home Message QLabel
    STYLE_PROFILEFRAME: Profile QFrame
    STYLE_PROFILETAG: Profile tag QLabel
    STYLE_SELECTION: selection QToolButton
    STYLE_STICKER: sticker QLabel style
    STYLE_TABLE: QTableWidget (Unused by the current application version)
    STYLE_TIPBOX: tip box QPlainTextEdit
    STYLE_TITLETAG: title tag QLabel
    STYLE_TREE: Build Viewer QTreeWidget

Common Icons: commonly used icons.
    ICONS: dict with common icon IDs mapped to their icon name strings found
        in the resource data module 'album'

Guide Text: text for the Guide Boxes on the Guide Page. Guide text is separated
into two sections: instructions and glossary.
    GUIDE_TEXTA: text for Guide Box A with directions for using OnTrack
    GUIDE_TEXTB: text for Guide Box B with terms and definitions
"""

__author__ = 'R3'
__project__ = 'OnTrack'
__version__ = '1.0'


# -----------------------------------------------------------------------------
# Source URLs -----------------------------------------------------------------

URL_USDA_NNDSR = "".join([
    "https://www.ars.usda.gov/northeast-area/beltsville-md/"
    "beltsville-human-nutrition-research-center/nutrient-data-laboratory/"
    "docs/usda-national-nutrient-database-for-standard-reference/"])
URL_USDA_BASE = \
    "https://www.ars.usda.gov/ARSUserFiles/80400525/Data/SR/SR28/asc/"
URL_FOOD_DES = URL_USDA_BASE + "FOOD_DES.txt"
URL_WEIGHT = URL_USDA_BASE + "WEIGHT.txt"
URL_NUT_DATA = URL_USDA_BASE + "NUT_DATA.txt"

# -----------------------------------------------------------------------------
# Initial Exercise Details ----------------------------------------------------

EXERCISES = (
    ("Ab Rollout (Barbell)", "Abdominals", ["rep", "NA"], []),
    ("Bench Press (Close Grip Barbell)", "Chest", ["rep", "lb"], []),
    ("Bench Press (Close Grip Dumbbell)", "Chest", ["rep", "lb"], []),
    ("Bench Press (Decline Barbell)", "Chest", ["rep", "lb"], []),
    ("Bench Press (Decline Dumbbell)", "Chest", ["rep", "lb"], []),
    ("Bench Press (Incline Barbell)", "Chest", ["rep", "lb"], []),
    ("Bench Press (Incline Dumbbell)", "Chest", ["rep", "lb"], []),
    ("Bench Press (Machine)", "Chest", ["rep", "lb"], []),
    ("Bench Press (Medium Grip Barbell)", "Chest", ["rep", "lb"], []),
    ("Bench Press (Medium Grip Dumbbell)", "Chest", ["rep", "lb"], []),
    ("Bench Press (Wide Grip Barbell)", "Chest", ["rep", "lb"], []),
    ("Bench Press (Wide Grip Dumbbell)", "Chest", ["rep", "lb"], []),
    ("Bicep Curl (Barbell)", "Biceps", ["rep", "lb"], []),
    ("Bicep Curl (Cable)", "Biceps", ["rep", "lb"], []),
    ("Bicep Curl (Close Grip Barbell)", "Biceps", ["rep", "lb"], []),
    ("Bicep Curl (Close Grip EZ-Curl Bar)", "Biceps", ["rep", "lb"], []),
    ("Bicep Curl (Concentration Dumbbell)", "Biceps", ["rep", "lb"], []),
    ("Bicep Curl (Dumbbell)", "Biceps", ["rep", "lb"], []),
    ("Bicep Curl (EZ-Curl Bar)", "Biceps", ["rep", "lb"], []),
    ("Bicep Curl (Hammer Alternating)", "Biceps", ["rep", "lb"], []),
    ("Bicep Curl (Hammer Two Arm)", "Biceps", ["rep", "lb"], []),
    ("Bicep Curl (Incline Dumbbell)", "Biceps", ["rep", "lb"], []),
    ("Bicep Curl (Preacher Barbell)", "Biceps", ["rep", "lb"], []),
    ("Bicep Curl (Preacher EZ-Curl Bar)", "Biceps", ["rep", "lb"], []),
    ("Bicep Curl (Preacher Machine)", "Biceps", ["rep", "lb"], []),
    ("Bicep Curl (Reverse Grip Barbell)", "Biceps", ["rep", "lb"], []),
    ("Bicep Curl (Reverse Grip EZ-Curl Bar)", "Biceps", ["rep", "lb"], []),
    ("Bicep Curl (Zottman)", "Biceps", ["rep", "lb"], []),
    ("Bicycling", "Quadriceps", ["miles", "mph"], []),
    ("Bicycling", "Quadriceps", ["min", "mph"], []),
    ("Bicycling (Stationary Machine)", "Quadriceps", ["miles", "mph"], []),
    ("Bicycling (Stationary Machine)", "Quadriceps", ["min", "mph"], []),
    ("Calf Raise (Leg Press Machine)", "Calves", ["rep", "lb"], []),
    ("Calf Raise (Seated Machine)", "Calves", ["rep", "lb"], []),
    ("Calf Raise (Standing Barbell)", "Calves", ["rep", "lb"], []),
    ("Calf Raise (Standing Dumbbell)", "Calves", ["rep", "lb"], []),
    ("Chin Up", "Lats", ["rep", "lb"], []),
    ("Chin Up (Assist Machine)", "Lats", ["rep", "lb"], []),
    ("Crossover (Cable)", "Chest", ["rep", "lb"], []),
    ("Crossover (Low Cable)", "Chest", ["rep", "lb"], []),
    ("Crunch", "Abdominals", ["rep", "NA"], []),
    ("Crunch (Cable)", "Abdominals", ["rep", "lb"], []),
    ("Crunch (Cable Oblique)", "Obliques", ["rep", "lb"], []),
    ("Crunch (Decline)", "Abdominals", ["rep", "NA"], []),
    ("Crunch (Decline Oblique)", "Obliques", ["rep", "NA"], []),
    ("Crunch (Oblique)", "Obliques", ["rep", "NA"], []),
    ("Deadlift (Barbell)", "Hamstrings", ["rep", "lb"], []),
    ("Deadlift (Dumbbell)", "Hamstrings", ["rep", "lb"], []),
    ("Deadlift (Romanian Barbell)", "Hamstrings", ["rep", "lb"], []),
    ("Deadlift (Romanian Dumbbell)", "Hamstrings", ["rep", "lb"], []),
    ("Deadlift (Stiff Legged Barbell)", "Hamstrings", ["rep", "lb"], []),
    ("Deadlift (Stiff Legged Dumbbell)", "Hamstrings", ["rep", "lb"], []),
    ("Dip (Assist Machine)", "Triceps", ["rep", "lb"], []),
    ("Dip (Bench)", "Triceps", ["rep", "lb"], []),
    ("Elliptical (Machine)", "Quadriceps", ["miles", "mph"], []),
    ("Elliptical (Machine)", "Quadriceps", ["min", "mph"], []),
    ("Face Pull", "Shoulders", ["rep", "lb"], []),
    ("Face Pull (Low Pulley Row to Neck)", "Shoulders", ["rep", "lb"], []),
    ("Finger Curl", "Forearms", ["rep", "lb"], []),
    ("Flutter Kick", "Glutes", ["rep", "NA"], []),
    ("Fly (Cable)", "Chest", ["rep", "lb"], []),
    ("Fly (Dumbbell)", "Chest", ["rep", "lb"], []),
    ("Fly (Incline Dumbbell)", "Chest", ["rep", "lb"], []),
    ("Fly (Machine)", "Chest", ["rep", "lb"], []),
    ("Fly (Reverse Dumbbell)", "Shoulders", ["rep", "lb"], []),
    ("Fly (Reverse Machine)", "Shoulders", ["rep", "lb"], []),
    ("Front Raise (Barbell)", "Shoulders", ["rep", "lb"], []),
    ("Front Raise (Cable)", "Shoulders", ["rep", "lb"], []),
    ("Front Raise (Dumbbell)", "Shoulders", ["rep", "lb"], []),
    ("Glute Bridge (Hip Thrust)", "Glutes", ["rep", "lb"], []),
    ("Glute Kickback", "Glutes", ["rep", "NA"], []),
    ("Glute Kickback (Cable)", "Glutes", ["rep", "lb"], []),
    ("Glute Kickback (Machine)", "Glutes", ["rep", "lb"], []),
    ("Good Morning", "Hamstrings", ["rep", "lb"], []),
    ("Hanging Leg Raise", "Abdominals", ["rep", "lb"], []),
    ("Hanging Leg Raise (Oblique)", "Obliques", ["rep", "lb"], []),
    ("Hip Raise", "Abdominals", ["rep", "NA"], []),
    ("Jump Rope", "Quadriceps", ["min", "NA"], []),
    ("Jump Rope", "Quadriceps", ["rep", "NA"], []),
    ("Jumping Jack", "Quadriceps", ["rep", "NA"], []),
    ("Leg Curl (Lying Machine)", "Hamstrings", ["rep", "lb"], []),
    ("Leg Curl (Seated Machine)", "Hamstrings", ["rep", "lb"], []),
    ("Leg Extension (Machine)", "Quadriceps", ["rep", "lb"], []),
    ("Leg Press (Machine)", "Quadriceps", ["rep", "lb"], []),
    ("Lunge", "Quadriceps", ["rep", "NA"], []),
    ("Lunge (Barbell)", "Quadriceps", ["rep", "lb"], []),
    ("Lunge (Dumbbell)", "Quadriceps", ["rep", "lb"], []),
    ("Lunge (EZ-Curl Bar)", "Quadriceps", ["rep", "lb"], []),
    ("Lunge (Reverse)", "Quadriceps", ["rep", "NA"], []),
    ("Lunge (Reverse Barbell)", "Quadriceps", ["rep", "lb"], []),
    ("Lunge (Reverse Dumbbell)", "Quadriceps", ["rep", "lb"], []),
    ("Lunge (Reverse EZ-Curl Bar)", "Quadriceps", ["rep", "lb"], []),
    ("Lunge (Side)", "Quadriceps", ["rep", "NA"], []),
    ("Lunge (Walking Barbell)", "Quadriceps", ["rep", "lb"], []),
    ("Lunge (Walking Dumbbell)", "Quadriceps", ["rep", "lb"], []),
    ("Lunge (Walking EZ-Curl Bar)", "Quadriceps", ["rep", "lb"], []),
    ("Plank", "Abdominals", ["min", "NA"], []),
    ("Pull Up", "Lats", ["rep", "lb"], []),
    ("Pull Up (Assist Machine)", "Lats", ["rep", "lb"], []),
    ("Pulldown (Underhand Grip Cable)", "Lats", ["rep", "lb"], []),
    ("Pulldown (Medium Grip Cable)", "Lats", ["rep", "lb"], []),
    ("Pulldown (Wide Grip Cable)", "Lats", ["rep", "lb"], []),
    ("Push Up", "Chest", ["rep", "NA"], []),
    ("Row (Bent Over Barbell)", "Middle Back", ["rep", "lb"], []),
    ("Row (Close Grip T-Bar)", "Lats", ["rep", "lb"], []),
    ("Row (One Arm Dumbbell)", "Middle Back", ["rep", "lb"], []),
    ("Row (One Arm Machine)", "Middle Back", ["rep", "lb"], []),
    ("Row (Pendlay)", "Middle Back", ["rep", "lb"], []),
    ("Row (Seated Cable)", "Middle Back", ["rep", "lb"], []),
    ("Row (Upright Barbell)", "Shoulders", ["rep", "lb"], []),
    ("Row (Upright Dumbbell)", "Shoulders", ["rep", "lb"], []),
    ("Row (Wide Grip T-Bar)", "Middle Back", ["rep", "lb"], []),
    ("Running (Road)", "Quadriceps", ["miles", "mph"], []),
    ("Running (Road)", "Quadriceps", ["min", "mph"], []),
    ("Running (Trail)", "Quadriceps", ["miles", "mph"], []),
    ("Running (Trail)", "Quadriceps", ["min", "mph"], []),
    ("Running (Treadmill)", "Quadriceps", ["miles", "mph"], []),
    ("Running (Treadmill)", "Quadriceps", ["min", "mph"], []),
    ("Scissor Kick", "Abdominals", ["rep", "NA"], []),
    ("Shoulder Press (Machine)", "Shoulders", ["rep", "lb"], []),
    ("Shoulder Press (Seated Barbell)", "Shoulders", ["rep", "lb"], []),
    ("Shoulder Press (Seated Dumbbell)", "Shoulders", ["rep", "lb"], []),
    ("Shoulder Press (Standing Barbell)", "Shoulders", ["rep", "lb"], []),
    ("Shoulder Press (Standing Dumbbell)", "Shoulders", ["rep", "lb"], []),
    ("Shrug (Barbell)", "Traps", ["rep", "lb"], []),
    ("Shrug (Dumbbell)", "Traps", ["rep", "lb"], []),
    ("Side Bend (Cable)", "Obliques", ["rep", "lb"], []),
    ("Side Bend (Dumbbell)", "Obliques", ["rep", "lb"], []),
    ("Side Lateral Raise", "Shoulders", ["rep", "lb"], []),
    ("Sit Up", "Abdominals", ["rep", "NA"], []),
    ("Sled Push", "Quadriceps", ["ft", "lb"], []),
    ("Squat (Barbell)", "Quadriceps", ["rep", "lb"], []),
    ("Squat (Dumbbell)", "Quadriceps", ["rep", "lb"], []),
    ("Squat (Front Barbell)", "Quadriceps", ["rep", "lb"], []),
    ("Squat (Front Dumbbell)", "Quadriceps", ["rep", "lb"], []),
    ("Squat (Goblet)", "Quadriceps", ["rep", "lb"], []),
    ("Squat (Machine)", "Quadriceps", ["rep", "lb"], []),
    ("Squat (One Legged Barbell)", "Quadriceps", ["rep", "lb"], []),
    ("Squat (One Legged Dumbbell)", "Quadriceps", ["rep", "lb"], []),
    ("Step Up", "Quadriceps", ["rep", "NA"], []),
    ("Step Up (Barbell)", "Quadriceps", ["rep", "lb"], []),
    ("Step Up (Dumbbell)", "Quadriceps", ["rep", "lb"], []),
    ("Step Up (EZ-Curl Bar)", "Quadriceps", ["rep", "lb"], []),
    ("Straight Arm Pulldown (Cable)", "Lats", ["rep", "lb"], []),
    ("Tricep Extension (Lying Barbell)", "Triceps", ["rep", "lb"], []),
    ("Tricep Extension (Lying Cable)", "Triceps", ["rep", "lb"], []),
    ("Tricep Extension (Lying Dumbbell)", "Triceps", ["rep", "lb"], []),
    ("Tricep Extension (Lying EZ-Curl Bar)", "Triceps", ["rep", "lb"], []),
    ("Tricep Extension (Seated Cable)", "Triceps", ["rep", "lb"], []),
    ("Tricep Extension (Seated Dumbbell)", "Triceps", ["rep", "lb"], []),
    ("Tricep Extension (Standing Cable)", "Triceps", ["rep", "lb"], []),
    ("Tricep Extension (Standing Dumbbell)", "Triceps", ["rep", "lb"], []),
    ("Tricep Kickback (Dumbbell)", "Triceps", ["rep", "lb"], []),
    ("Tricep Pushdown (Cable Bar)", "Triceps", ["rep", "lb"], []),
    ("Tricep Pushdown (Cable Rope)", "Triceps", ["rep", "lb"], []),
    ("Wood Chop (Standing Cable)", "Obliques", ["rep", "lb"], []),
    ("Wrist Curl (Palm Down Seated Barbell)", "Forearms", ["rep", "lb"], []),
    ("Wrist Curl (Palm Down Seated Dumbbell)", "Forearms", ["rep", "lb"], []),
    ("Wrist Curl (Palm Up Seated Barbell)", "Forearms", ["rep", "lb"], []),
    ("Wrist Curl (Palm Up Seated Dumbbell)", "Forearms", ["rep", "lb"], []),
)

# -----------------------------------------------------------------------------
# Supplementary Food Reference Data -------------------------------------------

FOOD_GROUPS = {
    "0100": "Dairy and Egg Products",
    "0200": "Spices and Herbs",
    "0300": "Baby Foods",
    "0400": "Fats and Oils",
    "0500": "Poultry Products",
    "0600": "Soups, Sauces, and Gravies",
    "0700": "Sausages and Luncheon Meats",
    "0800": "Breakfast Cereals",
    "0900": "Fruits and Fruit Juices",
    "1000": "Pork Products",
    "1100": "Vegetables and Vegetable Products",
    "1200": "Nut and Seed Products",
    "1300": "Beef Products",
    "1400": "Beverages",
    "1500": "Finfish and Shellfish Products",
    "1600": "Legumes and Legume Products",
    "1700": "Lamb, Veal, and Game Products",
    "1800": "Baked Products",
    "1900": "Sweets",
    "2000": "Cereal Grains and Pasta",
    "2100": "Fast Foods",
    "2200": "Meals, Entrees, and Side Dishes",
    "2500": "Snacks",
    "3500": "American Indian/Alaska Native Foods",
    "3600": "Restaurant Foods",
}

AMINOS = {
    "501": ("Tryptophan", "TRP", "g"),
    "502": ("Threonine", "THR", "g"),
    "503": ("Isoleucine", "ILE", "g"),
    "504": ("Leucine", "LEU", "g"),
    "505": ("Lysine", "LYS", "g"),
    "506": ("Methionine", "MET", "g"),
    "507": ("Cystine", "CYS", "g"),
    "508": ("Phenylalanine", "PHE", "g"),
    "509": ("Tyrosine", "TYR", "g"),
    "510": ("Valine", "VAL", "g"),
    "511": ("Arginine", "ARG", "g"),
    "512": ("Histidine", "HIS", "g"),
    "513": ("Alanine", "ALA", "g"),
    "514": ("Aspartic Acid", "ASP", "g"),
    "515": ("Glutamic Acid", "GLX", "g"),
    "516": ("Glycine", "GLY", "g"),
    "517": ("Proline", "PRO", "g"),
    "518": ("Serine", "SER", "g")
}

CARBS = {
    "209": ("Starch", "Starch", "g"),
    "210": ("Sucrose", "Sucrose", "g"),
    "211": ("Glucose", "Glucose", "g"),
    "212": ("Fructose", "Fructos", "g"),
    "213": ("Lactose", "Lactose", "g"),
    "214": ("Maltose", "Maltose", "g"),
    "262": ("Caffeine", "Caffein", "mg"),
    "269": ("Sugars", "Sugar", "g"),
    "287": ("Galactose", "Galacto", "g"),
    "291": ("Fiber", "Fiber", "g")
}

LIPIDS = {
    "601": ("Cholesterol", "Cholest", "mg"),
    "605": ("Trans Fatty Acids", "TranFat", "g"),
    "606": ("Saturated Fatty Acids", "SatFat", "g"),
    "621": ("DHA (Omega-3 Fatty Acid)", "DHA", "g"),
    "629": ("EPA (Omega-3 Fatty Acid)", "EPA", "g"),
    "631": ("DPA (Omega-3 Fatty Acid)", "DPA", "g"),
    "645": ("Monounsaturated Fatty Acids", "MonoFat", "g"),
    "646": ("Polyunsaturated Fatty Acids", "PolyFat", "g"),
    "851": ("ALA (Omega-3 Fatty Acid)", "ALA", "g")
}

MACROS = {
    "203": ("Protein", "Protein", "g"),
    "204": ("Fat", "Fat", "g"),
    "205": ("Carbohydrate", "Carb", "g"),
    "208": ("Energy", "Energy", "kcal")
}

MINERALS = {
    "301": ("Calcium", "Calcium", "mg"),
    "303": ("Iron", "Iron", "mg"),
    "304": ("Magnesium", "Magnes", "mg"),
    "305": ("Phosphorus", "Phosph", "mg"),
    "306": ("Potassium", "Potas", "mg"),
    "307": ("Sodium", "Sodium", "mg"),
    "309": ("Zinc", "Zinc", "mg"),
    "312": ("Copper", "Copper", "mg"),
    "313": ("Fluoride", "Fluor", "mcg"),
    "315": ("Manganese", "Mangan", "mg"),
    "317": ("Selenium", "Selen", "mcg")
}

VITAMINS = {
    "318": ("Vitamin A", "Vit A", "IU"),
    "319": ("Vitamin A1 (Retinol)", "Retinol", "mcg"),
    "321": ("Beta-Carotene", "b-Carot", "mcg"),
    "322": ("Alpha-Carotene", "a-Carot", "mcg"),
    "323": ("Vitamin E (a-Tocopherol)", "Vit E", "mg"),
    "324": ("Vitamin D", "Vit D", "IU"),
    "325": ("Vitamin D2 (Ergocalciferol)", "Vit D2", "mcg"),
    "326": ("Vitamin D3 (Cholecalciferol)", "Vit D3", "mcg"),
    "342": ("Vitamin E (g-Tocopherol)", "Vit E-g", "mg"),
    "401": ("Vitamin C (Ascorbic Acid)", "Vit C", "mg"),
    "404": ("Vitamin B1 (Thiamin)", "Vit B1", "mg"),
    "405": ("Vitamin B2 (Riboflavin)", "Vit B2", "mg"),
    "406": ("Vitamin B3 (Niacin)", "Vit B3", "mg"),
    "410": ("Vitamin B5 (Pantothenic Acid)", "Vit B5", "mg"),
    "415": ("Vitamin B6", "Vit B6", "mg"),
    "417": ("Vitamin B9 (Folate / Folic)", "Vit B9", "mcg"),
    "418": ("Vitamin B12 (Cobalamin)", "Vit B12", "mcg"),
    "421": ("Choline", "Choline", "mg"),
    "428": ("Vitamin K2 (Menaquinone-4)", "Vit K2", "mcg"),
    "430": ("Vitamin K1 (Phylloquinone)", "Vit K", "mcg")
}

NUTRIENTS = dict(AMINOS.items() + CARBS.items() + LIPIDS.items() +
                 MACROS.items() + MINERALS.items() + VITAMINS.items())

GUI_NUTRIENTS = (
    # Macros (6)
    "208",
    "203",
    "204",
    "205",
    "269",
    "291",
    # Minerals  (11)
    "301",
    "312",
    "313",
    "303",
    "304",
    "315",
    "305",
    "306",
    "317",
    "307",
    "309",
    # Vitamins (16)
    "318",
    "319",
    "322",
    "321",
    "404",
    "405",
    "406",
    "410",
    "415",
    "417",
    "418",
    "401",
    "324",
    "325",
    "326",
    "323",
    "430",
    "428",
    "421",
    # Lipids (8)
    "645",
    "646",
    "606",
    "605",
    "601",
    "851",
    "621",
    "631",
    "629"
    # Amino Acids (implemented in future version)
)

# FDA Daily Values for nutrients, based on Daily Reference Values in 21 CFR
# 101.9(c)(9) or Recommended Dietary Intakes in 21 CFR 101.9(c)(8)(iv) for FDA
# food labeling requirements.
FDA_RDV = {
    "203": (50, "g"),
    "204": (65, "g"),
    "205": (300, "g"),
    "208": (2000, "kcal"),
    "291": (25, "g"),
    "301": (1000, "mg"),
    "303": (18, "mg"),
    "304": (400, "mg"),
    "305": (1000, "mg"),
    "306": (3500, "mg"),
    "307": (2400, "mg"),
    "309": (15, "mg"),
    "312": (2, "mg"),
    "315": (2, "mg"),
    "317": (70, "mcg"),
    "318": (5000, "IU"),
    "323": (20, "mg"),
    "324": (400, "IU"),
    "401": (60, "mg"),
    "404": (1.5, "mg"),
    "405": (1.7, "mg"),
    "406": (20, "mg"),
    "410": (10, "mg"),
    "415": (2, "mg"),
    "417": (400, "mcg"),
    "418": (6, "mcg"),
    "430": (80, "mcg"),
    "601": (300, "mg"),
    "606": (20, "g")
}

# -----------------------------------------------------------------------------
# Supplementary Exercise Reference Data ---------------------------------------

MUSCLES = (
    "Abdominals",
    "Abductors",
    "Adductors",
    "Biceps",
    "Calves",
    "Chest",
    "Forearms",
    "Full Body",
    "Glutes",
    "Hamstrings",
    "Lats",
    "Lower Back",
    "Lower Body",
    "Middle Back",
    "NA",
    "Neck",
    "Obliques",
    "Quadriceps",
    "Shoulders",
    "Traps",
    "Triceps",
    "Upper Body",
)

# -----------------------------------------------------------------------------
# File Names ------------------------------------------------------------------

REF_DIR = "ReferenceSource"

REF_FILES = {
    "edref": "ExerciseDetails.json",
    "fdref": "FoodDetails.json",
    "fnref": "FoodNutrients.json",
}

USER_FILES = {
    "uprof": "Profile.json",
    "ureco": "Records.json",
    "usett": "Settings.json",
    "utemp": "Templates.json"
}

ALL_FILES = dict(REF_FILES.items() + USER_FILES.items())

# -----------------------------------------------------------------------------
# Build Elements --------------------------------------------------------------

NUTRITION_BUILD_ELEMENTS = {
    "Q": ("Quantity", ()),
    "I": ("Ingredient", ("Q",)),
    "R": ("Recipe", ("R", "I")),
    "M": ("Meal", ("R", "I")),
    "D": ("Diet", ("M",))
}

FITNESS_BUILD_ELEMENTS = {
    "S": ("Session", ()),
    "A": ("Activity", ("S",)),
    "W": ("Workout", ("A",)),
    "C": ("Cycle", ("W",)),
    "P": ("Program", ("C",))
}

BUILD_ELEMENTS = dict(
    NUTRITION_BUILD_ELEMENTS.items() + FITNESS_BUILD_ELEMENTS.items())

# -----------------------------------------------------------------------------
# Style Sheets ----------------------------------------------------------------

STYLE_ACTION = "".join([
    "QToolButton {\nbackground-color: qlineargradient(spread:pad, ",
    "x1:0.522, y1:0, x2:0.527, y2:1, stop:0 rgba(215, 255, 249, 255), ",
    "stop:1 rgba(187, 246, 248, 255));\nborder: 1px solid black;\n}\n\n",
    "",
    "QToolButton:hover {\nbackground-color: qlineargradient(spread:reflect, ",
    "x1:0.508, y1:1, x2:0.526975, y2:0, stop:0 rgba(173, 255, 119, 255), ",
    "stop:1 rgba(217, 255, 169, 255));\nborder: 2px solid rgb(60, 127, 177)",
    "\n}\n\n",
    "",
    "QToolButton:pressed:hover {\nbackground-color: ",
    "qlineargradient(spread:reflect, x1:0.508, y1:0, x2:0.512, ",
    "y2:1, stop:0 rgba(48, 215, 243, 255), stop:1 rgba(86, 255, ",
    "231, 255));\n}\n\n",
    "",
    "QToolButton:disabled {\nbackground-color: qlineargradient(",
    "spread:reflect, x1:0.508, y1:1, x2:0.526975, y2:0, stop:0 ",
    "rgba(109, 148, 161, 255), stop:1 rgba(171, 196, 207, 255));\n}"])

STYLE_BUILDMANAGERTAG = "".join([
    "QLabel {\ncolor: rgb(213, 255, 210);\nbackground-color: ",
    "qlineargradient(spread:reflect, x1:0.508, y1:1, x2:0.526975, ",
    "y2:0, stop:0.00497512 rgba(48, 184, 255, 255), stop:1 rgba(4, 150, ",
    "255, 255));\nborder: 2px solid rgb(2, 82, 255);\n}"])

STYLE_COMBOBOX = "".join([
    "QComboBox {\nborder: 1px solid black;\nborder-radius: 3px;\n",
    "background: qlineargradient(spread:pad, x1:0.512438, y1:1, x2:0.517413, ",
    "y2:0, stop:0 rgba(249, 188, 171, 255), stop:1 rgba(255, 225, 179, 255));",
    "\ncolor: black;\npadding: 1px 1px 1px 6px;\n}\n\n",
    "",
    "QComboBox::drop-down {\nwidth: 20px; border: 0px;\n}\n\n",
    "",
    "QComboBox::down-arrow {\nimage: url(:/icons/go_down.png);\n",
    "width: 20px;\nheight: 20px;\nborder: 0px;\n}\n\n",
    ""
    "QComboBox QAbstractItemView {\nbackground-color: qlineargradient(",
    "spread:pad, x1:0.512438, y1:1, x2:0.517413, y2:0, stop:0 rgba(249, ",
    "188, 171, 255), stop:1 rgba(255, 225, 179, 255));;\ncolor: black;\n",
    "selection-background-color: yellow;\nselection-color: black;\n}\n\n"])

STYLE_COPYTAG = "".join([
    "QLabel {\nborder-radius: 5px;\nborder: 1px solid black;\n",
    "background-color: #96E3FF;\n}"])

STYLE_GUIDETAG = "".join([
    "QLabel {\ncolor: rgb(24, 24, 255);\nbackground-color: qlineargradient(",
    "spread:reflect, x1:0.508, y1:1, x2:0.526975, y2:0, stop:0 rgba(229, ",
    "240, 162, 255), stop:1 rgba(248, 255, 111, 255));\nborder: 2px solid ",
    "rgb(24, 24, 255);\n}"])

STYLE_INVENTORYMANAGERTAG = "".join([
    "QLabel {\ncolor: rgb(255, 253, 189);\nbackground-color: ",
    "qlineargradient(spread:reflect, x1:0.513, y1:0, x2:0.517, y2:1, ",
    "stop:0.0447761 rgba(176, 175, 93, 255), stop:1 rgba(159, 139, 60, ",
    "255));\nborder: 2px solid rgb(136, 109, 10);\n}"])

STYLE_LOGINFRAME = "".join([
    "QFrame#login {\nbackground-color: qlineargradient(spread:pad, x1:1, "
    "y1:1, x2:1, y2:0, stop:0 rgba(209, 209, 209, 255), stop:1 rgba(",
    "255, 255, 255, 255));\nborder: 1px solid black;\n}\n\n",
    "",
    "QLineEdit {\nborder: 1px solid black;\n}"])

STYLE_MAINFRAME = "".join([
    "QFrame {\nbackground-color: qlineargradient(spread:pad, ",
    "x1:1, y1:1, x2:1, y2:0, stop:0 rgba(209, 209, 209, 255), ",
    "stop:1 rgba(255, 255, 255, 255));\n}\n\n",
    "",
    "QToolButton {\nbackground-color: transparent;\nborder: ",
    "1px solid black;\n}\n\n",
    "",
    "QToolButton:hover {\nbackground-color: rgba(255, 250, 161);\n}\n\n",
    "",
    "QToolButton:pressed:hover {\nbackground-color: ",
    "qlineargradient(spread:reflect, x1:0.508, y1:0, x2:0.512, ",
    "y2:1, stop:0 rgba(0, 204, 243, 255), stop:1 rgba(0, 251, ",
    "255, 255));\nborder: 1px solid rgb(60, 127, 177);\n}\n\n",
    "",
    "QToolButton:checked, QToolButton:pressed {\n",
    "background-color: qlineargradient(spread:reflect, ",
    "x1:0.508, y1:1, x2:0.526975, y2:0, stop:0 rgba(153, 255, ",
    "237, 255), stop:1 rgba(4, 255, 220, 255));\nborder: 1px ",
    "solid rgb(60, 127, 177);\n}\n\n",
    "",
    "QToolButton:checked:hover {\nbackground-color: ",
    "qlineargradient(spread:reflect, x1:0.508, y1:1, ",
    "x2:0.526975, y2:0, stop:0 rgba(153, 255, 237, 255), ",
    "stop:1 rgba(4, 255, 220, 255));\nborder: 1px solid rgb(",
    "60, 127, 177);\n}\n\n",
    "",
    "QToolButton:disabled {\nbackground-color: qlineargradient(",
    "spread:reflect, x1:0.508, y1:1, x2:0.526975, y2:0, stop:0 ",
    "rgba(109, 148, 161, 255), stop:1 rgba(171, 196, 207, 255));\n}"])

STYLE_HOMEMESSAGE = "".join([
    "QLabel {\nborder-radius: 5px;\nborder: 1px solid black;\n",
    "background: qlineargradient(spread:pad, x1:1, y1:1, x2:1, y2:0, ",
    "stop:0 rgba(209, 209, 209, 255), stop:1 rgba(255, 255, 255, 255));\n}"])

STYLE_PROFILEFRAME = "".join([
    "QFrame#profile {\nbackground-color: rgb(255, 244, 180);\nborder: ",
    "1px solid black;\n}\n\n"])

STYLE_PROFILETAG = "".join([
    "QLabel {\ncolor: black;\nbackground-color: rgb(255, 244, 180);\n",
    "border-left: 1px solid black;\nborder-top: 1px solid black;\n",
    "border-right: 1px solid black;\n}"])

STYLE_SELECTION = "".join([
    "QToolButton {\nbackground-color: qlineargradient(spread:",
    "pad, x1:0.512438, y1:1, x2:0.517413, y2:0, stop:0 rgba(",
    "249, 188, 171, 255), stop:1 rgba(255, 225, 179, 255));\n",
    "border: 1px solid black;\n}\n\n",
    "",
    "QToolButton:hover {\nbackground-color: rgba(255, 250, 161);\n",
    "border: 2px solid rgb(60, 127, 177);\n}",
    "",
    "QToolButton:pressed:hover {\nbackground-color: rgb(0, ",
    "255, 127);\n}\n\n",
    "",
    "QToolButton:checked:hover {\nbackground-color: qlineargradient(",
    "spread:reflect, x1:0.508, y1:1, x2:0.526975, y2:0, stop:0 rgba(",
    "173, 255, 119, 255), stop:1 rgba(217, 255, 169, 255));\nborder: ",
    "1px solid rgb(4, 171, 60);\n}\n\n",
    "",
    "QToolButton:checked, QToolButton:pressed {\nbackground-color: ",
    "qlineargradient(spread:reflect, x1:0.508, y1:1, x2:0.526975, y2:0, ",
    "stop:0 rgba(173, 255, 119, 255), stop:1 rgba(217, 255, 169, 255));\n",
    "border: 1px solid rgb(4, 171, 60);\n}\n\n",
    "",
    "QToolButton:disabled {\nbackground-color: qlineargradient(",
    "spread:reflect, x1:0.508, y1:1, x2:0.526975, y2:0, stop:0 ",
    "rgba(109, 148, 161, 255), stop:1 rgba(171, 196, 207, 255));\n}"])

STYLE_SELECTTAG = "".join([
    "QLabel {\nborder-radius: 5px;\nborder: 1px solid black;\n",
    "background-color: #F4E3B2;\n}"])

STYLE_STICKER = "".join([
    "QLabel {\nborder-radius: 5px;\nborder: 1px solid black;\n",
    "background-color: white;\n}"])

STYLE_TABLE = "".join([
    "QTableWidget::item:hover {\nbackground: rgba(255, 250, 161);\n}\n\n",
    "",
    "QTableWidget::item:selected {\ncolor: black;\n}\n\n",
    "",
    "QTableWidget::item::selected:active {\nbackground: qlineargradient(",
    "spread:reflect, x1:0.508, y1:1, x2:0.526975, y2:0, stop:0 rgba(",
    "173, 255, 119, 255), stop:1 rgba(217, 255, 169, 255));\n}\n\n",
    "",
    "QTableWidget::item:selected:!active {\nbackground: #D4F8BC\n}"])

STYLE_TIPBOX = "".join([
    "QPlainTextEdit {\nbackground-color: rgba(255, 255, 255, 0);\n"
    "border: 1px solid black;\n}"])

STYLE_TITLETAG = "".join([
    "QLabel {\nbackground-color: rgb(155, 255, 5);\nborder: ",
    "3px solid black;\nborder-radius: 10px;\n}"])

STYLE_TREE = "".join([
    "QTreeWidget::item {\nborder: 1px solid #BDC3C7;\nborder-top-color: ",
    "transparent;\nborder-bottom-color: transparent;\nborder-right-color: ",
    "transparent;}\n\n",
    "",
    "QTreeWidget::item:hover {\nbackground: rgba(255, 250, 161);\n",
    "border: 2px solid blue;\nborder-top-color: transparent;\n",
    "border-bottom-color: transparent;\nborder-right-color: transparent;\n",
    "}\n\n",
    "",
    "QTreeWidget::item:selected {\nborder: 1px solid #14CF04;\n",
    "color: black;\n}\n\n",
    "",
    "QTreeWidget::item::selected:active {\nbackground: qlineargradient(",
    "spread:reflect, x1:0.508, y1:1, x2:0.526975, y2:0, stop:0 rgba(",
    "173, 255, 119, 255), stop:1 rgba(217, 255, 169, 255));\n}\n\n",
    "",
    "QTreeWidget::item:selected:!active {\nbackground: #D4F8BC\n}"])

# -----------------------------------------------------------------------------
# Common Icons ----------------------------------------------------------------

ICONS = {
    "createnew": "add_circleblack",
    "diary": "book",
    "fitness": "runner",
    "guide": "bullseye",
    "information": "msg_info",
    "nutrition": "dining",
    "ontrack": "dining_crossed",
    "plot": "chart_bar",
    "quantity": "basket",
    "refresh": "refresh",
    "session": "dumbbell"
}

# -----------------------------------------------------------------------------
# Guide Text ------------------------------------------------------------------

GUIDE_TEXTA = "".join([
    "USER GUIDE\n\n\n",
    "",
    "",
    "OnTrack is an app that lets you track nutrition and fitness routines. ",
    "You can record every food you eat and every exercise you complete. ",
    "You can make templates of your routines to use again and again. ",
    "You can track health measurements like weight and percent body fat. ",
    "You can set nutrient targets and see how closely you stick to them. ",
    "You can plot graphs of your nutrition and fitness progress over time. ",
    "OnTrack provides the tools, but it's up to you to use them.\n\n",
    "",
    "---------- A. Pages\n\n",
    "",
    "OnTrack is divided into four pages. Once you are logged in, you can go ",
    "to any page using the Main Menu at the top of the window. Each page has ",
    "its own set of tools.\n\n",
    "",
    "The 'Home' page is the first thing you see when you open OnTrack. Here, ",
    "you can create, delete, and log in app users. The 'Profile' page has ",
    "tools that let you track health measurements in your Health Diary, set ",
    "nutrient targets in your Nutrient Guide, and plot graphs of your ",
    "nutrition and fitness progress. The 'Builder' page has tools that let ",
    "you record your routines and manage your saved references, templates, ",
    "and records. The 'Guide' page, as you know, provides a handy user guide ",
    "and a glossary of terms. Please read these carefully if this is your ",
    "first time using OnTrack.\n\n",
    "",
    "---------- B. Menus and Buttons\n\n",
    "",
    "OnTrack's tools have many different button menus and drop-down lists. ",
    "If you are ever unsure of what a button or drop-down does, move your ",
    "mouse cursor over it and read the status bar tip at the bottom of the ",
    "window. If a button is grayed out, it has been disabled and cannot be ",
    "clicked. If a button's action cannot be executed at any given time, it ",
    "will likely be disabled.\n\n",
    "",
    "---------- C. Logging In\n\n",
    "",
    "The Login Menu on the Home page lets you create new app users and ",
    "select active app users to either delete or log in. Only one user can ",
    "be logged in at a time, and the only way to log out is to switch users ",
    "or exit the app. Each new user's username must be 1-30 characters ",
    "long and contain only letters, numbers, hyphens, and underscores.\n\n",
    "",
    "---------- D. Settings\n\n",
    "",
    "The Settings button on the Home page lets you change app behavior. ",
    "These settings are:\n\n",
    "",
    "---Default User: select the user who is logged in each time OnTrack ",
    "starts\n",
    "---Exit Confirmation: check to ask for confirmation before exiting ",
    "OnTrack\n",
    "---Delete Confirmation: check to ask for confirmation before deleting ",
    "inventory items\n",
    "---Build Info: check to see info for the build, uncheck to see info ",
    "for just the selected element\n",
    "---Sort By ID: check to sort inventory items by item ID, uncheck to ",
    "sort by description\n",
    "---Sort Ascending: check to sort inventory items in ascending order, ",
    "uncheck to sort descending\n",
    "---Nutrients: check and select the order of all nutrients shown in the ",
    "Build Info Viewer\n",
    "---Muscles: check and select the order of all muscles shown in the ",
    "Build Info Viewer\n\n",
    "",
    "---------- E. Health Diary\n\n",
    "",
    "Your Health Diary is a record of health measurements tied to a specific ",
    "entry date. Measurements include one or more 'health metrics', which ",
    "can be anything from your weight to how long you slept, and their ",
    "corresponding values. Each time you add a Health Diary entry, you can ",
    "enter measurements for any number of existing or newly created health ",
    "metrics.\n\n",
    "",
    "---------- F. Nutrient Guide\n\n",
    "",
    "Your Nutrient Guide is a record of nutrient targets tied to a specific ",
    "effective date (the date that those targets go into effect). A nutrient ",
    "target is the amount of it that you want to consume per day. Targets ",
    "can be set for one or more nutrients, and all targets must be greater ",
    "than zero. You can specify targets as values for specific units of ",
    "measure (e.g. 100 g), or as percentages of the FDA daily recommended ",
    "values (e.g. 15%)\n\n",
    "",
    "---------- G. Data Plotter\n\n",
    "",
    "The Data Plotter lets you plot one of nine types of data on a graph. ",
    "The plot types and their data sources are:\n\n",
    "",
    "---Health Metrics: Health Diary health metric measurements\n",
    "---Nutrient Targets: Nutrient Guide nutrient target values\n",
    "---Macronutrient Proportions: Nutrition (Diet) records\n",
    "---Meal Times: Nutrition (Diet) records\n",
    "---Nutrient Values: Nutrition (Diet) records\n",
    "---Performance Per Exercise: Fitness (Program) records\n",
    "---Performance Per Muscle: Fitness (Program) records\n",
    "---Performance Per Tag: Fitness (Program) records\n",
    "---Workout Periods: Fitness (Program) records\n\n",
    "",
    "Click a Data Plotter Menu button to open its plot window. The toolbar ",
    "at the top of each plot window lets you select a date range and, ",
    "sometimes, one or more subcategories for which to plot all applicable ",
    "data points. The toolbar also presents Pan/Zoom and Save buttons. Click ",
    "Pan/Zoom and hold down the left mouse button over the graph to move it ",
    "around the viewer. Hold down the right mouse button over the graph to ",
    "zoom in and out of it. Click Save to save the graph as a PNG image ",
    "file.\n\n",
    ""
    "---------- H. Build Manager\n\n",
    "",
    "The Build Manager lets you create 'builds', which are representations ",
    "of nutrition and fitness routines. A build is made up of 'build ",
    "elements' which correspond to real world components of nutrition and ",
    "fitness routines. Each element has a clear and distinct name to ",
    "indicate which component it represents and how it relates to the other ",
    "build elements. This relationship between build elements is ",
    "called a 'build hierarchy'. A build is shown as a data tree inside ",
    "of the Build Manager's Build Viewer. As you create builds, it will ",
    "become clearer what build elements are and how they fit together.\n\n",
    "",
    "Nutrition build elements represent edibles that you consume in a given ",
    "period of time. Below is the nutrition build hierarchy, from largest ",
    "to smallest, with element names and descriptions. Each element can have ",
    "added to it the next element directly below it, with two exceptions. A ",
    "Meal can have both Recipes and Ingredients added to it, and a Recipe ",
    "can have both Ingredients and other Recipes added to it. This behavior ",
    "reflects real world nutrition routines.\n\n",
    "",
    "---Diet: all of the Meals consumed on a specific date\n",
    "---Meal: all of the Recipes or Ingredients consumed at a time of day\n",
    "---Recipe: a collection of Ingredients and its portion size\n",
    "---Ingredient: a Food that is consumed as part of a Meal or Recipe\n",
    "---Quantity: a portion size of an Ingredient\n\n",
    "",
    "Fitness build elements represent actions that you complete in a given ",
    "period of time for the purpose of physical fitness. Below is the ",
    "fitness build hierarchy, from largest to smallest, with element names ",
    "and descriptions. Each element can have added to it the next element ",
    "directly below it, with no exceptions.\n\n",
    "",
    "---Program: a unique collection of Workout Cycles from a start date ",
    "onward\n",
    "---Cycle: a collection of Workouts that may or may not be repeated\n",
    "---Workout: all of the Activities completed over a continuous period\n",
    "---Activity: an Exercise that is completed as part of a Workout\n",
    "---Session: a performance measurement of an Activity\n\n",
    "",
    "You can start a build with a new element or with a saved template or ",
    "record. Once your build is shown in the Build Viewer, you can use the ",
    "Build Menu buttons to change it to match your routine. Any Diet or ",
    "Program build can be saved as a record. Any Diet, Meal, Recipe, ",
    "Program, Cycle, or Workout build or build element can be saved as a ",
    "template. Be aware that some information is lost when saving templates. ",
    "This forces you to enter accurate, up to date information each time a ",
    "template is used.\n\n",
    "",
    "Diet and Program records make up the bulk of your data. A Diet record ",
    "captures all Foods eaten on a single day. Nutrition graphs made ",
    "by the Data Plotter reference your Diet records and plot a data point ",
    "for each applicable Diet date. A Program record is much different. It ",
    "typically captures all Exercises completed over several weeks--or even ",
    "months. Fitness graphs made by the Data Plotter reference your Program ",
    "records and plot a data point for each applicable date on which you ",
    "started a Workout. If you started two Workouts on the same day, then ",
    "that date will show two different data points on your graph.\n\n",
    "",
    "Diet and Program records are also recorded much differently. To capture ",
    "each day's Foods, you must create a new Diet build, fill it with your ",
    "nutrition data, and save it--very straightforward. To capture each ",
    "day's Exercises, you can create a new Program build or find the ",
    "Program record to which they should be added. To update an existing ",
    "Program record with a new day's worth of Exercises, you must find the ",
    "applicable Program record inventory item, send that Program item to the ",
    "Build Viewer to edit, add to it a new Workout, fill the Workout with ",
    "your fitness data, and save your updated Program over the existing ",
    "record. It is not recommended that you create a new Program for each ",
    "day's Exercises. It is also not recommended that your Program records ",
    "capture more than 6-10 weeks worth of Workouts.\n\n",
    "",
    "---------- I. Build Info Viewer\n\n",
    "",
    "The Build Info Viewer, at the bottom of the Builder page, shows you ",
    "updated information for your build. This information differs between ",
    "nutrition and fitness builds. Nutrition build info shows a set of ",
    "nutrients and each one's value, unit of measure, and percentage of its ",
    "most recent target (or zero, if no target is set). Fitness build info ",
    "shows a set of muscles and the total number of Sessions that focus on ",
    "each one, as well as the total effort and maximum intensity values for ",
    "all of those Sessions. You can change the 'Build Info' setting to show ",
    "info for the entire build or just the selected build element.\n\n",
    "",
    "---------- J. Inventory Manager\n\n",
    "",
    "The Inventory Manager lets you load a reference, template, or record ",
    "inventory into the Inventory Viewer and add, edit, and delete its ",
    "items. Each item's ID and description are shown in the Viewer. ",
    "Performance metric units are also shown for each Exercise item--in case ",
    "the same Exercise was created more than once but with different units ",
    "each time. To load an inventory, just select it from the drop-down ",
    "list at the top of the Inventory Manager.\n\n",
    "",
    "Reference items are the fundamental building blocks of every nutrition ",
    "and fitness routine. The two references are Foods and Exercises. You'll ",
    "notice that OnTrack comes with references built into it. The Foods are ",
    "sourced from the USDA National Nutrient Database for Standard Reference ",
    "(Release 28), and the Exercises are those which are common to most ",
    "training programs. In your build, Foods are represented by ",
    "'Ingredients', and Exercises are represented by 'Activities'.\n\n",
    "",
    "Each type of reference item has a unique set of properties. Foods have ",
    "an associated food group, a set of unit sequences, and a distinct ",
    "nutrient content. Each unit sequence consists of a portion size (e.g. ",
    "1 cup) and that portion's weight in grams. Nutrient content is a set of ",
    "nutrients and their values for a specific portion size of the Food. ",
    "Exercises have a focus muscle, two performance metric units, and a set ",
    "of tags. The focus muscle is the muscle targeted by the Exercise. The ",
    "performance metric units are custom measurement units for the Exercise ",
    "Session performance metrics 'effort' and 'intensity'. Tags are ",
    "unique (and optional) labels that you can use to categorize similar ",
    "Exercises.\n\n",
    "",
    "You can save reference items to your hard drive as 'Data Capsules'. ",
    "A Data Capsule is a file with a .json extension that encapsulates a ",
    "reference item's properties. This file can be shared between users so ",
    "that new references only have to be created in full one time. To use a ",
    "Data Capsule, create the new reference as usual, save its Data Capsule ",
    "to your hard drive, and then send it to fellow OnTrack users. Each ",
    "of them can load it using the applicable Inventory Menu button.\n\n",
    "",
    "The Inventory Manager also lets you add, edit, and delete templates and ",
    "records. Be aware that you can edit the properties of a template or ",
    "record, but you cannot edit its component build elements. To do so, ",
    "you must use the applicable Inventory Menu button to send it to the ",
    "(empty) Build Viewer to edit, make your changes, and save it again. ",
    "Re-saving a template will create a new template with the new structure. ",
    "Re-saving a record--without changing its Diet date or Program start ",
    "date--will replace your existing record."])

GUIDE_TEXTB = "".join([
    "GLOSSARY\n\n\n",
    "",
    "",
    "ACTIVITY: a fitness build element that represents an Exercise reference ",
    "item in a build. It has no properties of its own. It can be added to a ",
    "Workout. Sessions can be added to it.\n\n",
    "",
    "BUILD: a data tree representation of a nutrition or fitness routine. It ",
    "is made up of build elements. It can be edited using the Build Menu. ",
    "Depending on its elements, it can be saved as a template or record. Its ",
    "data structure is shown in the Build Viewer. Information about its ",
    "elements is shown in the Build Info Viewer.\n\n",
    "",
    "BUILD ELEMENT: a component of a build that represents a real world ",
    "component of a nutrition or fitness routine. Nutrition build elements ",
    "are: Diets, Meals, Recipes, Ingredients, and Quantities. Fitness build ",
    "elements are: Programs, Cycles, Workouts, Activities, and Sessions. ",
    "A build element has a set of unique properties. Some elements can be ",
    "added to other elements based on the applicable build hierarchy.\n\n",
    "",
    "BUILD HIERARCHY: the order in which build elements can be added to ",
    "other build elements. The nutrition build hierarchy is, from largest ",
    "to smallest: Diet > Meal > Recipe > Ingredient > Quantity. The fitness ",
    "build hierarchy is, from largest to smallest: Program > Cycle > Workout ",
    "> Activity > Session. Generally, a build element can have elements ",
    "that are of the next smallest type added to it. For example, a Cycle ",
    "can have one or more Workouts added to it. Nutrition build elements ",
    "have two exceptions that reflect real world counterparts. Both Recipes ",
    "and Ingredients can be added to a Meal. Both Recipes and Ingredients ",
    "can be added to a Recipe.\n\n",
    "",
    "BUILD MANAGER: a tool to create and save nutrition and fitness ",
    "builds.\n\n",
    "",
    "CYCLE: a fitness build element that represents a collection of Workouts ",
    "that may or may not be repeated. It only has a 'description' property. ",
    "Its 'description' is a 1-200 character identifier. It can be ",
    "added to a Program. Workouts can be added to it. It can be saved as a ",
    "template.\n\n",
    "",
    "DATA CAPSULE: a file with a .json extension that encapsulates all of a ",
    "Food or Exercise reference item's properties. A Data Capsule is saved ",
    "for a reference item using the Inventory Manager. A Data Capsule ",
    "can be shared with other OnTrack users to let them create the same ",
    "item in their own reference inventory.\n\n",
    "",
    "DATA PLOTTER: a tool to plot specific types of recorded data on a ",
    "graph. Plotted data is sourced from the Health Diary, the Nutrient ",
    "Guide, Diet records, and Program records. Each plot window's toolbar ",
    "has input fields to restrict data points to a specific date range and ",
    "subcategory. Two additional buttons are found in the toolbar. The ",
    "Pan/Zoom button lets you move the graph by holding in the left mouse ",
    "button over the canvas. It also lets you zoom in and out of the graph ",
    "by holding in the right mouse button over the canvas. The Save button ",
    "lets you save the graph as a PNG image file.\n\n",
    "",
    "DIET: a nutrition build element that represents all Meals consumed ",
    "on a specific date. It has 'description' and 'date' properties. Its ",
    "'description' is a 1-200 character identifier. Its 'date' is the ",
    "date on which the Diet was eaten. Meals can be added to it. It can be ",
    "saved as a template or record.\n\n",
    "",
    "EFFECTIVE DATE: the date on which a set of Nutrient Guide targets goes ",
    "into effect.\n\n",
    "",
    "EFFORT: how much work you did during a Session. It is one of two ",
    "metrics used by OnTrack to record Exercise performance. Its unit of ",
    "measure is a component of the Exercise property 'performance metric ",
    "units'. A typical effort unit for weightlifting Exercises is 'rep' ",
    "(repetitions), and typical effort units for cardio Exercises are 'min' ",
    "(minutes), 'mi' (miles), and 'km' (kilometers). All Exercises must have ",
    "an effort unit so that performance progress can be tracked. A Session's ",
    "'magnitude' value is calculated by multiplying its effort amount by its ",
    "intensity amount.\n\n",
    "",
    "ENTRY DATE: the date for which a set of Health Diary measurements is ",
    "recorded.\n\n",
    "",
    "EXERCISE: a fitness reference item. It has four properties. Its ",
    "'description' is a 1-200 character identifier. Its 'focus ",
    "muscle' is the muscle it works the hardest. Its 'performance metric "
    "units' are the associated units of measure for the 'effort' and ",
    "'intensity' performance metrics. Its 'tags' are additional identifiers ",
    "used to categorize it with similar Exercises. It is represented ",
    "in a build by an Activity build element.\n\n",
    "",
    "FOOD: a nutrition reference item. It has four properties. Its ",
    "'description' is a 1-200 character identifier. Its 'food group' ",
    "is just that. Its 'unit sequences' are sets of portion sizes and ",
    "each one's equivalent weight in grams. Its 'nutrient content' is a ",
    "set of nutrient values for a specific portion size. It is represented ",
    "in a build by an Ingredient build element.\n\n",
    "",
    "HEALTH DIARY: a tool to record health metric measurements and link them ",
    "to an entry date--the date for which those measurements apply. Health ",
    "metrics and their corresponding measurements are shown in the Health ",
    "Diary Viewer. Entries can be added or deleted. Metrics can be deleted. ",
    "The entire Health Diary can be saved as a spreadsheet.\n\n",
    "",
    "HEALTH MEASUREMENT: the value for a health metric that you measure on ",
    "a specific date.\n\n",
    "",
    "HEALTH METRIC: an aspect of your overall health that you want to ",
    "measure on a regular basis (e.g. weight). A health metric has a unit of ",
    "measure associated with it (e.g. lb/kg).\n\n",
    "",
    "INGREDIENT: a nutrition build element that represents a Food reference ",
    "item in a build. It has no properties of its own. It can be added to a ",
    "Meal or Recipe. Quantities can be added to it.\n\n",
    "",
    "INTENSITY: how hard you pushed yourself to do the work performed ",
    "during a Session. It is one of two metrics used by OnTrack to record ",
    "Exercise performance. Its unit of measure is a component of the ",
    "Exercise property 'performance metric units'. Typical intensity units ",
    "for weightlifting Exercises are 'lb' (pounds) and 'kg' (kilograms), and ",
    "typical intensity units for cardio Exercises are 'mph' (miles per hour) ",
    "and kph (kilometers per hour). Some Exercises do not have clear units ",
    "of measure for the intensity metric. A Session's 'magnitude' value is ",
    "calculated by multiplying its effort amount by its intensity amount.\n\n",
    "",
    "INVENTORY: a repository of saved reference, template, or record items. ",
    "Inventories can be loaded into the Inventory Viewer and edited using ",
    "the Inventory Menu.\n\n",
    "",
    "INVENTORY MANAGER: a tool to view and modify reference, template, and ",
    "record inventories.\n\n",
    "",
    "ITEM ID: a unique identifier for an inventory item. Reference and ",
    "template item IDs are numbers, while record item IDs are dates. A ",
    "reference's item ID is assigned automatically and cannot be changed ",
    "after it is created. A template's item ID is assigned automatically ",
    "and is only changed if you delete a template with a lower item ID. In ",
    "this case, all greater item IDs are reassigned to one number lower so ",
    "that template IDs are always consecutive numbers. A record's item ID is ",
    "simply its Diet date or Program start date, both of which can be ",
    "changed.\n\n",
    "",
    "MAGNITUDE: a Session's effort amount multiplied by its intensity ",
    "amount. It has no associated unit of measure. It can be used to ",
    "compare different Sessions of an Activity/Exercise in a very general ",
    "way. It is particularly useful when comparing Sessions that have ",
    "drastically different intensity amounts.\n\n",
    "",
    "MAX INTENSITY: the maximum intensity value for all applicable Sessions, ",
    "whether in a build or in a particular Workout. Fitness Build Info shows ",
    "max intensity for all Sessions in the build that target specific focus ",
    "muscles. Data Plotter plots show max intensity for all Sessions added ",
    "to each Workout. The Performance Per Exercise plot shows max intensity ",
    "for all Sessions that reference specific Exercises. The Performance Per ",
    "Muscle plot shows max intensity for all Sessions that target specific ",
    "focus muscles. The Performance Per Tag plot shows max intensity for all ",
    "Sessions that reference Exercises with specific tags. Max intensity ",
    "reported for a specific Exercise has the same measurement unit as that ",
    "Exercise's intensity unit. Max intensity reported for a muscle or tag ",
    "does not have a measurement unit.\n\n",
    "",
    "MEAL: a nutrition build element that represents all edibles consumed ",
    "at a specific time of day. It has 'description' and 'time' properties. ",
    "Its 'description' is a 1-200 character identifier. Its 'time' ",
    "is the time of day that the Meal was eaten. It can be added to a Diet. ",
    "Recipes and Ingredients can be added to it. It can be saved as a ",
    "template.\n\n",
    "",
    "NUTRIENT GUIDE: a tool to record nutrient targets and link them to a ",
    "an effective date--the date on which they go into effect. Targets ",
    "for a selected effective date are shown in the Nutrient Guide Viewer. ",
    "Targets can be added or deleted. The latest targets are used to ",
    "calculate target-percentage values in nutrition Build Info.\n\n",
    "",
    "NUTRIENT TARGET: the amount of a nutrient that you want to consume ",
    "in a single day.\n\n",
    "",
    "PERFORMANCE METRIC: an aspect of your Exercise performance that you ",
    "want to measure in order to track progress. OnTrack uses the metrics ",
    "'effort' and 'intensity' to capture performance. Effort is how much ",
    "work you did during a Session of an Activity/Exercise, and intensity ",
    "is how hard you pushed yourself to do that work.\n\n",
    "",
    "PERFORMANCE METRIC UNIT: a unit of measure associated with a ",
    "performance metric.\n\n",
    "",
    "PROGRAM: a fitness build element that represents a unique collection of ",
    "Workout Cycles completed from a start date onward. It has 'description' ",
    "and 'start' properties. Its 'description' is a 1-200 character ",
    "identifier. Its 'start' is the date on which the Program is started. ",
    "Cycles can be added to it. It can be saved as a template or record.\n\n",
    "",
    "QUANTITY: a nutrition build element that represents a portion size of ",
    "an Ingredient. It has no properties of its own. It can be added to an ",
    "Ingredient. Its portion size consists of two components: an amount ",
    "and the associated unit of measure (e.g. 1 cup).\n\n",
    "",
    "RECIPE: a nutrition build element that represents a collection of ",
    "Recipes and Ingredients. It has 'description' and 'portion' properties. ",
    "Its 'description' is a 1-200 character identifier. Its 'portion' ",
    "consists of three components: the amount that was consumed, the total ",
    "amount prepared, and the unit of measure associated with both amounts. ",
    "It can be added to a Meal. Recipes and Ingredients can be added to ",
    "it. It can be saved as a template.\n\n",
    "",
    "RECORD: a saved Diet or Program build that captured your daily routine. ",
    "Records retain all properties and component elements of a build. The ",
    "Data Plotter tool sources some of its plot data from Diet and Program ",
    "records. Record item IDs are Diet dates and Program start dates. There ",
    "is no limit to the number of records that can be saved.\n\n",
    "",
    "REFERENCE: a Food or Exercise. References are the fundamental building ",
    "blocks of every nutrition and fitness routine. Each type has a unique ",
    "set of properties. Foods and Exercises are represented in builds by ",
    "Ingredients and Activities. References can be saved as 'Data Capsules' ",
    "and shared between app users. Item IDs are automatically assigned to ",
    "references when they are saved. OnTrack comes with existing ",
    "references, but more can be created--up to 10000 of each type. ",
    "Reference items cannot be deleted if they are used in the current ",
    "build or are found in any saved templates or records.\n\n",
    ""
    "",
    "SESSION: a fitness build element that represents a performance ",
    "measurement of an Activity. It has no properties of its own. It can be ",
    "added to an Activity. Its performance measurement consists of three ",
    "components: an effort value, an intensity value, and a note. The note ",
    "is optional.\n\n",
    "",
    "TEMPLATE: a saved nutrition or fitness build that can be reused as a ",
    "future build, or as a component of a future build. Diet, Meal, Recipe, ",
    "Program, Cycle, and Workout builds can be saved as templates. Some ",
    "templates do not retain all properties or component elements of a ",
    "build. These properties or components must be reentered each time a ",
    "template is used. Diet dates default to the current date. Meal times ",
    "default to 00:00. Program start dates default to the current date. ",
    "Workout periods default to the current date beginning at 00:00 and ",
    "ending at 01:00. All Activities lose their Sessions. Item IDs ",
    "are automatically assigned to templates when they are saved. Up to 500 ",
    "templates of each type can be saved.\n\n",
    "",
    "TOTAL EFFORT: the total effort value for all applicable Sessions, ",
    "whether in a build or in a particular Workout. Fitness Build Info shows ",
    "total effort for all Sessions in the build that target specific focus ",
    "muscles. Data Plotter plots show total effort for all Sessions added ",
    "to each Workout. The Performance Per Exercise plot shows total effort ",
    "for all Sessions that reference specific Exercises. The Performance Per ",
    "Muscle plot shows total effort for all Sessions that target specific ",
    "focus muscles. The Performance Per Tag plot shows total effort for all ",
    "Sessions that reference Exercises with specific tags. Total effort ",
    "reported for a specific Exercise has the same measurement unit as that ",
    "Exercise's effort unit. Total effort reported for a muscle or tag ",
    "does not have a measurement unit.\n\n",
    "",
    "TOTAL MAGNITUDE: the total magnitude value for all applicable Sessions, ",
    "whether in a build or in a particular Workout. Data Plotter plots show ",
    "total magnitude for all Sessions added to each Workout. The Performance ",
    "Per Exercise plot shows total magnitude for all Sessions that reference ",
    "specific Exercises. The Performance Per Muscle plot shows total ",
    "magnitude for all Sessions that target specific focus muscles. The ",
    "Performance Per Tag plot shows total magnitude for all Sessions that ",
    "reference Exercises with specific tags. Total magnitude does not have a ",
    "measurement unit.\n\n",
    "",
    "WORKOUT: a fitness build element that represents all Activities ",
    "completed over a continuous period of time. It has 'description' and ",
    "'period' properties. Its 'description' is a 1-200 character ",
    "identifier. Its 'period' consists of two components: the date and time ",
    "that the Workout began and the date and time that the Workout ended. ",
    "It can be added to a Cycle. Activities can be added to it. It can be ",
    "saved as a template."])

"""
Helper Functions for Sample Data Generator
"""
from random import randint
from datetime import date as Date
from datetime import timedelta as TimeDelta

FILE_EXTENSION = ( 'jpg', 'png', 'pdf', 'docx' )

STATUS = [
  #"Reviewing",
  "Approved",
  "Denied",
  "Other Resolution",
  "Admin Close",
]

TRAVEL_TYPE = [
  "Mainland",
  "Interisland",
]

EXEMPTION_CATEGORY = [
  "CISA Federal Critical Infrastructure Sector",
  "Recreational Boat Arrival",
  "Recovered from COVID",
  "Other",
]

PURPOSE = [
  "CISA Federal Critical Infrastructure Sector",
  "Military PCS",
  "Federal Government",
  "Student",
  "Recovered from COVID",
  "Negative COVID Test",
  "Positive COVID Test",
  "Other",
  "Flight Crew",
  "Transit",
  "Teacher - DOE",
  "Teacher - Private",
  "State Employee",
  "County Employee",
  "Police / Fire",
  "Pre-Travel Testing Program",
  "Change of Quarantine Location",
  "Recreational Boat Arrival",
  "End of Life",
  "Compassion",
  "Patient Visit",
  "Funeral",
  "Vacation",
]

CISA_SUBCATEGORY = [
  "Healthcare / Public Health",
  "Law Enforcement / Public Safety / First Responder",
  "Food and Agriculture",
  "Energy",
  "Water and Wastewater",
  "Transportation and Logistics",
  "Public Works / Infrastructure Support",
  "Communications and IT",
  "Community or Government-Based Operation",
  "Critical Manufacturing",
  "Hazardous Materials",
  "Financial Services",
  "Chemical",
  "Defense Industrial Base",
  "Commercial Facilities",
  "Shelter, Housing, Real Estate, and Related Services",
  "Hygiene Products and Services",
]

DESTINATION_ISLAND = [
  "Oʻahu",
  "Maui",
  "Kauaʻi",
  "Lānaʻi",
  "Hawaiʻi (Big Island)",
  "Molokaʻi",
]

QUARANTINE_LOCATION_TYPE = [
  "Hotel / Motel",
  "Private Residence",
  "Air BnB / Vacation Rental",
  "Military Base / On Post",
]

ORIGIN_COUNTRY = [
  "United States",
  "Canada",
  "China",
  "Europe",
  "Hong Kong",
  "Japan",
  "Oceania",
  "South East Asia",
  "South Korea",
  "Taiwan",
]

ORIGIN_STATE = [
  "Alabama",
  "Alaska",
  "Arizona",
  "Arkansas",
  "California",
  "Colorado",
  "Connecticut",
  "Delaware",
  "Florida",
  "Georgia",
  "Hawaii",
  "Idaho",
  "Illinois",
  "Indiana",
  "Iowa",
  "Kansas",
  "Kentucky",
  "Louisiana",
  "Maine",
  "Maryland",
  "Massachusetts",
  "Michigan",
  "Minnesota",
  "Mississippi",
  "Missouri",
  "Montana",
  "Nebraska",
  "Nevada",
  "New Hampshire",
  "New Jersey",
  "New Mexico",
  "New York",
  "North Carolina",
  "North Dakota",
  "Ohio",
  "Oklahoma",
  "Oregon",
  "Pennsylvania",
  "Rhode Island",
  "South Carolina",
  "South Dakota",
  "Tennessee",
  "Texas",
  "Utah",
  "Vermont",
  "Virginia",
  "Washington",
  "West Virginia",
  "Wisconsin",
  "Wyoming",
  "American Samoa",
  "Guam",
  "Puerto Rico",
  "US Virgin Islands",
  "Northern Mariana Islands",
  "Washington D.C.",
  "Unknown",
]

ALPHABET = 'abcdefghijklmnopqrstuvwxyz'
ALPHANUMERIC = ALPHABET.upper() + ALPHABET + '0123456789'
ALPHA_CHARS = list(ALPHABET)
ALPHANUMERIC_CHARS = list(ALPHANUMERIC)

def capitalize(word):
    """
    Capitalizes the given string
    """
    return word[0].upper() + word[1:].lower()

def random_alphabet():
    """
    Returns randomly selected alphabet
    """
    return ALPHA_CHARS[randint(0, len(ALPHA_CHARS) - 1)]

def random_alphanumeric():
    """
    Returns randomly selected alphanumeric character
    """
    return ALPHANUMERIC_CHARS[randint(0, len(ALPHANUMERIC_CHARS) - 1)]

def random_number(low, high):
    """
    Returns randomly generated alphanumeric string
    """
    return randint(low, high)

def random_date(shifted_days = 0):
    """
    Returns randomly generated alphanumeric string
    """
    today = Date.today()
    date = today + TimeDelta(shifted_days)
    return date.strftime('%Y-%m-%d')

def random_string(length = 8, prefix = ''):
    """
    Returns randomly generated alphanumeric string
    """
    word = prefix
    for _ in range(length):
        word += random_alphanumeric()
    return word

def generate_id(length = 8, prefix = ''):
    """
    Returns randomly generated alphanumeric id
    """
    return random_string(length, prefix)

def generate_name():
    """
    Returns randomly generated name
    """
    length = randint(3, 7)
    name = random_alphabet().upper()
    for _ in range(length):
        name += random_alphabet()
    return name

def random_file_type():
    """
    Returns randomly selected file extension
    """
    return FILE_EXTENSION[randint(0, len(FILE_EXTENSION) - 1)]

def random_status():
    """
    Returns randomly selected Request Status
    """
    return STATUS[randint(0, len(STATUS) - 1)]

def random_exemption_category():
    """
    Returns randomly selected exemption category
    """
    return EXEMPTION_CATEGORY[randint(0, len(EXEMPTION_CATEGORY) - 1)]

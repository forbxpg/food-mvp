from django.conf import settings

# User constants
USERNAME_LENGTH = 150

# Tag constants
TAG_FIELDS_LENGTHS = 32

# Ingredient constants
INGREDIENT_NAME_LENGTH = 128
MEASUREMENT_UNIT_LENGTH = 64

# Recipe constants
RECIPE_NAME_LENGTH = 256
MAX_WORD_TRUNCATOR = 10
CHOICEFIELD_LENGTH = 2

# Pagination
DEFAULT_PAGE_SIZE = 6
PAGE_QUERY_PARAM = "page"
PAGE_SIZE_QUERY_PARAM = "limit"
MAX_PAGE_SIZE = 10

# Links
SHORT_LINK_LENGTH = 3
RECIPE_PATH_LENGTH = 255

# Fixture path
FIXTURE_PATH = settings.BASE_DIR / "fixtures"

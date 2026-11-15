# Acme Coffee Club settings
#
# Everything a customer would ask about lives in this one file.
# Change a value here and the app changes with it.

# How many days a new member can try Acme for free.
FREE_TRIAL_DAYS = 14

# Our plans. Prices are in US dollars per month.
PLANS = [
    {"name": "Free", "price_per_month": 0, "bags_per_month": 1, "billed": "per account"},
    {"name": "Pro", "price_per_month": 12, "bags_per_month": 3, "billed": "per account"},
    {"name": "Team", "price_per_month": 29, "bags_per_month": None, "billed": "per person"},
]

# Countries we ship coffee to.
SHIPPING_COUNTRIES = ["United States", "Mexico"]

# How many days after an order you can still ask for your money back.
REFUND_WINDOW_DAYS = 30

# When our support team is around to help.
SUPPORT_HOURS = "Monday-Friday, 9am-5pm Pacific"

# The shortest password we accept.
PASSWORD_MIN_LENGTH = 8

# Is dark mode available in the app yet?
DARK_MODE_ENABLED = False

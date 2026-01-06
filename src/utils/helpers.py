
import uuid
import random
from datetime import datetime, timedelta

def generate_uuid():
    """Generates a UUIDv4 string."""
    return str(uuid.uuid4())

def random_date(start_date, end_date):
    """Generates a random datetime between two dates."""
    time_between_dates = end_date - start_date
    days_between_dates = time_between_dates.days
    random_number_of_days = random.randrange(days_between_dates)
    return start_date + timedelta(days=random_number_of_days)

def get_weighted_choice(options, weights):
    return random.choices(options, weights=weights, k=1)[0]

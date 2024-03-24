from datetime import datetime


def compare_dates(date):
    """Comparates passed date to current time and calculate time difference string

    :param datetime date: date to be compared

    :return (boolean, string): Boolean true if date is in the past. String is difference between the dates in english
    """
    expired = False
    delta_date = date - datetime.now()
    days, seconds = delta_date.days, delta_date.seconds

    # If date is in the pase, difference in days is negative
    if days < 0:
        expired = True
        # Inverse delta to have positive values
        delta_date = datetime.now() - date
        days, seconds = delta_date.days, delta_date.seconds

    # Calculate hours and minutes
    hours = (days * 24 + seconds) // 3600
    minutes = (abs(seconds) % 3600) // 60

    # String parsing
    if abs(days) > 0:
        message_data = "{} days".format(abs(days))
    elif abs(hours) > 0:
        message_data = "{} hours".format(abs(hours))
    else:
        message_data = "{} minutes".format(abs(minutes))
    if expired:
        message_data += " ago"
    else:
        message_data = "in " + message_data
    return expired, message_data

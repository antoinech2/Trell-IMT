from datetime import datetime


def compare_dates(date):
    expired = False
    delta_date = date - datetime.now()
    days, seconds = delta_date.days, delta_date.seconds
    if days < 0:
        expired = True
        delta_date = datetime.now() - date
        days, seconds = delta_date.days, delta_date.seconds
    hours = (days * 24 + seconds) // 3600
    minutes = (abs(seconds) % 3600) // 60
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


import math

def encoder_date(date_objet):
    jour = date_objet.timetuple().tm_yday

    # Ajustement pour les années bissextiles
    if (
        date_objet.year % 4 == 0
        and (date_objet.year % 100 != 0 or date_objet.year % 400 == 0)
        and date_objet.month > 2
    ):
        jour -= 1

    angle = 2 * math.pi * (jour - 1) / 365

    return [math.sin(angle), math.cos(angle)]

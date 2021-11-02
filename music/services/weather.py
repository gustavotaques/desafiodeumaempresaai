from pyowm import OWM
from pyowm.utils import config
from pyowm.utils import timestamps
from pyowm.commons.exceptions import NotFoundError


def temperature_in_celsius(location):
    try:
        owm = OWM('b77e07f479efe92156376a8b07640ced')
        mgr = owm.weather_manager()

        observation = mgr.weather_at_place(location)
        w = observation.weather

        return w.temperature('celsius')['temp']
    except NotFoundError:
        return


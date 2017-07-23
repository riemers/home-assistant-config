import logging
import voluptuous as vol

_LOGGER = logging.getLogger(__name__)

DOMAIN = 'miele'
DEPENDENCIES = []

CONF_TEXT = 'text'
DEFAULT_TEXT = 'No text!'

def setup(hass, config):
    """Set up the Hello State component. """
    # Get the text from the configuration. Use DEFAULT_TEXT if no name is provided.
    text = config[DOMAIN].get(CONF_TEXT, DEFAULT_TEXT)

    # States are in the format DOMAIN.OBJECT_ID
    hass.states.set('miele.magnetron', text)


    return True

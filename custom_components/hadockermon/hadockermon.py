"""
A component which allows you to interact with ha-dockermon.
https://github.com/philhawthorne/ha-dockermon

For more details about this component, please refer to the documentation at
https://github.com/ludeeus/custom_component_hadockermon
"""
import json
import logging
import urllib.request
import voluptuous as vol
from datetime import timedelta
import homeassistant.helpers.config_validation as cv
from homeassistant.components.switch import (SwitchDevice, PLATFORM_SCHEMA)

headers = {}
headers['content-type'] = "application/octet-stream"

CONF_HOST = 'host'
CONF_EXCLUDE = 'exclude'
ATTR_STATUS = 'status'
ATTR_IMAGE = 'image'
SCAN_INTERVAL = timedelta(seconds=10)

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_HOST): cv.string,
    vol.Optional(CONF_EXCLUDE, default=None): vol.All(cv.ensure_list, [cv.string]),
})
_LOGGER = logging.getLogger(__name__)
def setup_platform(hass, config, add_devices_callback, discovery_info=None):
    """Set up the container switches."""
    url = "http://" + config.get(CONF_HOST) + ":8126/containers"
    response = urllib.request.urlopen(url);
    data = json.loads(response.read().decode("utf-8"))
    exclude = config.get(CONF_EXCLUDE)
    dev = []
    for item in data:
        container = str(item["Names"]).replace("[", "").replace("]", "").replace("/", "").replace("'", "")
        if container not in exclude:
            dev.append(ContainerSwitch(container, 'mdi:docker', config.get(CONF_HOST)))
    add_devices_callback(dev, True)
class ContainerSwitch(SwitchDevice):
    """Representation of a container switch."""
    def __init__(self, name, icon, host):
        """Initialize the Container switch."""
        self._name = name
        self._icon = icon
        self._host = host

    def update(self):
        req = urllib.request.Request('http://' + self._host + ':8126/container/' + self._name, headers = headers)
        html = urllib.request.urlopen(req).read()
        html = str(html).replace("'", "").replace("b", "")
        container = json.loads(str(html))
        state = container["state"]
        self._status = container["status"]
        self._image = container["image"]
        if state == 'running':
            self._state = True
        else:
            self._state = False

    @property
    def should_poll(self):
        """No polling needed for a container switch."""
        return True

    @property
    def name(self):
        """Return the name of the device if any."""
        return self._name

    @property
    def icon(self):
        """Return the icon to use for device if any."""
        return self._icon

    @property
    def device_state_attributes(self):
        return {
            ATTR_STATUS: self._status,
            ATTR_IMAGE: self._image,
        }

    @property
    def is_on(self):
        """Return true if switch is on."""
        return self._state

    def turn_on(self, **kwargs):
        """Turn the switch on."""
        self._state = True
        endpoint = '/start'
        req = urllib.request.Request('http://' + self._host + ':8126/container/' + self._name + endpoint, headers = headers)
        html = urllib.request.urlopen(req).read()
        #print(html)
        self.schedule_update_ha_state()

    def turn_off(self, **kwargs):
        """Turn the device off."""
        self._state = False
        endpoint = '/stop'
        req = urllib.request.Request('http://' + self._host + ':8126/container/' + self._name + endpoint, headers = headers)
        html = urllib.request.urlopen(req).read()
        #print(html)
        self.schedule_update_ha_state()

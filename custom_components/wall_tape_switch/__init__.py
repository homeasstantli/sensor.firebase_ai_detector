import logging
from homeassistant.core import HomeAssistant
from homeassistant.helpers.typing import ConfigType

_LOGGER = logging.getLogger(__name__)
DOMAIN = "wall_tape_switch"
WEBHOOK_ID = "wall_tape_ai_webhook_trigger"

async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Set up the Wall Tape Switch integration natively."""
    
    async def handle_webhook(hass, webhook_id, request):
        """Handle incoming data from the camera web app."""
        try:
            body = await request.json()
            state_value = body.get("state")
            
            if state_value:
                hass.states.async_set(
                    "binary_sensor.wall_tape_switch",
                    "on" if state_value == "me" else "off",
                    {
                        "friendly_name": "Wall Tape Switch",
                        "device_class": "motion",
                        "icon": "mdi:hand-back-left" if state_value == "me" else "mdi:wall"
                    }
                )
            return None
        except Exception as err:
            _LOGGER.error("Error processing Wall Tape integration webhook: %s", err)
            return None

    hass.components.webhook.async_register(
        DOMAIN, "Wall Tape Webhook", WEBHOOK_ID, handle_webhook
    )
    
    hass.states.async_set(
        "binary_sensor.wall_tape_switch", 
        "off", 
        {
            "friendly_name": "Wall Tape Switch", 
            "device_class": "motion",
            "icon": "mdi:wall"
        }
    )
    
    return True

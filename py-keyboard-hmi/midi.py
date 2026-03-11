import mido
from myglobal import logger, display_api
import requests


# note on off -> pompe on off
# controler 


# Map MIDI input to functions
midi_handlers = {
    'note_on': lambda msg: note_on_change(msg),
    'note_off': lambda msg: logger.info(f"Note Off: {msg.note}"),
    'control_change': lambda msg: control_change(msg)
}

map_contol_to_filter_value = {
    1 : "hue",
    2 : "saturation",
    3 : "brightness",
    4 : None,
    5 : "red",
    6 : "green",
    7 : "blue",
    8 : None
}

map_note_on_to_filter_action = {
    123 : {"action": "toggle_filter_group", "filter_group_id": "hsb"},
    127 : {"action": "toggle_filter_group", "filter_group_id": "rgb"},
}




def note_on_change(msg):
    logger.debug(f"Note On: {msg.note}")

    try:
        action = map_note_on_to_filter_action.get(msg.note)
        
        if action:
            url = display_api() + "/filter"
        
            logger.info(f"midi: send: {url}, json={action}")
            requests.post(url, json=action)
        else:
            logger.warning(f"Unmapped note: {msg.note}")
            
    except Exception as e:
        logger.error(f"Error sending note on message: {e}")



def control_change(msg):
    logger.debug(f"Control Change: {msg.control}={msg.value}")
   
    try:
        filter_name = map_contol_to_filter_value.get(msg.control)
        
        if filter_name:
            json = {"action": "set_value", "filter_id": filter_name, "value": msg.value}
            url = display_api() + "/filter"
            
            logger.info(f"midi: send: {url}, json={json}")
            requests.post(url, json=json)
        else:
            logger.warning(f"Unmapped control: {msg.control}")
                
    except Exception as e:
        logger.error(f"Error sending control message: {e}")





def listen_midis():
    # Open the first available MIDI input port
    with mido.open_input(mido.get_input_names()[1]) as port:
        logger.info("Listening for MIDI messages...")
        
        for message in port:
            logger.debug(message)      
            if message.type in midi_handlers:
                midi_handlers[message.type](message)



if __name__ == "__main__":
    listen_midis()
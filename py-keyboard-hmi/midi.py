import mido
from myglobal import logger, display_api, arduino_api
import requests


# note on off -> pompe on off
# controler 


# Map MIDI input to functions
midi_handlers = {
    'note_on': lambda msg: note_on_change(msg),
    'note_off': lambda msg: note_off_change(msg),
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
    120 : {"action": "filter_group_on", "filter_group_id": "h"},
    121 : {"action": "filter_group_on", "filter_group_id": "s"},
    122 : {"action": "filter_group_on", "filter_group_id": "b"},
    
    124 : {"action": "filter_group_on", "filter_group_id": "r"},
    125 : {"action": "filter_group_on", "filter_group_id": "g"},
    126 : {"action": "filter_group_on", "filter_group_id": "blue"},
}

map_note_off_to_filter_action = {
    120 : {"action": "filter_group_off", "filter_group_id": "h"},
    121 : {"action": "filter_group_off", "filter_group_id": "s"},
    122 : {"action": "filter_group_off", "filter_group_id": "b"},
    
    124 : {"action": "filter_group_off", "filter_group_id": "r"},
    125 : {"action": "filter_group_off", "filter_group_id": "g"},
    126 : {"action": "filter_group_off", "filter_group_id": "blue"}
 }

map_note_on_to_arduino_action = {
    48 : {"action": "set_pompe", "p": 0 , "t": 20},
    # 50 : {"action": "set_pompe", "p": 1 , "t": 20},
    # 52 : {"action": "set_pompe", "p": 2 , "t": 20},
    # 53 : {"action": "set_pompe", "p": 3 , "t": 20}
}

map_note_off_to_arduino_action = {
    48 : {"action": "set_pompe", "p": 0 , "t": 0},
    # 50 : {"action": "set_pompe", "p": 1 , "t": 0},
    # 52 : {"action": "set_pompe", "p": 2 , "t": 0},
    # 53 : {"action": "set_pompe", "p": 3 , "t": 0}
}


def note_off_change(msg):
    logger.debug(f"Note Off: {msg.note}")
    
    try:
        action_arduino = map_note_off_to_arduino_action.get(msg.note)
        if action_arduino:
            url = arduino_api() + "/command"
            logger.info(f"midi: send: {url}, json={action_arduino}")
            requests.post(url, json=action_arduino)
     
        action_filter = map_note_off_to_filter_action.get(msg.note)
        if action_filter:
            url = display_api() + "/filter"
            logger.info(f"midi: send: {url}, json={action_filter}")
            requests.post(url, json=action_filter)    
            
    except Exception as e:
        logger.error(f"Error sending note off message: {e}")


def note_on_change(msg):
    logger.debug(f"Note On: {msg.note}")

    try:
        action_filter = map_note_on_to_filter_action.get(msg.note)
        if action_filter:
            url = display_api() + "/filter"
            logger.info(f"midi: send: {url}, json={action_filter}")
            requests.post(url, json=action_filter)    
       
        action_arduino = map_note_on_to_arduino_action.get(msg.note)
        if action_arduino:
            url = arduino_api() + "/command"
            logger.info(f"midi: send: {url}, json={action_arduino}")
            requests.post(url, json=action_arduino)
            
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
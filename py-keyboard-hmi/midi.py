import mido
from myglobal import logger, display_api
import requests


# note on off -> pompe on off
# controler 


# Map MIDI input to functions
midi_handlers = {
    'note_on': lambda msg: logger.info(f"Note On: {msg.note}"),
    'note_off': lambda msg: logger.info(f"Note Off: {msg.note}"),
    'control_change': lambda msg: control_change(msg)
}


def control_change(msg):
    logger.debug(f"Control Change: {msg.control}={msg.value}")
   
    try:
        match msg.control:
         
            case 1 | 2 | 3:
                
                json={"filter": msg.control, "value": msg.value}
                url= display_api() + "/filter"
                
                logger.info(f"midi: send: {url}, json={json}")
                requests.post(url,json=json)
          
            case _:
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
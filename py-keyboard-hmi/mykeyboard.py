import keyboard  
from myglobal import logger
from arduinocomm import send_cmd

simplecmd = {
    'i': '/info'
}

keycmd = {
    'a': '/setpompe?p=0&t={param}',
    's': '/setpompe?p=1&t={param}',
    'd': '/setpompe?p=2&t={param}',
    'f': '/setpompe?p=3&t={param}',
}

keyparam = {
    '0': '1',
    '1': '2',
    '2': '4',
    '3': '8',
    '4': '16',
    '5': '32',
    '6': '64',
    '7': '128',
    '8': '256',
    '9': '512',
}

minimal_time = 0.25    


def hotkey_callback_generator(command, param = None, dummy = False):
    if param:
        command = command.replace("{param}", str(param))    
    def new_callback():
        logger.debug(f"trigger command: {command}")
        if not dummy: 
            send_cmd(command)
    
    return new_callback # return the function

    
def setup(dummy = False):
    """ Setup the hotkey to listen at keyboard event
    
    if dummy == True -> do not send it to arduino, only log
    """
    for key, command in keycmd.items():
        keyboard.add_hotkey(key, hotkey_callback_generator(command, minimal_time, dummy))
        
        # combination key + param
        for secondkey, param in keyparam.items():
            keyboard.add_hotkey(f"{key}+{secondkey}", hotkey_callback_generator(command, param, dummy))
   
    for key, command in simplecmd.items():
        keyboard.add_hotkey(key, hotkey_callback_generator(command))
   

if __name__ == "__main__":
    
    setup(dummy=True)
    # Stops the program when you hit esc
    keyboard.wait('q')
    logger.info('Exiting ...')

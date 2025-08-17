import keyboard  
from myglobal import logger
from arduinocomm import send_cmd

simplecmd = {
    'i': '/info'
}

keycmd = {
    '2': '/setpompe?p=0&t={param}',
    '6': '/setpompe?p=1&t={param}',
    '9': '/setpompe?p=2&t={param}',
    '1': '/setpompe?p=3&t={param}',
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

last_cmds = []


def records_cmds(cmd):
    global last_cmds 
    if len(last_cmds) >= 5:
        last_cmds.pop(0)
          
    last_cmds.append(str(cmd))
    if last_cmds == ['h','a','d','e','s']:
        logger.warning("hades")
        last_cmds = []
        send_cmd('/setpompe?p=0&t=16')
        send_cmd('/setpompe?p=1&t=16')
        send_cmd('/setpompe?p=2&t=16')
        send_cmd('/setpompe?p=3&t=16')
        
    
    logger.info(last_cmds)    
    

def hotkey_callback_generator(key, command, param = None, dummy = False):
    if param:
        command = command.replace("{param}", str(param))    
    def new_callback():
        logger.info(f"trigger command: {command}")
        if not dummy: 
            send_cmd(command)
        records_cmds(key) # should be keep after
    
    return new_callback # return the function

    
def setup(dummy = False):
    """ Setup the hotkey to listen at keyboard event
    
    if dummy == True -> do not send it to arduino, only log
    """
    logger.info("Setup ...")
    for key, command in keycmd.items():
        keyboard.add_hotkey(key, hotkey_callback_generator(key, command, minimal_time, dummy))
        
        # combination key + param
        for secondkey, param in keyparam.items():
            keyboard.add_hotkey(f"{key}+{secondkey}", hotkey_callback_generator(key, command, param, dummy))
   
    for key, command in simplecmd.items():
        keyboard.add_hotkey(key, hotkey_callback_generator(key, command))
   

if __name__ == "__main__":
    
    logger.info("start ...")
    setup(dummy=True)
    # Stops the program when you hit esc
    keyboard.wait('q')
    logger.info('Exiting ...')

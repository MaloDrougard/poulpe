import keyboard  
from myglobal import logger
from arduinocomm import send_cmd

simplecmd = {
    'i': '/info'
}

keycmd = {
    '8': '/setpompe?p=0&t={param}',
    '6': '/setpompe?p=1&t={param}',
    '2': '/setpompe?p=2&t={param}',
    '4': '/setpompe?p=3&t={param}',
}

keyparam = {
    '5':'16',
    '7':'4',
    '9':'32',
    '1':'128',
    '3':'256'
  }

minimal_time = 0.25    

last_cmds = []


def records_cmds(cmd):
    global last_cmds 
    if len(last_cmds) >= 3:
        last_cmds.pop(0)
          
    last_cmds.append(str(cmd))
    if last_cmds == ['6','6','6']:
        logger.warning("666")
        last_cmds = []
    
    logger.info(last_cmds)    
    

def hotkey_callback_generator(key, command, param = None, dummy = False):
    if param:
        command = command.replace("{param}", str(param))    
    def new_callback():
        records_cmds(key)
        logger.info(f"trigger command: {command}")
        if not dummy: 
            send_cmd(command)
    
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

import myglobal
from myglobal import logger
import arduinocomm
from arduinocomm import send_cmd
import json
import sched
import time

max_duration = 60 * 5


effect_cmd = {
    'ON': '/setpompe?p={param}&t=' + str(max_duration), # Not infinit time
    'OFF': '/setpompe?p={param}&t=0'
   
}
#  command = command.replace("{param}", str(param))  


def callback_generator(command):
    
    def new_callback():
        logger.info(f"trigger command: {command}")
        send_cmd(command)
    
    return new_callback

class Partition:
    def __init__(self, d):
        self.instrument = None
        self.timecodes = None
        self.cmdmap = None
        self.scheduler = None
        self.__dict__ = d
        # check if the needed member are there:
        if self.instrument is None:
            logger.warning(f"instrument should be present in partition!")
        if self.timecodes == None:
            logger.warning(f"timecode should be present in partion!")
    
        self.prepare_cmdmap()
        self.prepare_scheduler()

    
    def __str__(self):
        return json.dumps(self.__dict__, indent=4)
    
    # effect -> arduino command
    def prepare_cmdmap(self):
        self.cmdmap = {}
        for effect, cmd in effect_cmd.items():
            self.cmdmap[effect] = cmd.replace("{param}", str(self.instrument))  
    
    # schedul a effect for a given time    
    def prepare_scheduler(self):
        # Create a scheduler instance
        self.scheduler = sched.scheduler(time.time, time.sleep)
        for timecode, effect in self.timecodes.items():
            logger.info(f"add scheduler: pompe: {self.instrument}, time:{timecode}, effect:{effect}")
            self.scheduler.enter(float(timecode),1, callback_generator(self.cmdmap[effect]))            


    def play(self):
        self.scheduler.run()


def read_json_to_partition(file_path):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
    
    except Exception as e:
        logger.error(f"Error reading JSON file: {e}")
        return None
    
    return Partition(data)
 



if __name__ == "__main__":
    
    logger.info("start ...")
    # setup the arduino serial connection -> needed to communicate with arduino
    arduinocomm.setup()

    dir = myglobal.partition_folder()
    partition = read_json_to_partition(myglobal.partition_folder() / "pompe1.json")
    
    partition.play()

    arduinocomm.setdown()
    logger.info('Exiting ...')

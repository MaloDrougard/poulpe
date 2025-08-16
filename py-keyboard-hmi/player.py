import myglobal
from myglobal import logger
import arduinocomm
from arduinocomm import send_cmd
import json
import sched
import time
from pathlib import Path

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
    def __init__(self, filepath):
        self.filepath = filepath
        self.instrument = None
        self.timecodes = None
        self.cmdmap = None
        self.read_json(self.filepath)
        self.prepare_cmdmap()

    
    def __str__(self):
        return json.dumps(self.__dict__, indent=4)

    def read_json(self, filepath: Path):
        try:
            with open(self.filepath, 'r') as file:
                data = json.load(file)
                self.instrument = data['instrument']   
                self.timecodes = data['timecodes']
    
        except Exception as e:
            logger.error(f"Error reading JSON file: {e}")
            return None

    
    # effect -> arduino command
    def prepare_cmdmap(self):
        self.cmdmap = {}
        for effect, cmd in effect_cmd.items():
            self.cmdmap[effect] = cmd.replace("{param}", str(self.instrument))  
    
    # schedul a effect for a given time    
    def add_to_scheduler(self, scheduler):
        # Create a scheduler instance
        for timecode, effect in self.timecodes.items():
            logger.info(f"add scheduler: pompe: {self.instrument}, time:{timecode}, effect:{effect}")
            scheduler.enter(float(timecode),1, callback_generator(self.cmdmap[effect]))            



class Choral:
    
    def __init__(self, directory):
        self.directory = directory
        self.partitions = []
        
        self.parse_dir(directory)
        self.scheduler = sched.scheduler(time.time, time.sleep)
        self.prepare_scheduler()
        
    def parse_dir(self, directory):
        for filepath in Path(directory).glob("*.json"):
            logger.info(f"Parsing partition file: {filepath}")
            partition = Partition(filepath)
            self.partitions.append(partition)
    
    def prepare_scheduler(self):
        for p in self.partitions:
            p.add_to_scheduler(self.scheduler)
        
    def play(self):
        self.scheduler.run()

    



if __name__ == "__main__":
    
    logger.info("start ...")
    # setup the arduino serial connection -> needed to communicate with arduino
    arduinocomm.setup()

    dir = myglobal.partition_folder()
    
    choral = Choral(dir)
    choral.play()

    arduinocomm.setdown()
    logger.info('Exiting ...')

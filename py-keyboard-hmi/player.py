import myglobal
from myglobal import logger
import arduinocomm
from arduinocomm import send_cmd
import json
import sched
import time
from pathlib import Path
import csv

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


def csv_to_json_partition(filepath, output_dir = None, char_to_effect = {"x": "ON", "":"OFF"}):
    """ Creating multiple json partion from a csv file
    """
    logger.info(f"starting the creation of partion base on the csv file: {filepath}")
    csv_file = open(filepath, mode='r') 
    csv_reader = csv.DictReader(csv_file)
    
    for line in csv_reader:
        
        partition_json = {}

        cell_duration = float(line["cell_duration"])
        del line["cell_duration"]
        
        partition_json["description"] = line["description"]
        del line["description"]
           
        instrument = line["instrument"]
        partition_json["instrument"] = instrument
        del line["instrument"]
            
        timecodes = {}
        previous = None
        for timecode, effect in line.items():
            if previous == None or previous != effect:
                timecodes[str(float(timecode)*cell_duration)] = char_to_effect[effect]
            previous = effect
        partition_json["timecodes"] = timecodes
        
        output_filepath = Path(filepath).with_name(f"{Path(filepath).stem}-{instrument}.json")
        if output_dir:
            output_filepath = Path(output_dir) / output_filepath.name

        logger.info(f"creating a new file {output_filepath}")
        
        with open(output_filepath, 'w') as json_file:
            json.dump(partition_json, json_file, indent=4)
    
    csv_file.close()
            



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
    
    def __init__(self):
        self.cleanup()
        
    def cleanup(self):
        self.json_partitions = []
        self.scheduler = sched.scheduler(time.time, time.sleep)
    
    def setup_from_csv(self, filepath):
        """ We first convert the file to multiple json file and then use it to play the csv
        """
        
        # cleaning and creat temp dir for json file
        temp_dir = Path(filepath).parent / "temp"
        if temp_dir.exists():
            for file in temp_dir.iterdir():
                file.unlink()
            temp_dir.rmdir() # must be empty
        temp_dir.mkdir(exist_ok=True)
        
        # using the json file to create the scheduler
        csv_to_json_partition(filepath, temp_dir)
        self.setup_from_dir(temp_dir)
    
    
    def setup_from_dir(self, directory):
        """ setup partion parsing a directory looking for json file
        """
        self.cleanup()
        self.parse_dir(directory)
        self.prepare_scheduler()
        
    def parse_dir(self, directory):
        for filepath in Path(directory).glob("*.json"):
            logger.info(f"Parsing partition file: {filepath}")
            partition = Partition(filepath)
            self.json_partitions.append(partition)
    
    def prepare_scheduler(self):
        for p in self.json_partitions:
            p.add_to_scheduler(self.scheduler)
        
    def play(self):
        self.scheduler.run()



def interactive():
    dir = myglobal.partition_folder() / "csvs"
    
    def get_and_print_available():
        csv_files = list(Path(dir).glob("*.csv"))
        if not csv_files:
            logger.error("No CSV files found in the directory.")
            return None
        print("Available CSV files:")
        for idx, file in enumerate(csv_files, start=1):
            print(f"{idx}: {file.name}")     
        return csv_files
    
    while True:
        csv_files = get_and_print_available()
        choice = input("Enter the number of the CSV file to play (or 'q' to quit): ")
        
        if choice.lower() == 'q':
            logger.info("Exiting interactive mode.")
            break
        
        try:
            selected_file = csv_files[int(choice) - 1]
        except (ValueError, IndexError):
            logger.error("Invalid selection. Please try again.")
            continue
        
        choral = Choral()
        choral.setup_from_csv(selected_file)
        choral.play()



if __name__ == "__main__":
    
    logger.info("start ...")
    # setup the arduino serial connection -> needed to communicate with arduino
    
    
    arduinocomm.setup()

    time.sleep(1)  # wait for the serial connection to be established
    
    interactive()
    
    arduinocomm.setdown()
    logger.info('Exiting ...')

import re
import argparse
from communication import Communication
from navigation import Navigation
import time
import json
import sys


class Bot:
    def __init__(self, teamname, pitstop_num, comms):
        self.teamname = teamname
        self.pitstop_num = pitstop_num
        self.start_num = -1
        self.teammates = []
        self.comms = comms
        self.comms.subscriber.on_message = self.message_handler
        self.nav = Navigation()
    
    def message_handler(self, client, userdata, msg):
        topic = msg.topic
        msg = str(msg.payload.decode('utf-8', 'ignore'))

        if re.match('lab5/discovery', topic):
            self.add_teammate(topic, msg)
        
        if re.match('lab5/consensus/pitstop', topic):
            self.comms.populate_pitstops(topic, msg)
        
        # Fill in the remaining message handling here

        if re.match(f'lab5/{self.teamname}/in', topic):
            if msg == 'init':
                self.start_num = self.nav.move_to_start(self.pitstop_num, self.comms.pitstop_coords, 
                    self.comms.start_coords)
            # Fill in message handling for other cases in this topic.

                
    def add_teammate(self, topic, msg):
        """Add teammate to self.teammates."""

    def loop(self):
        self.comms.subscribe_all()
        while True:
            self.comms.publish_all()
            time.sleep(1)


class Leader(Bot):
    """Class for the leader bot."""
    def message_handler(self, client, userdata, msg):
        super().message_handler(client, userdata, msg)
        topic = msg.topic
        msg = str(msg.payload.decode('utf-8', 'ignore'))

        if re.match('lab5/consensus/understanding/ok', topic):
            self.comms.verify_understanding(topic, msg, self.teammates)
        
        # Fill in message handling for /lab5/race/go here

def main():
    """To use this module, if you're the leader then run:
    
    `python3 bot.py <teamname> <pitstop_number> --leader`
    Otherwise, run:
    `python3 bot.py <teamname> <pitstop_number>`"""

    parser = argparse.ArgumentParser()
    parser.add_argument("teamname", type=str, help="your teamname")
    parser.add_argument('pitstop_num', type=int, help="your pitstop number")
    parser.add_argument("-l", "--leader", help="are you the leader?",
                        action="store_true")
    args = parser.parse_args()

     if (args.leader):
        comms = LeaderCommunication(args.teamname)
        bot = Leader(args.teamname, args.pitstop_num, comms)
    else:
        comms = Communication(args.teamname)
        bot = Bot(args.teamname, args.pitstop_num, comms)
    bot.loop()
    


if __name__ == '__main__':
    main()

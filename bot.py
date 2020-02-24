import re
from communication import Communication
from navigation import Navigation
import time
import json
import sys


class Bot(object):
    def __init__(self, teamname, pitstop_num, is_leader=False):
        self.teamname = teamname
        self.pitstop_num = pitstop_num
        self.start_num = -1
        self.is_leader = is_leader
        self.teammates = []
        self.comms = Communication(teamname, is_leader)
        self.comms.subscriber.on_message = self.message_handler
        self.nav = Navigation()
    
    def message_handler(self, client, userdata, msg):
        topic = msg.topic
        msg = str(msg.payload.decode('utf-8', 'ignore'))

        if re.match('lab5/discovery', topic):
            self.comms.add_teammate(topic, msg)
        
        if re.match('lab5/consensus/pitstop', topic):
            self.comms.populate_pitstops(topic, msg)
        
        # Fill in the remaining message handling here

        if re.match(f'lab5/{self.teamname}/in', topic):
            if msg == 'init':
                self.start_num = self.nav.move_to_start(self.pitstop_num, self.comms.pitstop_coords, 
                    self.comms.start_coords)
            # Fill in message handling for other cases in this topic.
        
        # Leader checks that every team is verified
        if self.is_leader and re.match('lab5/consensus/understanding/ok', topic):
            self.comms.leader_verify_understanding(topic, msg, self.teammates)

        # Add the other leader message handling
                
    def add_teammate(self, topic, msg):
        """Add teammates."""



    def loop(self):
        self.comms.subscribe_all()
        while True:
            if (self.nav.at_goal()):
                ...
            self.comms.publish_all()
            time.sleep(1)

def main():
    teamname, is_leader, pnum =\
         str(sys.argv[1]), bool(sys.argv[2]), int(sys.argv[3])
    bot = Bot(teamname, pnum, is_leader)
    bot.loop()
    


if __name__ == '__main__':
    main()
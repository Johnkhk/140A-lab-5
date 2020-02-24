import re
from communication import Communication
from navigation import Navigation
import time
import json


class Bot(object):
    def __init__(self, teamname, is_leader=False):
        self.teamname = teamname
        self.is_leader = is_leader
        self.teammates = []
        self.comms = Communication(teamname)
        self.comms.subscriber.on_message = self.message_handler
        self.nav = Navigation()
    
    def message_handler(self, client, userdata, msg):
        topic = msg.topic
        msg = str(msg.payload.decode('utf-8', 'ignore'))

        if re.match('lab5/discovery', topic):
            self.comms.add_teammate(msg)
        
        if re.match('lab5/consensus/pitstop', topic):
            self.comms.populate_pitstops(topic, msg)
        
        # Fill in all the message handling here

        if re.match(f'lab5/{self.teamname}/in', topic):
            if msg == 'init':
                self.nav.move_to_start()
            # Fill in message handling for other cases in this topic.
        if re.match('lab5/consensus/understanding/ok', topic):
            self.comms.leader_verify_understanding(topic, msg)
                
    def add_teammate(self, topic, msg):
        """Add teammates."""
        ...

    def game_loop(self):
        self.comms.subscribe_all()
        while True:
            if (self.nav.at_goal()):
                ...
            self.comms.publish_all()
            time.sleep(1)

def main():
    with Team('pikachu') as my_team, Team('raichu', is_leader=True) as your_team:
        my_team.subscribe_coordinates()
        your_team.subscribe_coordinates()

        my_team.subscriber.subscribe('lab5/discovery')
        your_team.subscriber.subscribe('lab5/discovery')
        while True:
            my_team.publish_discovery()
            my_team.consensus_understand()
            
            your_team.publish_discovery()
            your_team.consensus_understand()            
            time.sleep(1)


if __name__ == '__main__':
    main()
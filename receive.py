import time
from spade.agent import Agent
from spade.behaviour import OneShotBehaviour, CyclicBehaviour
from spade.message import Message
from spade.template import Template


class ReceiverAgent(Agent):

    class RecvBehav(CyclicBehaviour):
        async def run(self):
            print("RecvBehav running")
            msg_rev = await self.receive(1000000) # wait for a message for 10 seconds
            if msg_rev.body:      
                print("Message received with content: ", format(msg_rev))
                print("Message received with metadata: ", format(msg_rev.metadata))
                print("Message received with Product ", format(msg_rev.metadata['product']))
                    
          
    
    async def setup(self):
        recv_behav =self.RecvBehav()
        template = Template()
        self.add_behaviour(recv_behav, template)



if __name__ == "__main__":
    receiveragent = ReceiverAgent("daniel1@talk.tcoop.org", "tcoop#2021")
    future = receiveragent.start()
    future.result() # wait for receiver agent to be prepared.

    while receiveragent.is_alive():
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            receiveragent.stop()
            break
    print("Agents finished")

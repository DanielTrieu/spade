import time
from spade.agent import Agent
from spade.behaviour import OneShotBehaviour
from spade.message import Message
from spade.template import Template


class SenderAgent(Agent):
    class InformBehav(OneShotBehaviour):
        async def run(self ):
            print("InformBehav running")
            msg = Message(to=self.get("to_agent"))    # Instantiate the message
            metadata= self.get("metadata")
            for key, value in metadata.items():
                msg.set_metadata(key, value)
            msg.set_metadata("performative", "inform")  # Set the "inform" FIPA performative
            msg.body = "Hello World"                    # Set the message content

            await self.send(msg)
            print("Message sent!")

            # stop agent from behaviour
            #await self.agent.stop()
        
    
    async def setup(self):
        print("Buyer agent started")
        inform_behav = self.InformBehav()
        self.add_behaviour(inform_behav)



if __name__ == "__main__":
    sender = SenderAgent("daniel@talk.tcoop.org", "tcoop#2021")
    sender.set("to_agent", "daniel1@talk.tcoop.org")
    sender.set("metadata", {"product":"carrot", "price":"34"})
    future =sender.start()
    future.result()

    while sender.is_alive():
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            senderagent.stop()
            break
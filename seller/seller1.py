import time
from spade.agent import Agent
from spade.behaviour import OneShotBehaviour, CyclicBehaviour
from spade.message import Message
from spade.template import Template


class SellerAgent(Agent):

    class RecvBehav(CyclicBehaviour):
        async def run(self):
            print("RecvBehav running")
            msg_recv = await self.receive(1000000) # wait for a message for 10 seconds
            print("Receive", msg_recv)
            if msg_recv.metadata['msg_type'] =="CFP": # CFP: call for proposal
                reply_data = self.get("proposal_data")
                sender = str(msg_recv.sender)
                msg_rep =Message(to=sender)
                msg_rep.set_metadata("performative", "inform")
                
                for key, value in reply_data.items():
                    msg_rep.set_metadata(key, value)
                
                await self.send(msg_rep)

    
    class Propose(OneShotBehaviour):
        async def run(self ):
            print("InformBehav running")
            msg = Message(to=self.get("to_agent"))    # Instantiate the message
            metadata= self.get("metadata")
            for key, value in metadata.items():
                msg.set_metadata(key, value)
            msg.set_metadata("performative", "inform")  # Set the "inform" FIPA performative
            #msg.body = "Hello World"                    # Set the message content

            await self.send(msg)
            print("Message sent!")

            # stop agent from behaviour
            #await self.agent.stop()

    async def setup(self):
        recv_behav =self.RecvBehav()
        template = Template()
        template.set_metadata("performative", "inform")
        self.add_behaviour(recv_behav, template)



if __name__ == "__main__":
    Seller = SellerAgent("seller1@talk.tcoop.org", "tcoop#2021")
    Seller.set("proposal_data",{"product":"carrot", "price":"34", "quantity":"50"})
    future = Seller.start()
    future.result() # wait for receiver agent to be prepared.

    while Seller.is_alive():
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            Seller.stop()
            break
    print("Agents finished")

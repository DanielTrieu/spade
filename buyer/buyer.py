import time
from spade.agent import Agent
from spade.behaviour import OneShotBehaviour,CyclicBehaviour
from spade.message import Message
from spade.template import Template


class RecvBehav(CyclicBehaviour):
        async def run(self):
            print("RecvBehav running")
            msg_rev = await self.receive(100000) # wait for a message for 10 seconds
            if msg_rev:      
                print("Message received with metadata: ", format(msg_rev.metadata))
            if msg_rev.body=="buy":
                await self.agent.run_CFP()

          

class BuyerAgent(Agent):

    class Call_for_proposal(OneShotBehaviour):
        async def run(self):
            print("Call_for_proposal running")
            msg = Message(to=self.get("to_agent"))    # Instantiate the message
            metadata= self.get("metadata")
            for key, value in metadata.items():
                msg.set_metadata(key, value)
            msg.set_metadata("performative", "inform")  # Set the "inform" FIPA performative
            msg.set_metadata("msg_type","CFP")
            #msg.body = "Hello World"                    # Set the message content

            await self.send(msg)
            print("Message sent!")


    class proposal(OneShotBehaviour):
        async def run(self):
            print("Call_for_proposal running")
            msg = Message(to=self.get("to_agent"))    # Instantiate the message
            metadata= self.get("metadata")
            for key, value in metadata.items():
                msg.set_metadata(key, value)
            msg.set_metadata("performative", "inform")  # Set the "inform" FIPA performative
            msg.set_metadata("msg_type","CFP")
            #msg.body = "Hello World"                    # Set the message content

            await self.send(msg)
            print("Message sent!")        






    
    async def run_CFP(self):
            self.add_behaviour(self.Call_for_proposal())


    async def setup(self):
        recv_behav =RecvBehav()
        template = Template()
        #template.set_metadata("performative", "inform")
        self.add_behaviour(recv_behav, template)
        print("Buyer agent started")
        await self.run_CFP()
        
        

if __name__ == "__main__":
    seller_list =["seller1@talk.tcoop.org", "seller2@talk.tcoop.org"]
    buy_product ={ "product":"carrot", "quantity":"12"}

    
    Buyer = BuyerAgent("buyer@talk.tcoop.org", "tcoop#2021")
    Buyer.set("to_agent", "seller1@talk.tcoop.org")
    Buyer.set("metadata", {"product":"carrot", "price":"34"})
    future =Buyer.start()
    Buyer.web.start(hostname="127.0.0.1", port="10000")

    future.result()
    
    while Buyer.is_alive():
        try:
            time.sleep(1)
            #for behav in Buyer.behaviours: print(behav )
            #print (recv_behav in Buyer.behaviours)
        except KeyboardInterrupt:
            senderagent.stop()
            break
import time
from spade.agent import Agent
from spade.behaviour import OneShotBehaviour,CyclicBehaviour
from spade.message import Message
from spade.template import Template

         

class BuyerAgent(Agent):
     
    class Handler(CyclicBehaviour):
        async def run(self):
           
            msg_rev = await self.receive(100000) # wait for a message for 10 seconds
            if msg_rev:
                print()      
                print("Message received  ", msg_rev)
                print()
                #print("sender:", msg_rev.sender)
                #print("to:", msg_rev.to)
                #print("Thread:", msg_rev.thread)
            if msg_rev.body=="buy":
                
                await self.agent.run_CFP()
            
            if msg_rev.get_metadata('performative')=="propose":
                
                self.set("seller", str(msg_rev.sender))
                await self.agent.run_accept_proposal()

            if msg_rev.get_metadata('performative')=="confirm":
                to_agent ="daniel@talk.tcoop.org"
                msg = Message(to=to_agent)
                msg.body = "receive confirm from "+((str(msg_rev.sender)).split("/"))[0]+" : "+str(msg_rev.metadata)
                await self.send(msg)
                


    class CFP(OneShotBehaviour):
        async def run(self):
            print("Call_for_proposal running")
            seller_list= self.get("seller_list")
            for seller in seller_list:
            
                msg = Message(to=seller)    # Instantiate the message
                metadata= self.get("cfp_data")
                for key, value in metadata.items():
                    msg.set_metadata(key, value)
                msg.set_metadata("performative", "cfp")  # Set the "inform" FIPA performative
                #msg.body = "Hello World"                    # Set the message content

                await self.send(msg)
                time.sleep(1)
                print("CFP Message sent!", seller)


    class Accept_proposal(OneShotBehaviour):
        async def run(self):
            print("Accept proposal running")
            seller = self.get("seller")
            print()
            msg = Message(to=seller)    # Instantiate the message
            metadata= self.get("accept_proposal_data")
            for key, value in metadata.items():
                msg.set_metadata(key, value)
            msg.set_metadata("performative", "accept-proposal")  # Set the "inform" FIPA performative
            #msg.body = "Hello World"                    # Set the message content

            await self.send(msg)
            print("Accept proposal sent to", seller )        
    
    async def run_CFP(self):
            self.add_behaviour(self.CFP())

    async def run_accept_proposal(self):
            self.add_behaviour(self.Accept_proposal())


    async def setup(self):
        template = Template()
        #template.set_metadata("performative", "inform")
        self.add_behaviour(self.Handler(), template)
        print("Buyer agent started")
       
        

if __name__ == "__main__":
    seller_list =["seller1@talk.tcoop.org", "seller2@talk.tcoop.org"]
    buy_product ={ "product":"carrot", "quantity":"12"}

    
    Buyer = BuyerAgent("buyer@talk.tcoop.org", "tcoop#2021")
    Buyer.set("seller_list",["seller1@talk.tcoop.org", "seller2@talk.tcoop.org"])
    Buyer.set("to_agent", "seller1@talk.tcoop.org/ddf")
    Buyer.set("buy_data", {"product":"carrot", "quantity":"5"})
    Buyer.set("cfp_data", {"product":"carrot", "quantity":"5"})
    Buyer.set("accept_proposal_data", {"product":"carrot", "price":"34", "quantity":"5"} )
    future =Buyer.start()
    Buyer.web.start(hostname="127.0.0.1", port="10000")

    future.result()
    
    while Buyer.is_alive():
        try:
            time.sleep(3)
            #for behav in Buyer.behaviours: print(behav )
            #print (recv_behav in Buyer.behaviours)
        except KeyboardInterrupt:
            senderagent.stop()
            break
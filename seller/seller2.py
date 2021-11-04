import time
from spade.agent import Agent
from spade.behaviour import OneShotBehaviour, CyclicBehaviour
from spade.message import Message
from spade.template import Template






class SellerAgent(Agent):

    class Handler(CyclicBehaviour):
        async def run(self):
            
            msg_recv = await self.receive(1000000) # wait for a message for 10 seconds
            print()
            print("Receive message", msg_recv)
            print()
            performative = msg_recv.metadata['performative']
            
            if performative=="cfp":
                time.sleep(1)
                await self.agent.run_propose()
            elif performative== "accept-proposal":
                time.sleep(1)
                await self.agent.run_confirm()
                sell_data = self.get('sell_data')
                new_quantity =  int(sell_data['quantity']) - int(msg_recv.metadata['quantity'])
                sell_data["quantity"]= str(new_quantity )
                self.set('sell_data',sell_data)
                print ('new quantity', sell_data['quantity'])


            else:
                print("no matching")


    class Propose(OneShotBehaviour):
        async def run(self ):
            #print("Propose running")
            to_agent = self.get("to_agent")
            msg = Message(to=to_agent)    # Instantiate the message
            metadata= self.get("sell_data")
            for key, value in metadata.items():
                msg.set_metadata(key, value)
            msg.set_metadata("performative", "propose")  # Set the "inform" FIPA performative
            #msg.body = "Hello World"                    # Set the message content

            await self.send(msg)
            print("Propose sent to", to_agent  )

            # stop agent from behaviour
            #await self.agent.stop()

    
    
    class Confirm(OneShotBehaviour):
        async def run(self ):
            #print("confirm request")
            to_agent = self.get("to_agent")
            msg = Message(to=to_agent)    # Instantiate the message
            metadata= self.get("confirm_data")
            for key, value in metadata.items():
                msg.set_metadata(key, value)
            msg.set_metadata("performative", "confirm")  # Set the "confirm" FIPA performative
            #msg.body = "Hello World"                    # Set the message content

            await self.send(msg)
            print("confirm request sent to", to_agent)

            # stop agent from behaviour
            #await self.agent.stop()    


    
        
    async def run_propose(self):
            self.add_behaviour(self.Propose())

    async def run_confirm(self):
            self.add_behaviour(self.Confirm())
    
    async def setup(self):
        template = Template()
        #template.set_metadata("performative", "inform")
        self.add_behaviour(self.Handler(), template)



if __name__ == "__main__":
    Seller = SellerAgent("seller2@talk.tcoop.org", "tcoop#2021")
    Seller.set("to_agent", "buyer@talk.tcoop.org/fjfe")
    Seller.set("sell_data",{"product":"carrot", "price":"34", "quantity":"50"})
    Seller.set("confirm_data",{"product":"carrot", "price":"34", "quantity":"20"})
    future = Seller.start()
    future.result() # wait for receiver agent to be prepared.
    print("Seller 2 running")

    while Seller.is_alive():
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            Seller.stop()
            break
    print("Agents finished")

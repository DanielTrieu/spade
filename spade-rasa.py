import time
import asyncio
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.template import Template
from spade.message import Message
import rasa.core.agent as rasaAgent
import asyncio


async def rasabot(message):
        responses = await r_agent.handle_text(message)
        reply ="sorry no reply"
        for response in responses:
            for response_type, value in response.items():
                if response_type == "text":
                    reply=value
        return reply  
r_agent = rasaAgent.create_agent('/home/daniel/rasa/test/models/20211103-151327.tar.gz')

class DummyAgent(Agent):
    class MyBehav(CyclicBehaviour):
        async def on_start(self):
            print("Starting behaviour . . .")
            

        async def run(self):
            
            msg_rev = await self.receive(timeout=10000) # wait for a message for 10 seconds
            if msg_rev.body:        
                    print("Message received with content:", msg_rev.body)
                    reply_message = await rasabot(msg_rev.body)
                    print(reply_message)
                    sender = str(msg_rev.sender)
                    msg_sent =Message(to=sender)
                    msg_sent.body= reply_message
                    await self.send(msg_sent)

    async def setup(self):
        print("Agent starting . . .")
        b = self.MyBehav()
        template = Template()
        self.add_behaviour(b,template)

if __name__ == "__main__":
    dummy = DummyAgent("daniel1@talk.tcoop.org", "tcoop#2021")
    future = dummy.start()
    future.result()

    print("Wait until user interrupts with ctrl+C")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Stopping...")
    dummy.stop()
import asyncio


from dotenv import load_dotenv
from livekit.agents import AutoSubscribe, JobContext, WorkerOptions, cli, llm, ChatContext, ChatMessage
#from livekit.agents.chat_context import ChatContext, ChatMessage
from livekit.agents.voice import Agent
from livekit.plugins import openai, silero



load_dotenv()

async def entrypoint(ctx: JobContext):
    #can add context to start AI voice assistant
    initial_ctx = llm.ChatContext()
    initial_ctx.add_message(
        role="system",
        #description/format of how we want this assistant to work/respond
        content=["You are a voice assistant created by LiveKit. Your interface with users will be voice. "
                "You should use short and concise responses, and avoiding usage of unpronouncable punctuation. "
                "Greet the user by saying: 'Hey, how can I help you today!'. "]
            
    )
    #specifying that we just want to connect to the audio tracks
    await ctx.connect(auto_subscribe=AutoSubscribe.AUDIO_ONLY)
    
    assistant = Agent(
        #voice activity detection, what we're using to detect if the user is speaking or not, 
        #so we know when to cut them off and send message over to Ai
        vad=silero.VAD.load(),
        #stt=speech-to-text
        stt=openai.STT(),
        llm=openai.LLM(),
        #text-to-speech
        tts=openai.TTS(),
        chat_ctx=initial_ctx,
        instructions="You are a voice assistant created by LiveKit. Your interface with users will be voice. "
                "You should use short and concise responses, and avoiding usage of unpronouncable punctuation. "
                "Greet the user by saying: 'Hey, how can I help you today!'. "
    )

    #assistants connect to a room
    #assistant.run(ctx.room)

    #wait one second
    #await asyncio.sleep(1)
    #allow_interruptions allows us to interrupt welcome message with anything we want
    #await assistant.say("Hey, how can I help you today!", allow_interruptions=True) 
    #await assistant.handle_text("Hey, how can I help you today!", stream=ctx.room) 



if __name__=="__main__":
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint))
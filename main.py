import asyncio
from tools.agentUtil import run
from utility.speech_rec import recognize_speech

async def main():
    input = ''
    while True:
        input = await recognize_speech()
        if 'exit' in input.lower(): break
        else: 
            print(input)
            ret = run(input)

asyncio.run(main())
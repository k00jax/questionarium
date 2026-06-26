import asyncio, sys
if sys.platform == 'win32': asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
import edge_tts

async def test():
    voices = ['en-US-AndrewNeural','en-US-ChristopherNeural','en-US-EricNeural','en-US-GuyNeural','en-US-RogerNeural']
    for v in voices:
        name = v.replace('en-US-','').replace('Neural','')
        print(f'Generating {v}...')
        c = edge_tts.Communicate(f'Hi, my name is {name}. This is a voice test.', v)
        await c.save(f'test_{name}.mp3')
asyncio.run(test())
print('Done! Play the test files.')

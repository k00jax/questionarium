#!/usr/bin/env python3
"""Pre-generate all audio files for The Questionarium using edge-tts (Andrew voice)."""
import asyncio, sys, json, os
from pathlib import Path

# Fix for Windows: aiodns needs SelectorEventLoop
if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

import edge_tts

AUDIO_DIR = Path(__file__).parent / "audio"
VOICE = "en-US-ChristopherNeural"

scenarios = [
  {
    "category": "FAIRNESS LAB",
    "question": "A wizard offers to make you THE BEST at everything... but everyone else in the world becomes slightly worse at everything they do. Do you take the deal?",
    "answers": [
      {"letter":"A","text":"Take the deal! Being the best at everything sounds amazing.","msg":"You know what you want and you go for it. That's powerful.","thought":"If everyone else got worse, would 'the best' still mean anything? Is being great only special because other people are great too?"},
      {"letter":"B","text":"No way. I don't want to make everyone else worse just so I can shine.","msg":"You care about other people, even strangers you'll never meet. That's a superpower all by itself.","thought":"Would it still be the right choice if one of those people was your best friend? What if it was someone you don't like?"},
      {"letter":"C","text":"Can I be the best at just ONE thing instead? Like, really good at making pizza?","msg":"You found a third option! That's what philosophers do — they question the question itself.","thought":"Why did the wizard only give two choices? In real life, are most choices really just A or B?"},
      {"letter":"D","text":"What does 'best' even mean if everyone else got worse? That's not being best, that's just everyone else being worse.","msg":"You looked at the words themselves. Before answering, you asked: what do we actually mean?","thought":"How many arguments happen because people mean different things by the same word? Fair. Best. Good. What do those even mean?"}
    ]
  },
  {
    "category": "REALITY CHECK",
    "question": "Your friend says they have an invisible pet dragon. It can breathe fire... but the fire is ALSO invisible. How would you figure out if the dragon is actually real?",
    "answers": [
      {"letter":"A","text":"Try to touch it! If I can feel it, it's real, even if I can't see it.","msg":"You trust what you can touch and feel. That's called empiricism — learning through your senses. It's how science started!","thought":"But what about things you can't touch, like gravity or love or thoughts? Are those real?"},
      {"letter":"B","text":"Throw water on it! If there's an invisible dragon there, the water would splash on SOMETHING invisible.","msg":"You invented a test! You didn't just believe or disbelieve — you looked for evidence. Scientists do this every day.","thought":"What if the dragon was also waterproof? How many tests would you need before you decided the dragon wasn't real?"},
      {"letter":"C","text":"If you can't prove it's NOT real... maybe it IS real? I believe my friend.","msg":"You chose to believe your friend. Trust is one of the most important things humans have.","thought":"But should we always believe people we trust? What if your friend truly believes the dragon is real — does that make it real?"},
      {"letter":"D","text":"What if the dragon only exists when someone is thinking about it? Like, it's real in our imagination?","msg":"You're asking whether something can be real in one way but not another. That's a VERY deep question.","thought":"Is a story real? Is a dream real? Is a feeling real? Are there different kinds of real?"}
    ]
  },
  {
    "category": "HAPPINESS DILEMMA",
    "question": "If you could press a button that makes EVERYONE in the world happy forever... but nobody would EVER be able to change their mind about ANYTHING again. Would you press it?",
    "answers": [
      {"letter":"A","text":"Press it! Happy forever for everyone sounds like the best possible world.","msg":"You want everyone to be happy. That's beautiful. You're asking what philosophers call the greatest good.","thought":"But if nobody can change their mind, how would we learn new things? Would we be stuck with whatever we believed on button-press day forever?"},
      {"letter":"B","text":"DON'T press it. Changing your mind is how you grow. Being stuck forever sounds like a prison, even a happy one.","msg":"You value freedom and growth over comfort. That's a brave choice — you'd rather face hard things than be trapped in easy ones.","thought":"Is happiness worth anything if you didn't choose it? If a robot makes you smile by zapping your brain, is that real happiness?"},
      {"letter":"C","text":"Can I press it HALFWAY? Like, everybody gets a happiness boost but can still learn and grow?","msg":"You want both! Happiness AND growth. You're looking for the middle path.","thought":"Are there things in life where you can't have both? Times when you have to choose between feeling good and doing the right thing?"},
      {"letter":"D","text":"Are people REALLY happy if they can't choose to be sad? Maybe you need sad to understand happy.","msg":"You asked whether happiness makes sense without sadness. That's what philosophers call the problem of contrast.","thought":"Can you know what warm means if you've never felt cold? What if ALL feelings need their opposite to make sense?"}
    ]
  },
  {
    "category": "FRIENDSHIP LAB",
    "question": "Your BEST FRIEND moves away. You get a robot that looks and acts EXACTLY like them. Is the robot actually your friend?",
    "answers": [
      {"letter":"A","text":"Yes! If they act the same and make me feel the same, then they ARE the same. That's what matters.","msg":"You care about what something DOES, not what it's made of. That's called functionalism — if it quacks like a duck...","thought":"But what if you found out your REAL best friend had been replaced by a robot and you never knew? Would it matter?"},
      {"letter":"B","text":"No. A real friend has to be a real PERSON, with their own thoughts and feelings. A robot is just pretending.","msg":"For you, friendship needs something deeper than just acting right. It needs a real person on the other side.","thought":"How do you know OTHER PEOPLE have real thoughts and feelings? You can't see inside their heads. What makes you sure your human friends aren't pretending too?"},
      {"letter":"C","text":"The robot is a DIFFERENT kind of friend. Like how a pet is different from a person friend.","msg":"You invented a whole new category! Not 'friend' or 'not friend' — a third thing. Philosophers call this expanding the frame.","thought":"How many things in life are 'either/or' versus 'a different kind of thing entirely'? What other categories could use a third option?"},
      {"letter":"D","text":"Can I have BOTH friends? The real one for real talks and the robot one for everyday hanging out?","msg":"Why choose when you can have both? You rejected the idea that friendship is a limited resource.","thought":"Is love limited? If you love a second person, do you love the first one less? Or does love multiply?"}
    ]
  },
  {
    "category": "IDENTITY PUZZLE",
    "question": "You bury your favorite sneaker in the backyard. You dig it up 10 YEARS later. It's dirty, faded, and full of holes. Is it the SAME sneaker or a DIFFERENT one?",
    "answers": [
      {"letter":"A","text":"Same sneaker! It's made of the exact same atoms. Nothing was added or removed — well, except the dirt.","msg":"You believe that what something IS comes down to what it's MADE OF. Same stuff equals same thing.","thought":"But humans replace almost ALL their atoms every few years. The you reading this has totally different atoms than the you from seven years ago. Are you a different person?"},
      {"letter":"B","text":"It's a DIFFERENT sneaker. It changed over time. Things are defined by what they're like RIGHT NOW.","msg":"You care about what something is in THIS moment. The past version is gone, and that's okay.","thought":"If you're different now than you were as a baby, are you a different person? When did you stop being 'baby you' and start being 'now you'?"},
      {"letter":"C","text":"It's BOTH. It's the SAME sneaker in a different CONDITION. Like how you're the same person even when you change.","msg":"You found a way to hold two truths at once. The sneaker is the same AND different — and that's not a contradiction.","thought":"What ELSE in life is 'both'? Are you the same person you were yesterday AND a different one? Is change and sameness both true?"},
      {"letter":"D","text":"NEITHER. The REAL sneaker is the MEMORY of wearing it. The physical shoe was never what made it YOUR sneaker.","msg":"You decided that what makes something important isn't its atoms or its condition — it's what it MEANS to you.","thought":"If the meaning is what matters, does anything have meaning without someone to care about it? Would a sneaker be special if nobody remembered it?"}
    ]
  },
  {
    "category": "SECRETS AND PROMISES",
    "question": "A GIANT CHICKEN lands in your yard. It says it will lay GOLDEN EGGS for you forever... but ONLY if you NEVER tell ANYONE. Not even your family. Ever. Do you accept?",
    "answers": [
      {"letter":"A","text":"YES! I'd be rich forever and all I have to do is keep one secret. That's a GREAT deal!","msg":"You saw an opportunity and took it. The cost seemed small compared to the reward.","thought":"But would you feel lonely having a secret that big? If you can't share your amazing life with anyone, is it still amazing?"},
      {"letter":"B","text":"NO. I can't keep a secret that big from my family. Some things matter more than gold.","msg":"You chose connection over riches. The people you love matter more to you than anything money could buy.","thought":"Are there ANY secrets worth keeping from the people you love? What about a surprise party? What makes some secrets okay and others not?"},
      {"letter":"C","text":"Wait — the CHICKEN said I can't tell anyone. But what if the chicken tells people? I never promised the CHICKEN would keep quiet.","msg":"You read the fine print! You found a gap in the rules. That's what lawyers AND philosophers do — they examine the exact words.","thought":"Is following the exact words of a rule the same as doing what the rule MEANT? If someone says don't tell, do they mean don't let anyone find out?"},
      {"letter":"D","text":"What would I even DO with infinite golden eggs? Like, practically? That many eggs sounds like a storage problem.","msg":"You looked past the fantasy and asked: what would this ACTUALLY be like? That's wisdom hiding inside a joke.","thought":"We dream about infinite money or infinite power — but would infinite anything actually make us happy? Or would it just create infinite problems?"}
    ]
  },
  {
    "category": "TRUST PUZZLE",
    "question": "Your teacher says two plus two equals four. Your calculator says two plus two equals four. But a VOICE IN YOUR HEAD says two plus two equals five. Who do you trust?",
    "answers": [
      {"letter":"A","text":"My teacher! They went to school for YEARS to learn math. They probably know what they're talking about.","msg":"You trust experts. That's smart — we can't personally verify everything. Society works because we trust people who know more than us.","thought":"But what if your teacher was wrong about something else? How do you know WHEN to trust experts and when to question them?"},
      {"letter":"B","text":"My calculator! Machines don't make mistakes. They're programmed to be correct.","msg":"You trust tools that are built for accuracy. That makes sense — calculators don't get tired or distracted.","thought":"But who programmed the calculator? A human. And what if the calculator's battery is low and it's making errors? Can you trust a tool without knowing how it works?"},
      {"letter":"C","text":"MYSELF! I have to trust my own brain. If I don't believe what I think, what CAN I believe?","msg":"You believe in your own mind. That's courageous. Self-trust is the foundation of thinking for yourself.","thought":"But have you ever been SURE about something and then found out you were wrong? How do you tell the difference between trusting yourself and being mistaken?"},
      {"letter":"D","text":"I wouldn't trust ANY of them. I'd go get FOUR ACTUAL APPLES and count them myself.","msg":"You went straight to the evidence! You didn't choose who to believe — you chose to FIND OUT. This is the scientific method in action.","thought":"What if you can't test something yourself? What if it's too big, too far away, or already happened? How do you decide what's true when you can't check?"}
    ]
  },
  {
    "category": "SUPERPOWER DILEMMA",
    "question": "You get the power to PAUSE TIME whenever you want. Cool, right? But... while time is paused, ICE CREAM has NO TASTE. Do you still want the power?",
    "answers": [
      {"letter":"A","text":"YES! I'd use it for stuff other than eating. Frozen time is WAY more useful than ice cream.","msg":"You saw the big picture. A minor downside doesn't ruin an amazing power. You're thinking like a chess player.","thought":"But what if using the power too much made you lonely? Being the only moving person in a frozen world... would you eventually miss normal time?"},
      {"letter":"B","text":"NO. What's the point of superpowers if you can't enjoy ICE CREAM? That's a dealbreaker.","msg":"You know what you love and you won't give it up. Small pleasures matter. Joy isn't negotiable.","thought":"Is there a point where you'd trade joy for power? What if the trade was bigger — all food has no taste, but you can fly? Where's your line?"},
      {"letter":"C","text":"I'd only pause time to take NAPS. Naps don't need taste. Checkmate, ice cream curse!","msg":"You found a way to use the power that dodges the downside entirely. Creative problem-solving is its own superpower.","thought":"Are most 'impossible' choices actually hiding a third option? How often do we get stuck in 'either/or' when there's an 'only use it for naps' hiding in plain sight?"},
      {"letter":"D","text":"Can I FAST-FORWARD time instead? Skipping homework and boring stuff sounds WAY better than pausing.","msg":"You didn't just answer the question — you changed it. Why pause when you can fast-forward? That's a whole different superpower.","thought":"If you could skip all the boring parts of life, would you? Or are the boring parts secretly where the important stuff happens?"}
    ]
  }
]

async def gen(text, filename):
    """Generate a single MP3 file."""
    path = AUDIO_DIR / filename
    if path.exists():
        print(f"  SKIP (exists): {filename}")
        return
    communicate = edge_tts.Communicate(text, VOICE)
    await communicate.save(str(path))
    print(f"  DONE: {filename}")

async def main():
    AUDIO_DIR.mkdir(parents=True, exist_ok=True)
    total = 0

    for qi, s in enumerate(scenarios):
        # Category title
        await gen(s["category"], f"q{qi}_cat.mp3"); total += 1
        # Question
        await gen(s["question"], f"q{qi}_q.mp3"); total += 1

        for ai, a in enumerate(s["answers"]):
            # Answer option text
            await gen(a["text"], f"q{qi}_a{ai}_text.mp3"); total += 1
            # Reaction msg
            await gen(a["msg"], f"q{qi}_a{ai}_msg.mp3"); total += 1
            # Thought
            await gen(a["thought"], f"q{qi}_a{ai}_thought.mp3"); total += 1

    print(f"\n✅ Done! {total} audio files generated in {AUDIO_DIR}")

if __name__ == "__main__":
    asyncio.run(main())

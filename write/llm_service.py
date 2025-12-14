import requests
from datetime import datetime


# ------------------------------------------
# TONE STYLES
# ------------------------------------------
TONE_MAP = {
    "soft": "gentle, warm, simple, soothing, caring",
    "balanced": "calm, steady, grounded, supportive",
    "deep": "emotional, reflective, poetic, heartfelt"
}


# ------------------------------------------
# TEMPLATES
# ------------------------------------------

LETTER_TEMPLATE = """
Letter

Write a short emotional letter.

STRICT RULES:
- 40–55 words only
- soft, warm, simple English
- no advice
- no teaching
- no long stories
- no technology mentions
- tone must be: {tone}
- no emojis
- no signature

Format:

Dear Someone dear,
{content}
"""

JOURNAL_TEMPLATE = """
Journal

Write a short emotional journal entry.

STRICT RULES:
- 45–60 words only
- reflective, soft tone
- simple English
- no advice
- no instructions
- tone must be: {tone}
- no emojis
- no signature

Format:

Date: {date}
{content}
"""


POEM_TEMPLATE = """
📝 Poem

Write a short emotional poem based on: {content}

STRICT RULES:
- 4 short lines only
- soft, simple, expressive
- no advice
- no long story
- tone must be: {tone}

Respond ONLY with the poem.
"""

QUOTE_TEMPLATE = """
💬 Quote

Write a short emotional quote about: {content}

STRICT RULES:
- one sentence only
- under 20 words
- soft, meaningful
- no advice
- tone must be: {tone}

Respond ONLY with the quote.
"""

AFFIRMATION_TEMPLATE = """
🌼 Affirmation

Write a short emotional affirmation inspired by: {content}

STRICT RULES:
- 1–2 lines only
- warm, uplifting, simple
- no advice
- no commands
- tone must be: {tone}

Respond ONLY with the affirmation.
"""

REFLECTION_TEMPLATE = """
🌙 Reflection

Write a short emotional reflection based on: {content}

STRICT RULES:
- 25–45 words only
- introspective, soft
- no advice
- tone must be: {tone}

Respond ONLY with the reflection.
"""

STORY_TEMPLATE = """
📘 Story

Write a very short emotional story based on: {content}

STRICT RULES:
- 2–3 sentences only
- warm, simple, emotional
- no heavy plot
- tone must be: {tone}

Respond ONLY with the story.
"""

NOTE_TEMPLATE = """
🗒️ Note

Write a short structured emotional note about: {content}

RULES:
- Use EXACTLY this bullet format
- No extra sentences
- No emojis
- Soft and simple tone

Format:
• What you felt: {content}
• Why it happened: (1 short line)
• What to try: (1 short line)
"""




# ------------------------------------------
# LLM SERVICE (GEMINI ONLY)
# ------------------------------------------
class LLM_Service:

    def __init__(self):
        pass

    # -------------------------
    # Gemini API call
    # -------------------------
    def call_ollama(self, prompt, model="llama3.2:3b"):
        url = "http://localhost:11434/api/generate"
        payload = {
        "model": model,
        "prompt": prompt,
        "stream": False
        }
        try:
            response = requests.post(url, json=payload)
            return response.json().get("response", "").strip()
        except Exception as e:
            return f"⚠️ Ollama error: {str(e)}"


    # -------------------------
    # Router
    # -------------------------
    def generate(self, mode, text, tone="soft"):
        tone_style = TONE_MAP.get(tone, TONE_MAP["soft"])
        mode = mode.lower().strip()

        # Select template
        prompt = self.build_prompt(mode, text, tone_style)
        safe, result = self.safety_filter(text)
        if not safe:
            return result


        if prompt is None:
            return "⚠️ Unknown mode."

        return self.call_ollama(prompt, model="llama3.2:3b")

    # -------------------------
    # Template selection
    # -------------------------
    def build_prompt(self, mode, text, tone):
        if mode == "letter":
            return LETTER_TEMPLATE.format(content=text, tone=tone)

        elif mode == "journal":
            date_str = datetime.now().strftime("%d/%m/%Y")
            return JOURNAL_TEMPLATE.format(date=date_str, content=text, tone=tone)

        elif mode == "poem":
            return POEM_TEMPLATE.format(content=text, tone=tone)

        elif mode == "quote":
            return QUOTE_TEMPLATE.format(content=text, tone=tone)

        elif mode == "affirmation":
            return AFFIRMATION_TEMPLATE.format(content=text, tone=tone)

        elif mode == "reflection":
            return REFLECTION_TEMPLATE.format(content=text, tone=tone)

        elif mode == "story":
            return STORY_TEMPLATE.format(content=text, tone=tone)

        elif mode == "note":
            return NOTE_TEMPLATE.format(content=text, tone=tone)

        return None
    

    def safety_filter(self, text):
        text_lower = text.lower().strip()

    # --------------------------------------
    # BAD WORD BLOCK
    # --------------------------------------
        bad_words = [
            "fuck", "bitch", "shit", "asshole",
            "bastard", "slut", "dick", "pussy",
            "kill you", "hurt you"  # generic abuse
        ]
        for w in bad_words:
            if w in text_lower:
                return False, "⚠️ Your input contains unsafe or harmful language. Please rewrite it more respectfully."

        selfharm_patterns = [
        "kill myself",
        "kill me",
        "i want to die",
        "end my life",
        "i want to disappear",
        "i hurt myself",
        "self harm",
        "i can't live",
        "no reason to live",
    ]
        for pattern in selfharm_patterns:
            if pattern in text_lower:
                return False, (
                "⚠️ HeartNote AI cannot continue this request.\n"
                "You are feeling something heavy.\n"
                "Here is a gentle, safe message instead:\n\n"
                "• You deserve care.\n"
                "• You are not alone.\n"
                "• Your feelings matter.\n"
            )
            
        return True, text

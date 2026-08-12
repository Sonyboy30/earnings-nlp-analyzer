import json
import time
import anthropic
from dotenv import load_dotenv

load_dotenv()

SYSTEM_PROMPT = """You are a financial analyst evaluating the LANGUAGE of \
earnings calls.

Focus on HOW things are said, not just what is said. Hedging, deflection, \
vague non-answers, topic changes, and shifts in confidence matter more than \
surface-level positive words.

You are analyzing language only. You have no knowledge of how the stock \
performed. Do not speculate about price. Do not let the company's reputation \
influence your scoring — judge only the text in front of you."""


class TranscriptAnalyzer:
    def __init__(self, model="claude-sonnet-5"):
        self.client = anthropic.Anthropic()
        self.model = model

    def analyze(self, ticker, quarter, section_name, text):
        """Analyze one section. Returns a dict, or a dict with 'error'."""

        prompt = f"""Analyze the {section_name} from {ticker}'s {quarter} earnings call.

You MUST respond with ONLY a valid JSON object. No preamble, no markdown, no explanation.

The JSON object must have exactly these keys:
- "sentiment_score": number from -1.0 (very negative) to 1.0 (very positive)
- "confidence_score": number from 0.0 to 1.0, how direct and confident management sounds
- "hedging_count": integer, count of distinctly hedged, evasive, or non-committal statements
- "forward_looking_tone": one of "optimistic", "cautious", "defensive", "neutral"
- "key_topics": list of 3 to 5 short topic strings
- "notable_language": list of up to 3 short observations about specific word choices
- "reasoning": one sentence explaining the sentiment score

TRANSCRIPT SECTION:
{text[:60000]}

RESPOND WITH ONLY THE JSON OBJECT. NO OTHER TEXT."""

        for attempt in range(3):
            try:
                message = self.client.messages.create(
                    model=self.model,
                    max_tokens=1500,
                    system=SYSTEM_PROMPT,
                    messages=[
                        {"role": "user", "content": prompt}
                    ],
                )
                
                raw = message.content[0].text.strip()
                
                # Clean markdown if present
                if raw.startswith("```"):
                    raw = raw.split("```")[1]
                    if raw.startswith("json"):
                        raw = raw[4:]
                    raw = raw.strip()
                
                result = json.loads(raw)
                return result

            except json.JSONDecodeError as e:
                if attempt < 2:
                    print(f"    JSON parse failed (attempt {attempt + 1}/3), retrying...")
                    time.sleep(1)
                    continue
                return {"error": "parse_failed", "raw": raw[:500]}

            except anthropic.RateLimitError:
                wait = 5 * (attempt + 1)
                print(f"    rate limited, waiting {wait}s...")
                time.sleep(wait)

            except anthropic.APIError as e:
                print(f"    API error: {e}")
                return {"error": "api_error", "detail": str(e)}

        return {"error": "max_retries"}
import os
import time
from split import load_transcript, split_transcript
from analyzer import TranscriptAnalyzer
from database import init_db, save, already_done

TRANSCRIPT_DIR = "transcripts"


def parse_filename(filename):
    """AMD_2025-Q1.txt  ->  ('AMD', '2025-Q1')"""
    base = filename.replace(".txt", "")
    parts = base.split("_")
    if len(parts) != 2:
        return None, None
    return parts[0], parts[1]


def main():
    conn = init_db()
    analyzer = TranscriptAnalyzer()

    files = sorted(f for f in os.listdir(TRANSCRIPT_DIR) if f.endswith(".txt"))
    print(f"Found {len(files)} transcripts.\n")

    for filename in files:
        ticker, quarter = parse_filename(filename)
        if ticker is None:
            print(f"SKIP {filename} — filename format is wrong")
            continue

        print(f"{ticker} {quarter}")

        text = load_transcript(os.path.join(TRANSCRIPT_DIR, filename))
        prepared, qa = split_transcript(text)

        sections = [
            ("prepared", "prepared remarks", prepared),
            ("qa", "Q&A section", qa),
        ]

        for section_key, section_label, section_text in sections:
            if not section_text or len(section_text) < 500:
                print(f"  {section_key}: too short, skipping")
                continue

            if already_done(conn, ticker, quarter, section_key):
                print(f"  {section_key}: already analyzed, skipping")
                continue

            result = analyzer.analyze(ticker, quarter, section_label,
                                      section_text)

            if "error" in result:
                print(f"  {section_key}: ERROR — {result['error']}")
                continue

            save(conn, ticker, quarter, section_key, result)
            print(f"  {section_key}: sentiment={result.get('sentiment_score')} "
                  f"hedging={result.get('hedging_count')}")

            time.sleep(1)

        print()

    conn.close()
    print("Done.")


if __name__ == "__main__":
    main()
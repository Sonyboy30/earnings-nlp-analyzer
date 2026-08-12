import re

QA_MARKERS = [
    
    r"start[- ]the[- ]Q&A[- ]session",
    r"open[- ]the[- ]line[- ]for[- ]questions",
    r"we (will|'ll) now (begin|open)[^.]{0,40}questions",
    r"open the (call |line |floor )?(up )?(for|to) questions",
    r"first question (comes|is) from",
    r"ready for questions",
    r"pull the audience for questions now",
    r"conducting the question",
]


def split_transcript(text):
    """Split a transcript into (prepared_remarks, qa_section).

    Returns (full_text, "") if no Q&A marker is found.
    """
    for pattern in QA_MARKERS:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return text[:match.start()], text[match.start():]
    return text, ""


def load_transcript(path):
    """Read a transcript file from disk."""
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()
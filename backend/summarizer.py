import re

def summarize_text(text, max_points=3):

    text = re.sub(r"\s+", " ", text).strip()
    if not text:
        return []
    sentences = re.split(r"(?<=[.!?])\s+", text)
    sentences = [
        sentence.strip()
        for sentence in sentences
        if len(sentence.strip()) > 10
    ]
    if len(sentences) <= max_points:
        return sentences
    words = re.findall(r"\b[a-zA-Z]{3,}\b", text.lower())
    frequency = {}
    for word in words:
        frequency[word] = frequency.get(word, 0) + 1
    scored_sentences = []
    for sentence in sentences:
        sentence_words = re.findall(
            r"\b[a-zA-Z]{3,}\b",
            sentence.lower()
        )
        score = sum(
            frequency.get(word, 0)
            for word in sentence_words
        )
        scored_sentences.append(
            (score, sentence)
        )
    scored_sentences.sort(
        reverse=True,
        key=lambda x: x[0]
    )
    selected = scored_sentences[:max_points]
    selected.sort(
        key=lambda x: sentences.index(x[1])
    )
    return [sentence for _, sentence in selected]
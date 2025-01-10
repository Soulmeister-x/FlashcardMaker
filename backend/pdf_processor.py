import PyPDF2


def extract_text_from_file(file):
    text = ""
    if file.filename.endswith('.pdf'):
        reader = PyPDF2.PdfReader(pdf_file)
        for page in reader.pages:
            text += page.extract_text()
    else:
        with open(file=file) as f:
            text = f.read()
    return text


def split_text_into_chunks(text, max_chunk_size=1000):
    return [text[i:i+max_chunk_size] for i in range(0, len(text), max_chunk_size)]


def generate_flashcards(text_chunks):
    flashcards = []
    for chunk in text_chunks:
        # TODO: Verarbeitung der Chunks mit Ollama
        flashcards.append({
            "frage": f"Was ist der Hauptinhalt von: {chunk:50}...?",
            "antwort": chunk[:200]
        })
    return flashcards


def process_file(file):
    text = extract_text_from_file(file)
    chunks = split_text_into_chunks(text=text)
    return generate_flashcards(chunks)

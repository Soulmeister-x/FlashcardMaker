import PyPDF2
from ollama_request import ask_llm_to_extract_facts, generate_question_for_answer


def extract_text_from_file(file):
    text = ""
    if isinstance(file, str) and file.endswith('.pdf'):
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            text += page.extract_text()
    elif file.filename.endswith('.pdf'):
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            text += page.extract_text()
    else:
        with open(file=file) as f:
            text = f.read()
    return text

#def extract_text_from_file_pdf(file):
#    reader = PyPDF2.PdfReader(file)


def split_text_into_chunks(text, max_chunk_size=1000):
    chunks = [
        text[i-int(max_chunk_size*0.05):i+int(max_chunk_size*1.05)] 
            for i in range(0, len(text), max_chunk_size)
    ]
    return chunks


def generate_flashcards(text_chunks):
    flashcards = []
    last_chunk = ""
    for chunk in text_chunks:
        # generate answers
        answers = ask_llm_to_extract_facts(chunk, last_chunk)

        # generate questions
        for answer in answers:
            flashcards.append({
                "answer": answer,
                "question": generate_question_for_answer(answer)
            })
        last_chunk = chunk
    return flashcards


def process_file(file):
    text = extract_text_from_file(file)
    chunks = split_text_into_chunks(text=text)
    return generate_flashcards(chunks)


def test_processing():
    import os
    _file_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        'data/original/Hasuarbeit-Visualisierung.pdf')
    return process_file(_file_path)

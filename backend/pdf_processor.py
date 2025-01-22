import PyPDF2
from ollama_request import ask_llm_to_extract_facts, generate_question_for_answer
from dotenv import load_dotenv


load_dotenv()


def extract_text_from_file(file):
    text = ""
    if isinstance(file, str) and file.endswith('.pdf'):
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            text += page.extract_text()
    else:
        with open(file=file) as f:
            text = f.read()
    return text

#def extract_text_from_file_pdf(file):
#    reader = PyPDF2.PdfReader(file)


def split_text_into_chunks(text, max_chunk_size=1000) -> list[str]:
    chunks = [
        text[i-int(max_chunk_size*0.05):i+int(max_chunk_size*1.05)] 
            for i in range(0, len(text), max_chunk_size)
    ]
    return chunks


def find_facts_from_chunks(chunks) -> list[str]:
    facts = []
    last_chunk = ""
    for chunk in chunks:
        if not chunk:
            continue
        facts.append(ask_llm_to_extract_facts(chunk, last_chunk))
        last_chunk = chunk
    return facts


#def generate_questions_for_facts(facts: list[str])


def generate_flashcards(text_chunks):
    flashcards = []
    last_chunk = ""
    for chunk in text_chunks:
        if not chunk:
            continue
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
        'data/original/Hausarbeit-Visualisierung.pdf')
    if not os.path.exists(_file_path):
        return "file not found: "+_file_path
    return process_file(_file_path)


if '__main__' == __name__:
    import os
    pdf_file = os.environ.get('PDF_FILE')
    #pdf_password = os.environ.get('PDF_PASSWORD')
    print(f"processing: {pdf_file}")
    text = extract_text_from_file(pdf_file)
    chunks = split_text_into_chunks(text=text)
    print(f"text was split into {len(chunks)} chunks")
    for chunk in chunks[:10]:
        print(f">  {chunk}")
    print("...\n")

    max_len = 50
    chunks = chunks[:max_len] if (len(chunks) >= max_len) else chunks[:len(chunks)]

    print(f"trying to find facts for these chunks...")
    if 'y' != input("Proceed? [N/y] ").lower():
        exit(0)
    facts = find_facts_from_chunks(chunks)
    print(f"extracted {len(facts)} facts")
    for fact in facts:
        print(fact)


#from langchain_core.prompts import ChatPromptTemplate
#from langchain_ollama.llms import OllamaLLM
#from langchain_ollama import ChatOllama
import os
#from typing_extensions import TypedDict
from pydantic import BaseModel
from ollama import chat



class Question(BaseModel):
    question: str

    def __str__(self):        
        return self.question if self.question.endswith('?') else self.question+'?'


class FactList(BaseModel):
    fact_list: list[str]

    def __str__(self):
        return "\n".join(self.fact_list)


class Flashcard(BaseModel):
    question: str
    answer: str

    def __str__(self):
        return f"{self.question};{self.answer}"

class Flashcards(BaseModel):
    cards: list[Flashcard]

    def __str__(self):
        return "\n".join([str(card) for card in self.cards])


def log_response(response: str):
    log_path = 'responses.log'
    if not os.path.exists(log_path):
        os.mknod(log_path)
    with open(log_path, 'a') as f:
        f.writelines(['-----', response, '-----'])


def _get_template_facts(text_chunk, previous_chunk):
    return [
        ('system', 'You are a helpful and concise AI Bot that specializes in text summarization.'),
        ('user', 'I have a chunked text. Analyze the following text_chunk and previous_chunk. Make a concise list of the most important facts from ONLY text_chunk:'),
        ('user', f"previous_chunk (context): ### {previous_chunk} ###"),
        ('user', f"text_chunk: ### {text_chunk} ###"),
        ('user', 'A good fact is:\n- Short, concrete and precise.\n- Has the original language of the text (German or English).\n'),
        ('user', 'Important:\n- Keep the language of the text (German or English).\n- Use clear, objective language without interpretations or opinions.\n- Make sure the facts cover the main content of the text without including unimportant details.\n- Avoid repetition.\n- Return only the facts, without additional explanations or comments.')
    ]


def _get_template_question():
    return [
        ('system', 'You are a helpful AI Bot that specializes in concise text generation.'),
        ('user', 'Generate an exact question for the provided fact in the language of the fact.'),
        ('user', f"fact: ### {answer} ###"),
        ('user', 'A good question is:\n- Encouraging interest and arousing curiosity.\n- Positively worded.\n- Concrete and precise.'),
        ('user', 'Important:\n- Question must be formulated in the same language as the fact (German or English).\n- Return only the question, without additional explanations or comments.')
    ]


def _invoke_llm(messages, format="json", model: str="llama3.2:1b"):
    response = chat(
        messages={"messages":messages},
        model=model,
        format=format
    )
    return response


def ask_llm_to_extract_facts(chunk, last_chunk):
    template = _get_template_facts(text_chunk=chunk, previous_chunk=last_chunk)
    response = _invoke_llm(messages=template, format=FactList.model_json_schema())
    facts = FactList.model_validate_json(response.message.content)
    return facts


def generate_question_for_answer(answer):
    template = _get_template_question(answer=answer)
    response = _invoke_llm(messages=template)
    question = Question.model_validate_json(response.message.content)
    return question



if '__main__' == __name__:
    print(Flashcards.model_json_schema())
    #create_flashcards_from_data()

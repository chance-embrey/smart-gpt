from dotenv import load_dotenv
import os
import openai
from typing import List

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")


def generate_response(prompt: str, model: str = "gpt-4") -> str:
    response = openai.ChatCompletion.create(
        model=model,
        messages=[{
            "role": "user", "content": prompt
        }],
        max_tokens=150,
        n=1,
        stop=None,
        temperature=0.5,
    )

    return response.choices[0].message['content'].strip()


def chain_of_thought_prompting(question: str) -> str:
    prompt = f"Let's work this out in a step-by-step way to make sure we have the right answer. Question: {question}"
    response = generate_response(prompt)
    print("Thinking step by step...")
    return response


def reflection_and_dialogue(question: str, response: str) -> str:
    reflection_prompt = f"I answered the question '{question}' with the response '{response}'. Is this response correct? If not, what is the correct answer?"
    reflection_response = generate_response(reflection_prompt)
    print("Reflecting and dialoguing...")
    return reflection_response


def smart_gpt(question: str) -> str:
    step_by_step_response = chain_of_thought_prompting(question)
    final_response = reflection_and_dialogue(question, step_by_step_response)

    return final_response


def main():
    question = input("What is your question?\n")
    response = smart_gpt(question)
    print(f"Smart GPT Response: \n{response}")


main()

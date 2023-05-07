from dotenv import load_dotenv
import os
import openai
from typing import List

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")
gpt_model = os.getenv("GPT_MODEL")


def generate_response(prompt: str) -> str:
    response = openai.ChatCompletion.create(
        model=gpt_model,
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
    prompt = f"Answer: Let's work this out in a step-by-step way to make sure we have the right answer. Question: {question}"
    response = generate_response(prompt)
    print("Thinking step by step...")
    print("Initial response: ", response)
    return response


def reflection_and_dialogue(question: str, response: str, max_rounds: int = 3) -> str:
    current_round = 1
    while current_round <= max_rounds:

        reflection_prompt = f"I answered the question '{question}' with the response '{response}'. Is this response correct? If yes, reply exactly 'Yes, this response is correct'. If not, what is the correct answer?"
        reflection_response = generate_response(reflection_prompt)

        print(
            f"Round {current_round}/{max_rounds} reflextion and dialogue: ", reflection_response)

        if "yes, this response is correct" in reflection_response.lower():
            break
        else:
            response = reflection_response
            current_round += 1

    return response


def smart_gpt(question: str) -> str:
    step_by_step_response = chain_of_thought_prompting(question)
    final_response = reflection_and_dialogue(question, step_by_step_response)

    return final_response


def main():
    question = input("What is your question?\n")
    response = smart_gpt(question)
    print(f"\n\nSmart GPT Response: \n{response}")


main()

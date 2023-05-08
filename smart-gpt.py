from dotenv import load_dotenv
import os
import openai
from typing import List, Set

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")
gpt_model = os.getenv("GPT_MODEL")


def generate_response(prompt: str) -> str:
    response = openai.ChatCompletion.create(
        model=gpt_model,
        messages=[{
            "role": "user", "content": prompt
        }],
        max_tokens=500,
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


def jaccard_similarity(set1: Set[str], set2: Set[str]) -> float:
    intersection = set1.intersection(set2)
    union = set1.union(set2)
    return len(intersection) / len(union)


def tokenize_text(text: str) -> Set[str]:
    return set(text.lower().split())


def is_response_correct(reflection_response: str) -> bool:
    positive_keywords = ["response is correct",
                         "answer is accurate", "answer is right"]
    for keyword in positive_keywords:
        if keyword in reflection_response.lower():
            return True
    return False


def reflection_and_dialogue(question: str, response: str, max_rounds: int = 3, similarity_threshold: float = 0.7) -> str:
    current_round = 1
    previous_responses = []

    while current_round <= max_rounds:
        reflection_prompt = f"The following question was asked '{question}'\n The response was '{response}'\n Is this response correct? If not, what is the correct answer?"
        reflection_response = generate_response(reflection_prompt)

        print(
            f"Round {current_round}/{max_rounds} reflection and dialogue: ", reflection_response)

        if is_response_correct(reflection_response):
            break

        for prev_response in previous_responses:
            prev_tokens = tokenize_text(prev_response)
            curr_tokens = tokenize_text(reflection_response)
            similarity = jaccard_similarity(prev_tokens, curr_tokens)

            if similarity >= similarity_threshold:
                print(
                    "Detected looping or non-improving response. Terminating the reflection and dialogue loop.")
                return response

        previous_responses.append(reflection_response)
        response = reflection_response
        current_round += 1

    return response


def smart_gpt(question: str) -> str:
    step_by_step_response = chain_of_thought_prompting(question)
    final_response = reflection_and_dialogue(question, step_by_step_response)

    return final_response


test_question = """
 Which of the following propositions is an immediate (one-step) consequence in PL of the given premises?
~E ⊃ ~F
G ⊃ F
H ∨ ~E
H ⊃ I
~I

Options: 
A. E ⊃ F
B. F ⊃ G
C. H ⊃ ~E
D. ~H

"""


def main():
    # question = test_question
    question = input("What is your question?\n")
    response = smart_gpt(question)
    print(f"\n\nSmart GPT Response: \n{response}")


main()

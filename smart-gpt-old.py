from dotenv import load_dotenv
import os
import openai

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")
gpt_model = os.getenv("GPT_MODEL")


def generate_response(prompt: str, temperature=0.5) -> str:
    response = openai.ChatCompletion.create(
        model=gpt_model,
        messages=[{
            "role": "user", "content": prompt
        }],
        max_tokens=500,
        n=1,
        stop=None,
        temperature=temperature,
    )

    return response.choices[0].message['content'].strip()


def generate(original_prompt) -> str:
    prompt = f"Let's work this out in a step-by-step way to make sure we have the right answer. ]n{original_prompt}"
    response = generate_response(prompt)
    print("Response: ", response)
    return response


def is_response_correct(reflection_response: str) -> bool:
    positive_keywords = ["response is correct",
                         "answer is accurate", "answer is right"]
    for keyword in positive_keywords:
        if keyword in reflection_response.lower():
            return True
    return False


def reflection_and_dialogue(question: str, response: str, min_rounds: int = 2, max_rounds: int = 3) -> str:
    current_round = 1
    correct_rounds = 0
    messages = [{"role": "system", "content": "You are a helpful assistant that provides accurate answers through self-dialogue and reflection."}]
    messages.append({"role": "user", "content": question})
    messages.append({"role": "assistant", "content": response})

    while current_round <= max_rounds:
        prompt = f"Is the answer '{response}' correct? If not, what is the correct answer?"
        messages.append(
            {"role": "user", "content": chain_of_thought_prompting(prompt)})
        generated_response = openai.ChatCompletion.create(
            model=gpt_model,
            messages=messages,
            max_tokens=150,
            n=1,
            stop=None,
            temperature=0.5,
        )

        response_text = generated_response.choices[0].message['content'].strip(
        )
        messages.append({"role": "assistant", "content": response_text})

        if is_response_correct(response_text):
            correct_rounds += 1
            if correct_rounds >= min_rounds:
                break
        else:
            correct_rounds = 0

        current_round += 1

    return response_text


def smart_gpt(question: str) -> str:
    step_by_step_response = chain_of_thought_prompting(question)
    final_response = reflection_and_dialogue(question, step_by_step_response)

    return final_response


# test_question = """
# Construct a complete truth table for the following pairs of propositions. Then, using the truth tables, determine whether the statements are logically equivalent or contradictory. If neither, determine whether they are consistent or inconsistent. Justify your answers.
# ~(J ∨ K) · L and (L ⊃ J) · K"
# A. Logically equivalent
# B. Contradictory
# C. Neither logically equivalent nor contradictory, but consistent
# D. Inconsistent
# """

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
    # question = input("What is your question?\n")
    question = test_question
    response = smart_gpt(question)
    print(f"\n\nSmart GPT Response: \n{response}")


main()

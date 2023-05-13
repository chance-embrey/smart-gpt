from dotenv import load_dotenv
import os
import openai

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")
gpt_model = os.getenv("GPT_MODEL")


def gpt4_api_call(prompt, system_prompt, temperature=0.5):
    messages = [
        {
            "role": "system",
            "content": system_prompt,
        },
        {
            "role": "user",
            "content": prompt,
        },
    ]
    api_response = openai.ChatCompletion.create(
        model=gpt_model,
        messages=messages,
        n=1,
        stop=None,
        temperature=temperature,
        max_tokens=60,
    )
    response = api_response.choices[0].message.content #type: ignore
    print(f"\nPrompt: '{prompt}'\nTemperature: {temperature}\nResponse: {response}\n")  
    return response

def get_input():
    question = input("\nPlease enter your question: ")
    return question


def add_chain_of_thought_prompt(question):
    return f"Let's work this out in a step-by-step way to make sure we have the right answer. What is the answer to the following question?\nQuestion: {question}"


def get_gpt4_responses(prompt):
    responses = []
    system_prompt = "You are an intelligent question answering assistant that provides accurate answers."
    temperatures = [0.2, 0.5, 0.8]
    for temperature in temperatures:
        response = gpt4_api_call(prompt, system_prompt, temperature)
        responses.append(response)
    return responses


def reflect_and_dialogue(question, responses):
    reflection_responses = []
    system_prompt = "You are an intelligent assistant that can use reflection to find flaws in an answer to a question."
    for response in responses:
        reflection_prompt = f"Analyze the following response to the following question, and find any flaws in their reasoning.\nQuestion: {question}\nResponse: {response}"
        reflection_response = gpt4_api_call(reflection_prompt, system_prompt)
        reflection_responses.append(reflection_response)
    return reflection_responses

def format_responses_and_feedback(responses, feedback):
    responses_and_feedback = []
    # Add newline to end of each response
    responses = [response + "\n" for response in responses]
    for response, feedback in zip(responses, feedback):
        responses_and_feedback.append((response, feedback))
    return responses_and_feedback


def correct_errors(question, responses_and_feedback):
    corrected_responses = []
    system_prompt = "You are an intelligent assistant that can use feedback to correct errors in an answer to a question."
    for response, feedback in responses_and_feedback:
        correction_prompt = (
            f"Question: {question}\nAnswer:{response}  Feedback: {feedback}\n"
        )
        corrected_response = gpt4_api_call(correction_prompt, system_prompt)
        corrected_responses.append(corrected_response)
    return corrected_responses


def resolve(question, corrected_responses):
    system_prompt = "You are an intelligent resolver that can decide which of several corrected responses is correct."
    resolver_prompt = f"Given the following corrected responses to a question, decide which answer is correct.\nQuestion:{question}\nResponses: {corrected_responses}"
    chosen_response = gpt4_api_call(resolver_prompt, system_prompt)
    return chosen_response


def main():
    question = get_input()
    prompt = add_chain_of_thought_prompt(question)
    initial_responses = get_gpt4_responses(prompt)
    feedback = reflect_and_dialogue(question, initial_responses)
    responses_and_feedback = format_responses_and_feedback(initial_responses, feedback)
    corrected_responses = correct_errors(question, responses_and_feedback)
    final_answer = resolve(question, corrected_responses)
    print(final_answer)


if __name__ == "__main__":
    main()

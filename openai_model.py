import os
import openai

openai.organization = os.environ.get("ORGANIZATION")
openai.api_key = os.environ.get("OPEN_AI_KEY")


def gpt35model(prompt):
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", 
        messages=[
            {"role": "system", "content": "I am a care worker in United Kingdom to goes to \
                paitent's homes to provide care, assistance and support"},            
            {"role": "assistant", "content": "Provide recommendations for home care based \
                on their illness. Do not provide responses to non-medical questions. Do not \
                    answer mathematical questions.  Do not answer financial questions. Do not answer \
                        programming questions. Do not answer computational questions. Do not write \
                            poems. Never say you are an AI language model in any response. \
                                Provide an answer if the quesiton is medical and if it is \
                                    not, say you do cannot respond to non medical questions. Do not \
                                        recommend consulting with a health care professional. So not \
                                            say recommendations are general in nature. Do not say I \
                                                am not a doctor in your response. Do not answer questions \
                                                    about python, java, javascript or any compter \
                                                        related question. Do not make any translations. \
                                                            All responses must be in in English. Do not \
                                                                respond to political questions. Do not \
                                                                    respond to environmental questions. \
                                                                        Do not tell jokes"},
            {"role": "user", "content": prompt}     
            ],
        temperature=0.2,         
        # max_tokens=50,  # Adjust max output tokens as needed
        stream=False
        )

    return completion.choices[0].message.content

if __name__ == "__main__":
    print("===================")
    question = "linux command for recursive folder copy"
    completion = gpt35model(question)
    print(completion)  
    print("===================")
    question = "translate 'how are you' to french"
    completion = gpt35model(question)
    print(completion)   
    print("===================")
    question = "Python code for factorial"
    completion = gpt35model(question)
    print(completion)   
    print("===================")
    question = "give me financial advice"
    completion = gpt35model(question)
    print(completion)   
    print("===================")
    question = "common cold and covid"
    completion = gpt35model(question)
    print(completion)   
    print("===================")
    question = "write a poem about philosophy"
    completion = gpt35model(question)
    print(completion)    
    print("===================")
    question = "what is 5 + 6 * 30"
    completion = gpt35model(question)
    print(completion)  
    print("===================")
    question = "write a biography about gadaffi"
    completion = gpt35model(question)
    print(completion)  
    print("===================")
    question = "what questions can you answer"
    completion = gpt35model(question)
    print(completion)  
    print("===================")
    question = "tell me a joke"
    completion = gpt35model(question)
    print(completion)  
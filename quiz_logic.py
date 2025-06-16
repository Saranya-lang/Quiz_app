from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv

load_dotenv()

def generate_quiz(topic):
    llm = ChatOpenAI(model="gpt-4o")

    prompt = PromptTemplate(
        input_variables=["topic"],
        template="""
Generate 20 multiple choice questions on "{topic}".
Each should have:
- Question
- 4 options (a–d)
- Answer line like: Answer: c
Output example:
Q1. Question text?
a) Option 1
b) Option 2
c) Option 3
d) Option 4
Answer: b
"""
    )

    chain = prompt | llm
    response = chain.invoke({"topic": topic})
    return response.content

if __name__ == "__main__":
    print("generate_quiz:", generate_quiz)


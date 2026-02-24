from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage
from dotenv import load_dotenv
import requests

load_dotenv()
# tool crate 

@tool

def multiply(a: int, b: int) -> int:
    """Given 2 numbers a and b this tool returns their product"""
    return a * b

# print(multiply.invoke({'a': 5, 'b': 6}))
# print(multiply.name)

# tool binding



llm = ChatOpenAI(model='gpt-4o-mini')

tools = llm.bind_tools([multiply])

query = HumanMessage('can you multiply 55 with 66')

messages = [query]
# print(messages)
b = tools.invoke(messages)

messages.append(b)

# print(messages)

# print(b)


# a = b.tool_calls[0]

# print(a)

# result = multiply.invoke(b.tool_calls[0]['args'])
result = multiply.invoke(b.tool_calls[0])
messages.append(result)

# print(messages)

answer = llm.invoke(messages).content

print(answer)
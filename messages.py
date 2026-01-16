from langchain_core.messages import SystemMessage,HumanMessage,AIMessage
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

model = ChatOpenAI(model='gpt-4o-mini')

messages = [
    SystemMessage(content='hi you are helpful assistant'),
    HumanMessage(content='tell me about the pytorch')
]

result = model.invoke(messages)

messages.append(AIMessage(content=result.content))

print(messages)
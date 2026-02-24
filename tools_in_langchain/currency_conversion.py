from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage
from dotenv import load_dotenv
import requests
from langchain_core.tools import InjectedToolArg
from typing import Annotated
import json
load_dotenv()

@tool
def get_conversion_factor(base_currency: str, target_currency: str) -> float:
    """
    This function fetches the currency conversion factor between the base currency and target currency
    """
    url = f'https://v6.exchangerate-api.com/v6/a16069ed7a8b84cb536ca8c4/pair/{base_currency}/{target_currency}'

    response = requests.get(url)
    

    return response.json()

@tool
def convert(base_currency_value : int, conversion_rate : Annotated[float, InjectedToolArg]) -> float:
    """
    Given a currency conversion rate this function calculates the target currency value from a given base currency value
    """
    
    return base_currency_value * conversion_rate


# conversion = get_conversion_factor.invoke({'base_currency':'USD', 'target_currency':'INR'})

# conversion = convert.invoke({'base_currency_value':12, 'conversion_rate':90.9674})

# print(conversion)

# TOOL BINDING

llm = ChatOpenAI(model='gpt-4o-mini')

llm_with_tools = llm.bind_tools([get_conversion_factor,convert])

messages = [HumanMessage('What is the conversion factor between USD and INR, and based on that can you convert 49 USD to INR')]
# print(messages)
ai_message = llm_with_tools.invoke(messages)
messages.append(ai_message)
n = ai_message.tool_calls
# print(n)

for tool_call in ai_message.tool_calls:
    #exceute the 1st tool and get the value of conversion rate
    if tool_call['name'] == 'get_conversion_factor':
        tool_message1 = get_conversion_factor.invoke(tool_call)
        #fetch this conversion rate 
        conversion_rate =json.loads(tool_message1.content)['conversion_rate']
        # append this tool message to message list 
        messages.append(tool_message1)    
    #exceute the 2nd tool using the conversion rate from tool1
    if tool_call['name'] == 'convert':
        # fetch the current arg
        tool_call['args']['conversion_rate'] = conversion_rate
        tool_message2 = convert.invoke(tool_call)
        messages.append(tool_message2) 

# print(messages)

b = llm_with_tools.invoke(messages).content

print(b)
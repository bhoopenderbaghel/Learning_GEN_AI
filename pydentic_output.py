from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel,Field

load_dotenv()

llm = HuggingFaceEndpoint(
    repo_id='meta-llama/Llama-3.2-1B-Instruct',
    task='text-generation'
)

model = ChatHuggingFace(llm=llm)

class Person(BaseModel):
    name: str = Field(description='Name of a person')
    age: int = Field(gt= 18, description='Age of the person')
    city: str = Field(description='Name of the city person belong to')

parser = PydanticOutputParser(pydantic_object=Person)

template = PromptTemplate(
    template='Generate the name, age and city of a fictional {place} person \n {format_instruction}',
    input_variables=['place'],
    partial_variables={'format_instruction':parser.get_format_instructions()}  
)

# prompt = template.invoke({'place':'Bhutan'})

# # print(prompt)

# result = model.invoke(prompt)

# final_result = parser.parse(result.content)
chain = template | model | parser

final_result = chain.invoke({'place':'brazil'})

print(final_result)

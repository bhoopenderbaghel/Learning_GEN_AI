from langchain_openai import ChatOpenAI
from langchain_huggingface import ChatHuggingFace,HuggingFaceEndpoint
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableParallel
load_dotenv()

model = ChatOpenAI(model='gpt-4o-mini')


hf_llm = HuggingFaceEndpoint(
    repo_id="meta-llama/Llama-3.2-1B-Instruct",
    task="text-generation",
)

model1 = ChatHuggingFace(llm=hf_llm)

prompt = PromptTemplate(
    template='Generate short and simple notes from the following text \n {text}',
    input_variables=['text']
)

prompt1 = PromptTemplate(
    template='Generate 5 short question answer from the following text \n {text}',
    input_variables=['text']
)


prompt2 = PromptTemplate(
    template='Merge the provided notes and quiz into a single document \n notes -> {notes} and {quiz}',
    input_variables=['notes','quiz']
)

parser = StrOutputParser()

#parallel chains 

parallel_chain = RunnableParallel({
    'notes': prompt | model | parser,
    'quiz' : prompt1 | model1 | parser
})

merge_chain = prompt2 | model | parser

chain = parallel_chain | merge_chain

text = """
This article explains the new features in Python 3.14, compared to 3.13. Python 3.14 was released on 7 October 2025. For full details, see the changelog.

See also PEP 745 – Python 3.14 release schedule
Summary – Release highlights
Python 3.14 is the latest stable release of the Python programming language, with a mix of changes to the language, the implementation, and the standard library. The biggest changes include template string literals, deferred evaluation of annotations, and support for subinterpreters in the standard library.

The library changes include significantly improved capabilities for introspection in asyncio, support for Zstandard via a new compression.zstd module, syntax highlighting in the REPL, as well as the usual deprecations and removals, and improvements in user-friendliness and correctness.

This article doesn’t attempt to provide a complete specification of all new features, but instead gives a convenient overview. For full details refer to the documentation, such as the Library Reference and Language Reference. To understand the complete implementation and design rationale for a change, refer to the PEP for a particular new feature; but note that PEPs usually are not kept up-to-date once a feature has been fully implemented. See Porting to Python 3.14 for guidance on upgrading from earlier versions of Python.

"""

result = chain.invoke({'text':text})

# print(result)

chain.get_graph().print_ascii()
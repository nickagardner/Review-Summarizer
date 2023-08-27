from fastapi import FastAPI, Request
from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.chains import LLMChain
from langchain.schema import BaseOutputParser

app = FastAPI()

@app.post("/summarize")
async def summarize(info : Request):
    req_info = await info.json()
    output = _summarize(req_info)
    return {
        "status" : "SUCCESS",
        "data" : output,
    }


def _summarize(req_info)
    class CommaSeparatedListOutputParser(BaseOutputParser):
        """Parse the output of an LLM call to a comma-separated list."""
    
    
        def parse(self, text: str):
            """Parse the output of an LLM call."""
            return text.strip().split(", ")
    
    template = """You are a helpful assistant who summarizes product reviews. 
    A user will pass in a list of reviews, and you should generate 5 common themes present in the reviews as a comma separated list.
    ONLY return a comma separated list, and nothing more."""
    system_message_prompt = SystemMessagePromptTemplate.from_template(template)
    human_template = "{text}"
    human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)
    
    chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])
    chain = LLMChain(
        llm=ChatOpenAI(openai_api_key=req_info[0]),
        prompt=chat_prompt,
        output_parser=CommaSeparatedListOutputParser()
    )
    return chain.run(req_info[1:])
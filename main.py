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
    themes, counts = _summarize(req_info)
    return {
        "status" : "SUCCESS",
        "data" : [themes, counts],
    }


def _summarize(req_info):
    class CommaSeparatedListOutputParser(BaseOutputParser):
        """Parse the output of an LLM call to a comma-separated list."""
    
    
        def parse(self, text: str):
            """Parse the output of an LLM call."""
            return text.strip().split(", ")
    
    template = """You are a helpful assistant who summarizes product reviews. 
    A user will pass in a list of reviews, and you should generate 5 common positive themes as a comma separated list.
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
    
    pos_themes = chain.run(req_info[1:])

    template = """You are a helpful assistant who summarizes product reviews. 
    A user will pass in a list of reviews, and you should generate 5 common negative themes as a comma separated list.
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
    
    neg_themes = chain.run(req_info[1:])

    themes = pos_themes.extend(neg_themes)

    template = """You are a helpful assistant who counts how many times themes appear in a list of reviews. 
    A user will pass in a list of reviews, and a list of 10 themes. For each review, you will determine whether each theme is present. 
    You will return a list of counts where each count corresponds with the number of times each theme appeared in the reviews. 
    ONLY return a comma separated list, and nothing more."""
    system_message_prompt = SystemMessagePromptTemplate.from_template(template)
    human_template = """Reviews: {reviews}
    Themes: """
    human_message_prompt = HumanMessagePromptTemplate.from_template(input_variables=["reviews", "themes"],
                                                                    template=human_template)
    
    chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])
    chain = LLMChain(
        llm=ChatOpenAI(openai_api_key=req_info[0]),
        prompt=chat_prompt,
        output_parser=CommaSeparatedListOutputParser()
    )

    counts = chain.run({
    'reviews': reviews,
    'themes': themes
    }))

    return (themes, counts)
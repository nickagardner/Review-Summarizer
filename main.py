from fastapi import FastAPI, Request
from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.chains import LLMChain
from langchain.schema import BaseOutputParser
import numpy as np

app = FastAPI()

@app.post("/summarize")
async def summarize(info : Request):
    req_info = await info.json()
    themes, counts = _summarize(req_info)
    return {
        "status" : "SUCCESS",
        "data" : {"themes": themes, 
                  "counts": counts},
    }


def _summarize(req_info):
    class CommaSeparatedListOutputParser(BaseOutputParser):
        """Parse the output of an LLM call to a comma-separated list."""
    
    
        def parse(self, text: str):
            """Parse the output of an LLM call."""
            return text.strip().split(", ")
    
    template = """You are a helpful assistant who summarizes product reviews. 
    A user will pass in a list of reviews, and you should generate the 5 most common positive sentiments expressed in those reviews as a comma separated list.
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
    
    themes = chain.run(req_info[1:])

    template = """You are a helpful assistant who summarizes product reviews. 
    A user will pass in a list of reviews, and you should generate the 5 most common negative sentiments expressed in those reviews as a comma separated list.
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

    themes.extend(neg_themes)

    counts = np.zeros(10)
    for i in range(1, len(req_info)):
        template = """You are a helpful assistant who counts how many times certain themes appear in a review. 
        A user will pass in reviews, and a list of 10 themes. For each theme, you will determine if that theme is present in the review. 
        You will return a comma separated list of 10 values where a value of 1 indicates that the corresponding theme is present and a 
        value of 0 indicates that the theme is not present in this review. ONLY return a comma separated list, and nothing more."""
        system_message_prompt = SystemMessagePromptTemplate.from_template(template)
        human_template = """Review: {review}
        Themes: {themes}"""
        human_message_prompt = HumanMessagePromptTemplate.from_template(input_variables=["review", "themes"],
                                                                        template=human_template)
        
        chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])
        chain = LLMChain(
            llm=ChatOpenAI(openai_api_key=req_info[0]),
            prompt=chat_prompt,
            output_parser=CommaSeparatedListOutputParser()
        )

        temp_count = chain.run({
        'review': req_info[i],
        'themes': themes
        })

        print(req_info[i])
        print(themes)
        print(temp_count)

        counts = np.add(counts, temp_count) 

    return themes, counts
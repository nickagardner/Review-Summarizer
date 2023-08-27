# Purpose
This project is a chrome extension that summarizes (using Gen AI) reviews for Amazon products and highlights salient details and statistics  

# TODO
* Basic MVP
    * Create fastapi Langchain implementation to query with information from extension
    * Summarize reviews and show interesting metrics / conclusions in some format
   
* Refinements
    * Create system for specifying OpenAI API key
    * Determine a better solution for getting around CORS issue
        * It appears [CORS Unblock](https://chrome.google.com/webstore/detail/cors-unblock/lfhmikememgdcahcdlaciloancbhjino) was able to get around this issue, but even after uninstalling the extension I am still not having CORS issues. Not sure if something was resolved there or if some permanent CORS setting was enabled by the extension. Will wait and see. 
    * Investigate array capping
        * For some reason, it appears that the reviews array can't contain more than 100 elements. Being pretty unfamiliar with JS, I am not sure what the issue is unfortunately. As openai charges by token, it is likely just fine that I can't include more than 100 reviews, but I would like to figure this out for personal benefit
    * Expand capability / displayed information
        * Have chatbot interface that user can query with questions about the product

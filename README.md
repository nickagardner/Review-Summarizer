# Purpose
This project is a chrome extension that summarizes (using Gen AI) reviews for Amazon products and highlights salient details and statistics  

# TODO
* Basic MVP
    * Resolve issue with some urls that contain "?" instead of "/" after product ASIN
    * Get Langchain working in JS
        * I have a functional demo in this project for langchain functionality in python, so hopefully replicating in JS will not be impossible
    * Summarize reviews and show interesting metrics / conclusions in some format
   
* Refinements
    * Determine a better solution for getting around CORS issue
        * At least in chrome, getting content from different web pages violates CORS policies. Currently, I am solving this by opening a fresh browser with web security disabled
           * ```open -na Google\ Chrome --args --user-data-dir=/tmp/temporary-chrome-profile-dir --disable-web-security```
        * Obviously, this is not a reasonable permanent solution. Currently, the most reasonable solution to pursue in the future seems to be routing traffic through a proxy server. There used to be just such a free resource (https://cors-anywhere.herokuapp.com/), but it seems that is not viable anymore. Perhaps another similar solution exists
    * Investigate array capping
        * For some reason, it appears that the reviews array can't contain more than 100 elements. Being pretty unfamiliar with JS, I am not sure what the issue is unfortunately. As openai charges by token, it is likely just fine that I can't include more than 100 reviews, but I would like to figure this out for personal benefit
    * Expand capability / displayed information

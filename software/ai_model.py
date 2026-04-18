"""
Step2:
text generation using gemini api
generate api key from: https://ai.google.dev/gemini-api/docs/api-key
"""

import google.generativeai as genai

# configure(api_key = "AIzaSyDnpqsCSYHMeF7PtDPHzeJD3skx4FfD77g")

def gemini_api(text):
    #Initialize a genAI model
    model = genai.GenerativeModel(model_name = "gemini-2.5-flash-latest")
    convo = model.start_chat()
    #generate a response based on the input text.
    response = model.generate_content(text)

    print(response.text)

    #-------------MAIN-------------

    text = "2+2 is ?"
    gemini_api(text)

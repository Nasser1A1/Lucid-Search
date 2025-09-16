from typing import List
import google.generativeai as genai
from config import Settings

settings = Settings()

class GeminiService:
    def __init__(self):
        genai.configure(api_key=settings.GOOGLE_GEMNINI_API_KEY)
        self.client = genai.GenerativeModel('gemini-2.5-flash')
    def generate_response(self, query:str, sorted_citations: List[dict]):
        """
        URL1 : url
        Content1 : This is an example of 
        URL2 : url
        Content2 : This is an example of content
        URL3 : url
        Content3 : This is an example of content
        """
        context = "\n\n".join([f"Source ${i+1}: {doc['url']}\nContent: {doc['content']}" for i,doc in enumerate(sorted_citations)])
        full_promot = f"""Context from web Search : {context} 
        Question : {query}
        Please provide a comprehensives, detailed, well-sited using the above context.
        Ensure it answer the user query and don't use your own knowledge until it is very necessary.
        """
        # Generate text from a prompt
        response = self.client.generate_content(full_promot)
        return response.text
    def generate_response_stream(self, query:str, sorted_citations: List[dict]):
        """
        URL1 : url
        Content1 : This is an example of 
        URL2 : url
        Content2 : This is an example of content
        URL3 : url
        Content3 : This is an example of content
        """
        context = "\n\n".join([f"Source ${i+1}: {doc['url']}\nContent: {doc['content']}" for i,doc in enumerate(sorted_citations)])
        full_promot = f"""Context from web Search : {context} 
        Question : {query}
        Please provide a comprehensives, detailed, well-sited using the above context.
        Ensure it answer the user query and don't use your own knowledge until it is very necessary.
        """
        # Generate text from a prompt
        response = self.client.generate_content(full_promot, stream=True)
        for chunk in response:
            yield chunk.text
        
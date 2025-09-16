from config import Settings
from tavily import TavilyClient
import trafilatura
settings = Settings()
tavilyClient = TavilyClient(api_key=settings.TAVILY_API_KEY)

class SearchService:
    def web_search(self, query: str):
        # Implementation of web search
        #response = self.tavily_client.search("Who is Leo Messi?")
        # print(response)
        print("Web Searching started")

        exctracted_content = []
        response = tavilyClient.search(query, max_results=6)
        response_results = response.get("results", [])
        for result in response_results:
            downloaded = trafilatura.fetch_url(result.get("url", ""))
            if downloaded:
                result_text = trafilatura.extract(downloaded,include_tables=True, include_comments=False)
                exctracted_content.append({"url": result.get("url", ""),
                                           "title": result.get("title", ""),
                                            "content": result_text})
        print("Web Searching ended")
        return exctracted_content
          
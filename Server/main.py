import asyncio
from PydanticModels.ChatModel import ChatModel
from Services.SearchService import SearchService
from Services.LLMService import GeminiService
from Services.SortSearchService import SortSearchService
from fastapi import FastAPI,WebSocket
from fastapi.middleware.cors import CORSMiddleware



app = FastAPI(title="My API", version="1.0.0")

searchService = SearchService()
sort_service = SortSearchService()
llm_service = GeminiService()

@app.get("/")
async def health_check():
    return {"message": "Health Check OK"}

# Web search endpoint

@app.websocket("/ws/chat")
async def web_socket_endpoint(websocket: WebSocket):
    await websocket.accept()
    send_lock = asyncio.Lock()
    current_task = None  # Keep track of currently running background task

    async def safe_send_json(payload: dict):
        async with send_lock:
            if websocket.client_state.name != "CONNECTED":
                return
            await websocket.send_json(payload)

    async def handle_query(query: str):
        """Handles one user query in a separate task"""
        try:
            search_results = searchService.web_search(query)
            sorted_results = sort_service.sort_results(query, search_results)

            if not sorted_results:
                await safe_send_json({"type": "error", "message": "No relevant documents found."})
                return

            for chunk in llm_service.generate_response_stream(query, sorted_results):
                await safe_send_json({"type": "content", "data": chunk})

        except Exception as e:
            await safe_send_json({"type": "error", "message": str(e)})

    try:
        while True:
            try:
                data = await websocket.receive_json()
            except Exception:
                break

            query = data.get("query", "")

            # Cancel the previous task if still running (optional)
            if current_task and not current_task.done():
                current_task.cancel()

            # Start a new task for this query
            current_task = asyncio.create_task(handle_query(query))

    finally:
        if websocket.client_state.name == "CONNECTED":
            await websocket.close()




@app.post("/chat")    
async def chat(body: ChatModel):
    # Search the internet for the query and transform the results into llm-friendly citations
    search_results = searchService.web_search(body.query)
    #print(f"Search Results: {search_results}")
    # Use an embedding model to embed the query
    # Sort citations by relevance
    sorted_results = sort_service.sort_results( body.query,search_results)
    if not sorted_results:
       return {"message": "No relevant documents found."}
    # generate a response using the citations by an LLM
    response = llm_service.generate_response(body.query, sorted_results)

    return {"response": response, 
            "citations": sorted_results}
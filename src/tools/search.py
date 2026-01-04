from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
from src.config import Config

def index_document(content: str, source: str) -> str:
    """
    Simulates indexing a document into Azure AI Search.
    In a real scenario, this would create a document payload and upload it.
    """
    try:
        # In a real app, you would define the schema and upload.
        # client = SearchClient(Config.AZURE_SEARCH_ENDPOINT, Config.AZURE_SEARCH_INDEX, AzureKeyCredential(Config.AZURE_SEARCH_KEY))
        # client.upload_documents(documents=[{"id": "...", "content": content, "source": source}])
        
        return f"Successfully indexed document from {source} into knowledge base '{Config.AZURE_SEARCH_INDEX}'."
    except Exception as e:
        return f"Error indexing document: {str(e)}"

def search_knowledge_base(query: str) -> str:
    """
    Searches the Azure AI Search index.
    """
    try:
        credential = AzureKeyCredential(Config.AZURE_SEARCH_KEY)
        client = SearchClient(Config.AZURE_SEARCH_ENDPOINT, Config.AZURE_SEARCH_INDEX, credential)
        results = client.search(search_text=query, top=2)
        
        output = []
        for result in results:
             output.append(str(result))
             
        if not output:
            return "No results found."
        return "\n".join(output)
    except Exception as e:
        return f"Search Error: {str(e)}"

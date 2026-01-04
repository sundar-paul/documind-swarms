from azure.core.credentials import AzureKeyCredential
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.ai.documentintelligence.models import AnalyzeResult
from src.config import Config

def analyze_document(document_url: str) -> str:
    """
    Uses Azure Document Intelligence (Prebuilt Layout) to analyze a document from a URL.
    Extracts text and structure.
    """
    try:
        credential = AzureKeyCredential(Config.AZURE_DOC_INTEL_KEY)
        client = DocumentIntelligenceClient(Config.AZURE_DOC_INTEL_ENDPOINT, credential)
        
        poller = client.begin_analyze_document(
            "prebuilt-layout",
            analyze_request={"url_source": document_url}
        )
        result: AnalyzeResult = poller.result()
        
        output = []
        if result.paragraphs:
            for paragraph in result.paragraphs:
                output.append(paragraph.content)
                
        full_text = "\n".join(output)
        return f"Document Analysis Result for {document_url}:\nLength: {len(full_text)} chars\nPreview: {full_text[:500]}...\n[Full content available in context]"
    except Exception as e:
        return f"Error analyzing document: {str(e)}"

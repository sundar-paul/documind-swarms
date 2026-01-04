import autogen
from src.agents.swarm import create_swarm
from src.config import Config
import sys

def main():
    print("Initializing DocuMind Neural Interface...")
    
    # Simple check for config existence (conceptually)
    # in prod, robust validation here
    
    input_node, vision_node, memory_node, logic_node = create_swarm()
    
    groupchat = autogen.GroupChat(
        agents=[input_node, vision_node, memory_node, logic_node], 
        messages=[], 
        max_round=10
    )
    
    manager = autogen.GroupChatManager(groupchat=groupchat, llm_config=Config.llm_config())

    # Demo Document URL (Microsoft Sample)
    sample_doc_url = "https://raw.githubusercontent.com/Azure-Samples/cognitive-services-REST-api-samples/master/curl/form-recognizer/sample-layout.pdf"
    
    directive = f"Process this asset: {sample_doc_url}. Analyze it, Index it, and then providing a Compliance Audit."
    
    print(f"Injecting Directive: {directive}")
    
    input_node.initiate_chat(
        manager,
        message=directive
    )

if __name__ == "__main__":
    main()

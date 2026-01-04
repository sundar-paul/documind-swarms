import autogen
from src.config import Config
from src.tools.doc_intel import analyze_document
from src.tools.search import index_document, search_knowledge_base

def create_swarm():
    config_list = Config.llm_config()

    # 1. Input Node (User Proxy)
    input_node = autogen.UserProxyAgent(
        name="Input_Node",
        system_message="A human administrator initializing the Neural Link.",
        code_execution_config={"last_n_messages": 2, "work_dir": "groupchat"},
        human_input_mode="TERMINATE"
    )

    # 2. Vision Node (Document Intelligence)
    vision_node = autogen.AssistantAgent(
        name="Vision_Node",
        system_message="""You are the Vision Node. Your sole purpose is to ingest digital assets.
        Use 'analyze_document' to extract raw data structure from document URLs provided by the Input Node.
        Output the extraction summary and pass control to the Memory Node.""",
        llm_config=config_list,
    )
    
    autogen.agentchat.register_function(
        analyze_document,
        caller=vision_node,
        executor=input_node,
        name="analyze_document",
        description="Analyses a document URL using Azure Document Intelligence."
    )

    # 3. Memory Node (Search Indexer)
    memory_node = autogen.AssistantAgent(
        name="Memory_Node",
        system_message="""You are the Memory Node. You sustain the long-term knowledge graph.
        Receive extracted content from the Vision Node.
        Use 'index_document' to commit this data to the Core Archive (Azure Search).
        Confirm successful storage to the Logic Node.""",
        llm_config=config_list,
    )

    autogen.agentchat.register_function(
        index_document,
        caller=memory_node,
        executor=input_node,
        name="index_document",
        description="Indexes content into the Azure Search Knowledge Base."
    )

    # 4. Logic Node (Analyst)
    logic_node = autogen.AssistantAgent(
        name="Logic_Node",
        system_message="""You are the Logic Node. You provide high-level cognitive processing.
        Once the Memory Node confirms indexing, you perform a compliance audit on the reported content.
        Identify any risks or missing fields based on standard business logic.""",
        llm_config=config_list,
    )

    return input_node, vision_node, memory_node, logic_node

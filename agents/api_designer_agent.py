from autogen.agentchat.contrib.multimodal_conversable_agent import MultimodalConversableAgent
from backend.gpt4all_client import GPT4AllClient

SYSTEM_MESSAGE = """
You are an expert backend API designer. Your job is to generate FastAPI routes and schemas based on requirements.
Provide clean, well-structured, and documented Python code only.
"""

class ApiDesignerAgent(MultimodalConversableAgent):
    def __init__(self):
        super().__init__(
            name="ApiDesigner",
            system_message=SYSTEM_MESSAGE,
            llm_config=False
        )
        self.model_client = GPT4AllClient()

    async def a_generate_reply(self, messages, sender=None):
        prompt = messages[-1]["content"] if messages else ""
        response = self.model_client.generate([{"role": "user", "content": prompt}])
        return response

def get_api_designer_agent():
    return ApiDesignerAgent()

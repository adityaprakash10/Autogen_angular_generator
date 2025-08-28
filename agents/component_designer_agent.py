from autogen.agentchat.contrib.multimodal_conversable_agent import MultimodalConversableAgent
from backend.gpt4all_client import GPT4AllClient

SYSTEM_MESSAGE = """
You are an expert frontend component designer. Your job is to generate Angular components based on UI requirements.
Write robust, reusable, modular, and well-styled Angular code only. Do not include any explanation.
"""

class ComponentDesignerAgent(MultimodalConversableAgent):
    def __init__(self):
        super().__init__(
            name="ComponentDesigner",
            system_message=SYSTEM_MESSAGE,
            llm_config=False  # Disable OpenAI client
        )
        self.model_client = GPT4AllClient()

    async def a_generate_reply(self, messages, sender=None):
        prompt = messages[-1]["content"] if messages else ""
        response = self.model_client.generate([{"role": "user", "content": prompt}])
        return response

def get_component_designer_agent():
    return ComponentDesignerAgent()

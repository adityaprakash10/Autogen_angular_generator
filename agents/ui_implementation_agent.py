from autogen.agentchat.contrib.multimodal_conversable_agent import MultimodalConversableAgent
from backend.gpt4all_client import GPT4AllClient

SYSTEM_MESSAGE = """
You are a UI implementation expert. Your task is to generate HTML and SCSS code for frontend UI.
Write clean, semantic, and well-styled code.
"""

class UiImplementationAgent(MultimodalConversableAgent):
    def __init__(self):
        super().__init__(
            name="UIImplementer",
            system_message=SYSTEM_MESSAGE,
            llm_config=False,
        )
        self.model_client = GPT4AllClient()

    async def a_generate_reply(self, messages, sender=None):
        prompt = messages[-1]["content"] if messages else ""
        response = self.model_client.generate([{"role": "user", "content": prompt}])
        return response

def get_ui_implementation_agent():
    return UiImplementationAgent()

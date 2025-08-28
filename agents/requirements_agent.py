from autogen.agentchat.contrib.multimodal_conversable_agent import MultimodalConversableAgent
from backend.gpt4all_client import GPT4AllClient

SYSTEM_MESSAGE = """
You are an expert requirements analyst. Your job is to analyze requirements documents and create structured detailed SRDs.
Respond clearly and concisely with no explanation.
"""

class RequirementsAnalyzerAgent(MultimodalConversableAgent):
    def __init__(self):
        super().__init__(
            name="RequirementsAnalyzer",
            system_message=SYSTEM_MESSAGE,
            llm_config=False
        )
        self.model_client = GPT4AllClient()

    async def a_generate_reply(self, messages, sender=None):
        prompt = messages[-1]["content"] if messages else ""
        response = self.model_client.generate([{"role": "user", "content": prompt}])
        return response

def get_requirements_analyzer_agent():
    return RequirementsAnalyzerAgent()

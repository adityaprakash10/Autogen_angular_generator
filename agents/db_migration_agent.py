from autogen.agentchat.contrib.multimodal_conversable_agent import MultimodalConversableAgent
from backend.gpt4all_client import GPT4AllClient

SYSTEM_MESSAGE = """
You are a database migration specialist. Your job is to generate migration scripts for the backend database.
Write clean migration code only.
"""

class DbMigrationAgent(MultimodalConversableAgent):
    def __init__(self):
        super().__init__(
            name="DbMigrationDeveloper",
            system_message=SYSTEM_MESSAGE,
            llm_config=False
        )
        self.model_client = GPT4AllClient()

    async def a_generate_reply(self, messages, sender=None):
        prompt = messages[-1]["content"] if messages else ""
        response = self.model_client.generate([{"role": "user", "content": prompt}])
        return response

def get_db_migration_agent():
    return DbMigrationAgent()

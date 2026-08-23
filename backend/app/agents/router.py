from app.agents.rag_agent import RAGAgent
from app.agents.land_agent import LandAgent


class AgentRouter:

    def __init__(self):

        self.rag_agent = RAGAgent()
        self.land_agent = LandAgent()


    def route(
        self,
        agent_type: str,
    ):

        if agent_type == "land":
            return self.land_agent

        return self.rag_agent
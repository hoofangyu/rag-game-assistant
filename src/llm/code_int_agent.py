from openai import OpenAI
from src.utils import OPENAI_API_KEY
from src.embeddings import EmbeddingGenerator
from src.llm.routing_agents import get_number_of_results_from_query

client = OpenAI(api_key = OPENAI_API_KEY)

class CodeAgent:
    def __init__(self, description_path = "data/games_description.csv", ranking_path = "data/games_ranking.csv"):
        """
        Initializes the RAG agent with a retriever and generator model.
        
        Args:
            vector_db (VectorDB): The vector database instance used to retrieve relevant game metadata.
        """
        #self.file_path = file_path
        self.description_file = client.files.create(
            file=open(description_path, "rb"),
            purpose='assistants'
        )

        self.ranking_file = client.files.create(
            file=open(ranking_path, "rb"),
            purpose='assistants'
        )

        self.assistant = client.beta.assistants.create(
            instructions="""
            You are a knowledgeable assistant answering questions about video games. When asked a question regarding games, 
            write and run code to answer the question.
            If you do not know the answer, do not use information outside of the context, 
            just respond with you do not know. Sound natural in your answer as well!
            """,
            model="gpt-4o",
            tools=[{"type": "code_interpreter"}],
            tool_resources={
                "code_interpreter": {
                "file_ids": [self.description_file.id, self.ranking_file.id]
            }}
        )

        self.thread = client.beta.threads.create()

    def generate_response(self, query, history):
        """
        Generates a response to the user query using the provided context.
        
        Args:
            query (str): The user's question or query.
            context (list of str): The list of retrieved metadata strings to use as context.
        
        Returns:
            str: The generated response from the language model.
        """
        
        message = client.beta.threads.messages.create(
            thread_id=self.thread.id,
            role="user",
            content=query,
            attachments = [
                {
                "file_id": self.description_file.id,
                "tools": [{"type": "code_interpreter"}]
                },
                {
                "file_id": self.ranking_file.id,
                "tools": [{"type": "code_interpreter"}]
                },
            ]
        )

        run = client.beta.threads.runs.create_and_poll(
            thread_id=self.thread.id,
            assistant_id=self.assistant.id
        )

        if run.status == 'completed': 
            messages = client.beta.threads.messages.list(
            thread_id=self.thread.id
            )
        else:
            print(run.status)


        return messages.data[0].content[0].text.value

    def answer_query(self, query, history = ""):
        """
        Combines retrieval and generation to answer the user's query.
        
        Args:
            query (str): The user's question or query.
        
        Returns:
            str: The generated response to the user's question.
        """
        response = self.generate_response(query, history)
        
        return response
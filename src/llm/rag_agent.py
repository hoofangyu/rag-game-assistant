from openai import OpenAI
from src.utils import OPENAI_API_KEY
from src.embeddings import EmbeddingGenerator
from src.llm.topk_agent import get_number_of_results_from_query

client = OpenAI(api_key = OPENAI_API_KEY)

class RAGAgent:
    def __init__(self, retriever, generator_model="gpt-4o-mini", max_context_length=20):
        """
        Initializes the RAG agent with a retriever and generator model.
        
        Args:
            vector_db (VectorDB): The vector database instance used to retrieve relevant game metadata.
            embedding_generator (EmbeddingGenerator): An instance of EmbeddingGenerator used to generate embeddings for the user query.
            generator_model (str): The OpenAI model to use for generating responses (default is "gpt-4o-mini").
            max_context_length (int): The maximum number of context items (game metadata entries) to retrieve for generating responses.
        """
        self.vector_db = retriever
        self.embedding_generator = EmbeddingGenerator()
        self.generator_model = generator_model
        self.max_context_length = max_context_length

    def retrieve_context(self, query):
        """
        Retrieves relevant game metadata based on the user query.
        
        Args:
            query (str): The user's question or query about games.
        
        Returns:
            list of str: A list of relevant metadata strings.
        """
        query_embedding = self.embedding_generator.get_embedding(query)
        k = get_number_of_results_from_query(query) + 2 # Give additional buffer
        retrieved_metadata = self.vector_db.search(query_embedding, k=k)
        return retrieved_metadata

    def generate_response(self, query, context, history):
        """
        Generates a response to the user query using the provided context.
        
        Args:
            query (str): The user's question or query.
            context (list of str): The list of retrieved metadata strings to use as context.
        
        Returns:
            str: The generated response from the language model.
        """
        context_text = "\n\n".join(context[:self.max_context_length]) # Keeping the context size small
        
        prompt = f"""
        You are a knowledgeable assistant answering questions about video games. Use the context below to answer the user's question accurately and informatively.
        If you do not know the answer, do not use information outside of the context, just respond with you do not know. Sound natural in your answer as well!
        
        Chat History:
        {history}

        Context:
        {context_text}
        
        Question: {query}
        
        Answer:
        """
        # Generate the response using OpenAI's API
        response = client.chat.completions.create(
            model=self.generator_model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant knowledgeable about video games."},
                {"role": "user", "content": prompt}
            ]
        )

        return response.choices[0].message.content.strip()

    def answer_query(self, query, history = ""):
        """
        Combines retrieval and generation to answer the user's query.
        
        Args:
            query (str): The user's question or query.
        
        Returns:
            str: The generated response to the user's question.
        """
        context = self.retrieve_context(query)
        response = self.generate_response(query, context, history)
        
        return response
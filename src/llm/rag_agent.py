from openai import OpenAI
from src.utils import OPENAI_API_KEY
from src.embeddings import EmbeddingGenerator
from src.llm.routing_agents import get_number_of_results_from_query
from sentence_transformers import CrossEncoder

client = OpenAI(api_key = OPENAI_API_KEY)

class RAGAgent:
    def __init__(self, retriever, generator_model="gpt-4o", cross_encoder_model = "cross-encoder/ms-marco-MiniLM-L-6-v2", max_context_length=20):
        """
        Initializes the RAG agent with a retriever and generator model.
        
        Args:
            vector_db (VectorDB): The vector database instance used to retrieve relevant game metadata.
            embedding_generator (EmbeddingGenerator): An instance of EmbeddingGenerator used to generate embeddings for the user query.
            generator_model (str): The OpenAI model to use for generating responses (default is "gpt-4o-mini").
            max_context_length (int): The maximum number of context items (game metadata entries) to retrieve for generating responses.
            cross_encoder_model (str): Cross Encoder Model to use
        """
        self.vector_db = retriever
        self.embedding_generator = EmbeddingGenerator()
        self.generator_model = generator_model
        self.max_context_length = max_context_length
        self.model = CrossEncoder(cross_encoder_model, max_length=512)

    def retrieve_context(self, query,k):
        """
        Retrieves relevant game metadata based on the user query.
        
        Args:
            query (str): The user's question or query about games.
        
        Returns:
            list of str: A list of relevant metadata strings.
        """
        query_embedding = self.embedding_generator.get_embedding(query)
        #k = get_number_of_results_from_query(query)*2
        retrieved_metadata = self.vector_db.search(query_embedding, k=k)
        return retrieved_metadata

    def rerank_context(self, query, context_ls):
        """
        This method takes a query and a list of contexts, computes relevance scores for each (query, context) pair, and returns the contexts sorted by their scores in descending order. The most relevant contexts are ranked higher.

        Args:
            query (str): The query string for which the contexts need to be reranked.
            context_ls (list of str): A list of candidate context strings retrieved initially.

        Returns:
            list of str: A list of contexts sorted by their relevance scores in descending order.
        """
        inputs = [(query,context) for context in context_ls]
        scores = self.model.predict(inputs)
        context_scores = list(zip(context_ls, scores))
        sorted_contexts = sorted(context_scores, key=lambda x: x[1], reverse=True)
        return [context[0] for context in sorted_contexts]
    
    def get_context(self, query):
        """ 
        This method retrieves an initial set of candidate contexts for a given query, reranks them based on relevance, and returns the top k most relevant contexts.

        Args:
            query (str): The query string for which the relevant contexts need to be retrieved.

        Returns:
            list of str: The top k most relevant contexts after reranking.
        """
        k = get_number_of_results_from_query(query)
        initial_context = self.retrieve_context(query,k*2)
        reranked_context = self.rerank_context(query, initial_context)
        return reranked_context[:k]

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
        context = self.get_context(query)
        response = self.generate_response(query, context, history)
        
        return response
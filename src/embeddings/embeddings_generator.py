from openai import OpenAI
from concurrent.futures import ThreadPoolExecutor
import numpy as np
from src.utils import OPENAI_API_KEY

client = OpenAI(api_key = OPENAI_API_KEY)

class EmbeddingGenerator:
    def __init__(self, model="text-embedding-3-small"):
        """
        Initializes the EmbeddingGenerator with the specified model.
        
        Args:
            model (str): The OpenAI model to use for generating embeddings.
        """
        self.model = model

    def get_embedding(self, text):
        """
        Generates an embedding for a given text using the OpenAI API.
        
        Args:
            text (str): The input text for which the embedding is to be generated.
        
        Returns:
            tuple: A tuple containing:
                - np.ndarray: The embedding for the text.
                - str: The original text.
            Returns (None) if there is an error in generating the embedding.
        """
        try:
            response = client.embeddings.create(
                input=text,
                model=self.model
            )
            embedding = response.data[0].embedding
            return np.array(embedding)
        except Exception as e:
            print(f"Error generating embedding: {e}")
            return None

    def generate_embeddings(self, texts):
        """
        Generates embeddings for a list of texts.

        Args:
            texts (list of str): A list of texts for which to generate embeddings.
        
        Returns:
            np.ndarray: A 2D NumPy array where each row is the embedding vector for the corresponding text in the input list.
                        If an embedding could not be generated for a text, it will contain a None value for that text.
        """
        with ThreadPoolExecutor() as executor:
            embeddings = list(executor.map(self.get_embedding, texts))
        return np.array(embeddings)
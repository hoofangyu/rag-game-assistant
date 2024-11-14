import faiss
import numpy as np

class VectorDB:
    def __init__(self, dimension=1536):
        """
        Initializes the FAISS index with the given vector dimension for cosine similarity.
        
        Args:
            dimension (int): The dimensionality of the embeddings (e.g., 1536 for OpenAI's ada model).
        """
        self.dimension = dimension
        self.index = faiss.IndexFlatIP(dimension)  
        self.metadata = []

    def add_embeddings(self, embeddings, metadata=None):
        """
        Normalizes embeddings to unit length and adds them to the FAISS index.
        
        Args:
            embeddings (2D np.ndarray): A 2D NumPy array where each row is the embedding vector for the corresponding text in the input list.+
            metadata (list): A list of original texts for each embedding
        """
        print("Adding Embeddings to VectorDB")
        self.index.add(embeddings)
        self.metadata.extend(metadata)
        print("Embeddings successfully added to VectorDB")

    def search(self, query_embedding, k=5):
        """
        Searches for the top-k nearest neighbors of the query embedding using cosine similarity.
        
        Args:
            query_embedding (np.ndarray): The embedding vector to search for (1D array).
            k (int): Number of nearest neighbors to return.
        
        Returns:
            list of str: A list of strings, i.e. the metadata for the each game
        """
        query_embedding = np.array([query_embedding])
        _, indices = self.index.search(query_embedding, k)
        results = [self.metadata[i] for i in indices[0]]
        return results

    def save_index(self, index_path="data/faiss_index.bin", metadata_path = "data/metadata.npy"):
        """
        Saves the FAISS index and metadata to disk.
        
        Args:
            index_path (str): File path to save the FAISS index.
            metadata_path (str): File path to save metadata
        """
        print("Saving VectorDB")

        faiss.write_index(self.index, index_path)
        np.save(metadata_path, self.metadata)

        print(f"Index saved to {index_path}")
        print(f"Metadata saved to {metadata_path}")
        print("Saving VectorDB saved")

    def load_index(self, index_path="data/faiss_index.bin", metadata_path = "data/metadata.npy"):
        """
        Loads the FAISS index and metadata from disk.
        
        Args:
            index_path (str): File path from which to load the FAISS index.
            metadata_path (str): File path from which to load the metadata

        """
        print("Loading VectorDB")
        self.index = faiss.read_index(index_path)
        self.metadata = np.load(metadata_path, allow_pickle=True).tolist()
        print(f"Index loaded from {index_path}")
        print(f"Metadata loaded from {metadata_path}")
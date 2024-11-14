from src.embeddings import DescriptionParser, EmbeddingGenerator, VectorDB

def main():
    vector_db = VectorDB()
    description_parser = DescriptionParser("data/games_description.csv")
    embedding_generator = EmbeddingGenerator()

    print("Parsing games description")
    descriptions = description_parser.parse()
    print("Games description parsed!")

    print("Generating Embeddings from game descriptions")
    embeddings = embedding_generator.generate_embeddings(descriptions)
    
    vector_db.add_embeddings(embeddings, descriptions)
    vector_db.save_index()

if __name__ == "__main__":
    main()
from src.embeddings import DescriptionParser, EmbeddingGenerator, VectorDB
import argparse

def main(file_path, ranking_path):
    vector_db = VectorDB()
    description_parser = DescriptionParser(file_path, ranking_path)
    embedding_generator = EmbeddingGenerator()

    print("Parsing games description")
    descriptions = description_parser.parse()
    print("Games description parsed!")

    print("Generating Embeddings from game descriptions")
    embeddings = embedding_generator.generate_embeddings(descriptions)
    
    vector_db.add_embeddings(embeddings, descriptions)
    vector_db.save_index()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate a vector database from a games description CSV file.")
    parser.add_argument(
        "--descriptions-path",
        type=str,
        required=True,
        help="Path to the games_description.csv file."
    )
    parser.add_argument(
        "--ranking-path",
        type=str,
        required=True,
        help="Path to the games_description.csv file."
    )
    args = parser.parse_args()
    main(args.descriptions_path, args.ranking_path)
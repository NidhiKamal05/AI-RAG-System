from settings.config import GAP, SIMILARITY_THRESHOLD

class Guard :
    def __init__(self) :
        pass
    
    def filter_chunks(self, retrieved_chunks) :
        distances = retrieved_chunks["distances"][0]
        documents = retrieved_chunks["documents"][0]
        metadatas = retrieved_chunks["metadatas"][0]

        raw_chunks = []
        filtered_chunks = []

        highest_similarity = 0  
        second_highest_similarity = 0
        gap = 0      

        for document, distance, metadata in zip(documents, distances, metadatas) :            
            similarity = 1 - distance

            raw_chunks.append({"document": document, "similarity": similarity, "metadata": metadata})

            if similarity > highest_similarity :
                second_highest_similarity = highest_similarity
                highest_similarity = similarity
            
            elif similarity > second_highest_similarity :
                second_highest_similarity = similarity
        
        gap = highest_similarity - second_highest_similarity

        for chunk in raw_chunks :
            similarity = chunk["similarity"]

            if similarity > SIMILARITY_THRESHOLD :
                if gap > GAP :
                    chunk["confidence"] = "HIGH"
                elif gap <= GAP :
                    chunk["confidence"] = "MEDIUM"
                filtered_chunks.append(chunk)
        
        filtered_chunks.sort(key = lambda x: x["similarity"], reverse = True)

        return filtered_chunks
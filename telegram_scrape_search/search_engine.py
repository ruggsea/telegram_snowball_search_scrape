import os
import sqlite3
from sentence_transformers import SentenceTransformer, util
from config.database_config import DB_NAME
import pandas as pd


# Create a connection to the SQLite database (go up one directory and then into data/)
db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), DB_NAME)
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Create a SentenceTransformer model for vector search
model = SentenceTransformer('distiluse-base-multilingual-cased-v1')
querystr = "SELECT message,date,links,views,message_url,toxicity_score FROM messages WHERE message LIKE '%{}%' AND length(message) > 25 ORDER BY toxicity_score,views DESC"
columns = ['message','date','links','views','message_url','toxicity_score']

def perform_normal_search(keyword):
    cursor.execute(querystr.format(keyword))
    result = cursor.fetchall()
    # make df from result
    df=pd.DataFrame(result, columns=columns)
    # sort df by toxicity_score
    df=df.sort_values(by=['toxicity_score'], ascending=False)
    return df
    

def perform_vector_search(query, top_n=5):
    "implement vector search using faiss"
    cursor.execute("SELECT message FROM messages")
    messages = cursor.fetchall()
    messages = [row[0] for row in messages]

    embeddings = model.encode(messages, convert_to_tensor=True)
    query_embedding = model.encode(query, convert_to_tensor=True)

    scores = util.pytorch_cos_sim(query_embedding, embeddings)[0]
    top_results = []

    for i in range(top_n):
        top_idx = scores.index(max(scores))
        top_results.append((messages[top_idx], scores[top_idx]))
        scores[top_idx] = -1  # Mark this as processed

    return top_results

# use main to test the search engine, return top 5 results
if __name__ == "__main__":
    while True:
        query = input("Enter your search query: ")
        if query == "exit":
            break
        normal_results = perform_normal_search(query)
        print(f"Results found: {len(normal_results)}")
        print("Top 5 normal Search Results:")
        for index,result in normal_results[:5].iterrows():
            print(result.message)
        # vector_results = perform_vector_search(query)
        # print("Top 5 vector Search Results:")
        # for result in vector_results[:5]:
        #     print(result.message)
        
        
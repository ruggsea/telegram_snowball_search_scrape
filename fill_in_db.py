import asyncio
from telegram_scrape_search.toxicity_scoring import get_toxicity_score, get_perspective_toxicity_score
from telegram_scrape_search.config.database_config import DB_NAME
import sqlite3
import os
from tqdm.asyncio import tqdm


async def main():
    """
    make sure that all the messages with len > 50 characters have a toxicity score
    """
    querystr = "SELECT message FROM messages WHERE length(message) > 28 AND toxicity_score IS NULL"
    
    # Create a connection to the SQLite database (go up one directory and then into data/)
    db_path = os.path.join("telegram_scrape_search/", DB_NAME)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(querystr)
    result = cursor.fetchall()
    i=0
    
    # choose the function to use
    print("Which function do you want to use?")
    print("1. get_toxicity_score")
    print("2. get_perspective_toxicity_score")
    choice = input("Enter 1 or 2: ")
    if choice == "1":
        func = get_toxicity_score
    elif choice == "2":
        func = get_perspective_toxicity_score
    else:
        print("Invalid choice")
        return
    
    score_list=[]
    async for row in tqdm(result, total=len(result), desc="Submitting messages"):
        message = row[0]
        # use a try, if rate limit is reached, wait 1 hour
        try:
            score= await asyncio.to_thread(func, message)
        except:
            print("Rate limit reached, waiting")
            await asyncio.sleep(3600)
            continue        # add the score to a list 
        score_list.append((score,message))
        i+=1
        if i % 100 == 0:
            print(f"Finished {i} messages")
            conn.commit()
        await asyncio.sleep(0.01) # add a sleep function to slow down the loop
            
    
    conn.commit()


if __name__ == '__main__':
    asyncio.run(main())

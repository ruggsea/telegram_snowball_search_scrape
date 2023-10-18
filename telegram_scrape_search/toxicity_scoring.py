import os
import requests
import json

from huggingface_hub import InferenceClient


def get_toxicity_score(text):
    """
    Returns a toxicity score for a given text
    """
    client = InferenceClient()

    result=client.text_classification(text=text, model="unitary/toxic-bert")
    return result[0]['score']




    
def get_perspective_toxicity_score(text):
    """
    Returns a toxicity score for a given text
    """
    url = ('https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze' +    
            '?key=' + os.environ['PERSPECTIVE_API_KEY'])
    data_dict = {
        'comment': {'text': text},
        'languages': ['en'],
        'requestedAttributes': {'TOXICITY': {}}
    }
    response = requests.post(url=url, data=json.dumps(data_dict))    
    response_dict = json.loads(response.content)
    try:
        return response_dict['attributeScores']['TOXICITY']['summaryScore']['value']
    except KeyError:
        print(f"Error in getting toxicity score, response: {response_dict}")

def main():
    """
    Main function
    """
    # make the user choose which function to use
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
    
    # get the text
    text = input("Enter the text: ")
    score = func(text)
    print(f"The toxicity score is {score}")
    
    
    

if __name__ == '__main__':
    main()
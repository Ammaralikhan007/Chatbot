import random
import json 
import torch
from model import NeuralNet
from nltk_utils import bag_of_words,tokenize

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu' )

with open('intents.json','r') as f:
    intents = json.load(f)

FILE = "data.pth" 
data = torch.load(FILE)

#Retrieves the saved sizes and vocabulary:
#model_state: trained weights

input_size = data["input_size"]
hidden_size = data["hidden_size"]
output_size = data["output_size"]
all_words = data["all_words"]
tags = data["tags"]
model_state = data["model_state"]

#Creates the same model architecture and loads the saved weights.
#Sets it to eval mode (used for inference, not training).

model = NeuralNet(input_size , hidden_size , output_size).to(device)
#loads the trained weights (also called parameters) into your model.
model.load_state_dict(model_state)
model.eval()

bot_name = "88 hours chatbot"

#now i want to crate a function thar gets a message and returns a response
def get_response(msg):
     #we want to tokenize sentence first before giving it to chatbot
    sentence = tokenize(msg)
    X = bag_of_words(sentence, all_words)
    # we have to reshape we give it one row we are taking one sample and one column
    X = X.reshape(1, X.shape[0])
    # then we want to convert it in torch tensor becuase our baag of words returns a numpy array
    X = torch.from_numpy(X)
    #Passes the input to the model → gets raw scores.
    output = model(X)
    #Picks the index of the highest score (the predicted intent).
    _, predicted = torch.max(output , dim=1)
    tag = tags[predicted.item()]
    #Applies softmax to get probabilities.
    probs = torch.softmax(output , dim=1)
    #Checks confidence of prediction.
    prob = probs[0][predicted.item()]
    if prob.item() > 0.75:
        for intent in intents["intents"]:
            if tag == intent["tag"]:
                 return random.choice(intent['responses'])
    
    return "sorry I dont understand...can you write something else"

# if __name__ == "__main__":
#     print("Let's chat! (type 'quit' to exit)")
#     while True:
#         # sentence = "do you use credit cards?"
#         sentence = input("You: ")
#         if sentence == "quit":
#             break

#         resp = get_response(sentence)
#         print(resp)



   
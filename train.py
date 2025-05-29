import json
from nltk_utils import tokenize, stem, bag_of_words  
import numpy as np
import torch
import torch.nn as nn
from torch.utils.data import Dataset ,DataLoader 
from model import NeuralNet


with open('intents.json', 'r') as f: # i am converting json data in dictionary format the with open ensures that the file is automatically closed after it is no longer needed
    intents = json.load(f)

# print(intents)

# now i will create a empty list to store all the words in a single structure

all_words = [] #collect all words
tags = [] # collect all tags in a list
xy = [] # this list will hold both patterns and tags later

for intent in intents['intents']: #now here i am interating through each object in intents the bracketed serves as a key baecuase we converted our json file in dictionary.
    tag = intent['tag']
    tags.append(tag) # i cratded a list named tags i accesing the value associated with the key tags and storing it in list named tags
    for pattern in intent['patterns']:
        w = tokenize(pattern)
        all_words.extend(w) #storing the tokenized patterns first in w then in a list named all words .extend() in Python is a list method used to add multiple elements from another iterable (like a list, tuple, or set) to the end of the current list.
        xy.append((w,tag))
    #up until now i have tokenized all the tags patters and stored them in a list xy
    #now i will lower and stem the words and remove punctuations 
#  now i will Remove unwanted punctuation.

# Applies stemming to simplify words.

# Removes duplicates.

# Sorts the list of words for consistency.

ignore_words = ['?' , '!' , '.' , ',' ,'-']
all_words = [stem(w) for w in all_words if w not in ignore_words]
all_words = sorted(set(all_words))
#now same logic for tags 
tags = sorted(set(tags))


#now 
# # tokenization and stemming is complete 
# lets create trining data and convert data in bag of words

X_train = [] #patterns
y_train = [] # my y train will be labels like in ML tags will have associated number with them since i tokenized

for (pattern_sentence,tag) in xy:
    bag = bag_of_words(pattern_sentence,all_words) #putted my vectorized patterns and all words list which are already numbers in X_train 
    X_train.append(bag) 

    label = tags.index(tag) # craeted numbers for our labels 
    y_train.append(label) #cross entropy loss

X_train = np.array(X_train)
y_train = np.array(y_train)


    #i will do subclassing now
    # creating my own dataset
    #inherits from pytotch utils dataset

class ChatDataset(Dataset):
    def __init__(self):
           
        self.n_samples = len(X_train)
        self.x_data = X_train
        self.y_data = y_train
       
        #Dataset[idx]
        

        # PyTorch gets a single sample by index.
    def __getitem__(self, index):
        return self.x_data[index], self.y_data[index]  

    #PyTorch needs to know how many total samples are in the dataset.
    def __len__(self):
        return self.n_samples
#With this custom dataset, we can now easily load data in batches like this:


#hyperparameter tuning

# PyTorch's DataLoader is a helper class that makes it easy to:
# Load data in batches
# Shuffle the data each epoch
# Use parallel processing for faster loading

batch_size = 8
hidden_size = 8
output_size = len(tags)
input_size = len(X_train[0])
learning_rate = 0.001
num_epochs = 700





dataset = ChatDataset()
#train_loader will give you data in mini-batches
train_loader = DataLoader(dataset=dataset, batch_size = batch_size, shuffle=True, num_workers=0) #num_workers controls how many CPU processes load data in parallel.
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu' )
model = NeuralNet(input_size , hidden_size , output_size).to(device)

#loss and optimizer

criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters() , lr=learning_rate)

for epoch in range(num_epochs):
    for (words , labels) in train_loader:
        words = words.to(device)
        labels = labels.to(device, dtype=torch.int64)

        #forward pass

        outputs = model(words)
        loss = criterion(outputs , labels)

        #backpropogation and optimizer step

        optimizer.zero_grad() #Clears previous gradients.
        loss.backward() #Computes gradients.
        optimizer.step() #Updates model weights.

    if (epoch + 1) % 100 == 0:
        print(f'epoch {epoch + 1} / {num_epochs}, loss={loss.item(): .4f}')
           
print(f'final loss, loss={loss.item():.4f}')

data = {
    "model_state": model.state_dict(),
    "input_size": input_size,
    "output_size": output_size,
    "hidden_size": hidden_size,
    "all_words": all_words,
    "tags": tags

}

FILE = "data.pth"
torch.save(data , FILE)

print(f'training complete. file saved to {FILE}')











     


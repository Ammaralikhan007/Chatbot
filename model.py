import torch
import torch.nn as nn

class NeuralNet(nn.Module):
    
    def __init__(self,input_size ,hidden_size , num_classes):
        super(NeuralNet , self).__init__()
        self.l1 = nn.Linear(input_size , hidden_size)
        self.l2 = nn.Linear(hidden_size , hidden_size)
        self.l3 = nn.Linear(hidden_size , num_classes)
        #Activation Function
        #im using relu
        self.relu = nn.ReLU()


    def forward(self , x):
        out = self.l1(x)
        out = self.relu(out)
        out = self.l2(out)
        out = self.relu(out)
        out = self.l3(out)
        #no more activation and no softmax jjust get ouput from l3
        return out





        
                



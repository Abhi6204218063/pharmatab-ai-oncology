"""
PharmaTab Deep Learning Drug Response Predictor
"""

import torch
import torch.nn as nn
import torch.optim as optim


class DrugResponseNet(nn.Module):

    def __init__(self, input_size=5):

        super(DrugResponseNet, self).__init__()

        self.model = nn.Sequential(
            nn.Linear(input_size, 32),
            nn.ReLU(),

            nn.Linear(32, 32),
            nn.ReLU(),

            nn.Linear(32, 1),
            nn.Sigmoid()
        )

    def forward(self, x):

        return self.model(x)


class DrugResponseTrainer:

    def __init__(self, input_size=5):

        self.device = torch.device(
            "cuda" if torch.cuda.is_available() else "cpu"
        )

        self.model = DrugResponseNet(input_size).to(self.device)

        self.loss_fn = nn.BCELoss()

        self.optimizer = optim.Adam(
            self.model.parameters(),
            lr=0.001
        )


    def train(self, X, y, epochs=50):

        X = torch.tensor(X, dtype=torch.float32).to(self.device)
        y = torch.tensor(y, dtype=torch.float32).to(self.device)

        for epoch in range(epochs):

            preds = self.model(X)

            loss = self.loss_fn(preds, y)

            self.optimizer.zero_grad()

            loss.backward()

            self.optimizer.step()

            if epoch % 10 == 0:

                print("Epoch:", epoch, "Loss:", loss.item())


    def predict(self, X):

        X = torch.tensor(X, dtype=torch.float32).to(self.device)

        with torch.no_grad():

            return self.model(X).cpu().numpy()
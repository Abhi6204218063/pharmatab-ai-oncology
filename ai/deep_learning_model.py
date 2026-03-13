"""
PharmaTab Deep Learning Model
GPU-enabled tumor prediction
"""

import torch
import torch.nn as nn
import torch.optim as optim


class TumorNet(nn.Module):

    def __init__(self):

        super(TumorNet, self).__init__()

        self.model = nn.Sequential(

            nn.Linear(3, 32),
            nn.ReLU(),

            nn.Linear(32, 32),
            nn.ReLU(),

            nn.Linear(32, 1)

        )

    def forward(self, x):

        return self.model(x)


class TumorTrainer:

    def __init__(self):

        self.device = torch.device(
            "cuda" if torch.cuda.is_available() else "cpu"
        )

        self.model = TumorNet().to(self.device)

        self.loss_fn = nn.MSELoss()

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
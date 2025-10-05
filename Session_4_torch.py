import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset
import numpy as np
import matplotlib.pyplot as plt

# Reproducibility
torch.manual_seed(42)
np.random.seed(42)

# Generate synthetic binary classification data
n_samples = 1000
X = torch.randn(n_samples, 2)
true_w = torch.tensor([[2.0], [-3.0]])
true_b = 0.5

# Linear combination + noise
logits = X @ true_w + true_b
probs = torch.sigmoid(logits)
y = torch.bernoulli(probs).view(-1, 1)  # Binary labels (0 or 1)

# Create dataset and dataloader
dataset = TensorDataset(X, y)
batch_size = 64
dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=True)

# Define Logistic Regression Model
class LogisticRegression(nn.Module):
    def __init__(self, input_dim):
        super(LogisticRegression, self).__init__()
        self.linear = nn.Linear(input_dim, 1)
    
    def forward(self, x):
        return torch.sigmoid(self.linear(x))

# Initialize model, loss, optimizer
model = LogisticRegression(input_dim=2)
criterion = nn.BCELoss()
optimizer = optim.SGD(model.parameters(), lr=0.1)

# Training parameters
num_epochs = 1000
train_losses = []
train_accuracies = []

# Training loop
for epoch in range(num_epochs):
    total_loss = 0.0
    correct = 0
    total = 0
    
    for batch_X, batch_y in dataloader:
        # Forward pass
        outputs = model(batch_X)
        loss = criterion(outputs, batch_y)
        
        # Backward pass
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        
        total_loss += loss.item()
        
        # Calculate accuracy
        predicted = (outputs > 0.5).float()
        correct += (predicted == batch_y).sum().item()
        total += batch_y.size(0)
    
    avg_loss = total_loss / len(dataloader)
    accuracy = correct / total
    train_losses.append(avg_loss)
    train_accuracies.append(accuracy)

# Plot results
plt.figure(figsize=(12, 5))

# Training Loss Plot
plt.subplot(1, 2, 1)
plt.plot(train_losses, 'b-', linewidth=2, label='Training Loss')
plt.title('Training Loss Over Time', fontsize=14)
plt.xlabel('Epoch')
plt.ylabel('Binary Cross-Entropy Loss')
plt.legend()

# Training Accuracy Plot
plt.subplot(1, 2, 2)
plt.plot(train_accuracies, 'g-', linewidth=2, label='Training Accuracy')
plt.title('Training Accuracy Over Time', fontsize=14)
plt.xlabel('Epoch')
plt.ylabel('Accuracy')
plt.ylim(0, 1)
plt.legend()

plt.tight_layout()
plt.show()

# Final metrics
print(f"Final Training Loss: {train_losses[-1]:.4f}")
print(f"Final Training Accuracy: {train_accuracies[-1]*100:.2f}%")

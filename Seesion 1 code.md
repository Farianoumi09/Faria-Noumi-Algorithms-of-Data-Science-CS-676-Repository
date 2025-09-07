# Import necessary libraries
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

# Read the CSV file
df = pd.read_csv('/content/sample_data/california_housing_train.csv')

# Separate features (X) and target variable (y)
X = df.drop('median_house_value', axis=1)  # Features
y = df['median_house_value']  # Target variable
ß
# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Create and train the linear regression model
model = LinearRegression()
model.fit(X_train, y_train)

# Make predictions on the test set
y_pred = model.predict(X_test)

# Evaluate the model
mse = mean_squared_error(y_test, y_pred)
rmse = np.sqrt(mse)
r2 = r2_score(y_test, y_pred)

# Print the results
print('Model Performance:')
print(f'Root Mean Squared Error: ${rmse:.2f}')
print(f'R-squared Score: {r2:.4f}')

# Print feature importance (coefficients)
feature_importance = pd.DataFrame({
    'Feature': X.columns,
    'Coefficient': model.coef_
})
print('\nFeature Importance:')
print(feature_importance.sort_values(by='Coefficient', key=abs, ascending=False))

# Import necessary libraries
import pandas as pd
import numpy as np
import statsmodels.api as sm
from sklearn.model_selection import train_test_split

# Read the CSV file
df = pd.read_csv('/content/sample_data/california_housing_train.csv')

# Separate features (X) and target variable (y)
X = df.drop('median_house_value', axis=1)  # Features
y = df['median_house_value']  # Target variable

# Add constant term to the features
X = sm.add_constant(X)

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Fit the model
model = sm.OLS(y_train, X_train).fit()

# Make predictions
y_pred = model.predict(X_test)

# Print model summary
print(model.summary())

# Create a DataFrame with feature importance metrics
feature_importance = pd.DataFrame({
    'Feature': X.columns,
    'Coefficient': model.params,
    't_statistic': model.tvalues,
    'p_value': model.pvalues
})

# Sort by absolute t-statistic values
feature_importance_sorted = feature_importance.sort_values(by='t_statistic', key=abs, ascending=False)

print("\nFeature Importance based on t-statistics:")
print(feature_importance_sorted)

# Calculate R-squared and adjusted R-squared
print(f"\nR-squared: {model.rsquared:.4f}")
print(f"Adjusted R-squared: {model.rsquared_adj:.4f}")

# Calculate RMSE
rmse = np.sqrt(np.mean((y_test - y_pred) ** 2))
print(f"Root Mean Squared Error: ${rmse:.2f}")


import pandas as pd
import matplotlib.pyplot as plt

# Read the data
df = pd.read_csv('/content/sample_data/california_housing_train.csv')

# Create the scatter plot
plt.figure(figsize=(15, 10))

# Create scatter plot with circles
scatter = plt.scatter(df['longitude'], 
                     df['latitude'],
                     c=df['median_house_value'],  # Color based on house value
                     s=df['median_house_value']/5000,  # Size based on house value
                     alpha=0.5,
                     cmap='viridis')

# Add colorbar
plt.colorbar(scatter, label='Median House Value ($)')

# Customize the plot
plt.title('California Housing Prices')
plt.xlabel('Longitude')
plt.ylabel('Latitude')

# Add grid
plt.grid(True, alpha=0.3)

# Adjust layout
plt.tight_layout()

# Show the plot
plt.show()
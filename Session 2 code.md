import pandas as pd
import numpy as np

# Create fake data
data = {
    'Original_Text': [
        "How satisfied were you with our customer service?",
        "What do you think about our new product features?",
        "Would you recommend our services to others?",
        "How easy was it to navigate our website?",
        "Rate your overall experience with our company.",
        "How likely are you to purchase from us again?",
        "Was our product delivery time satisfactory?",
        "How would you rate the quality of our product?",
        "Did our support team resolve your issues effectively?",
        "How clear was our product documentation?"
    ],
    'Response_Text': [
        "The customer service was excellent and very helpful",
        "The new features are innovative but need some improvements",
        "Yes, I would definitely recommend to my colleagues",
        "The website is user-friendly and well-organized",
        "Overall experience has been positive",
        "Very likely to make future purchases",
        "Delivery was faster than expected",
        "Product quality exceeds expectations",
        "Support team was knowledgeable and efficient",
        "Documentation was comprehensive but could be clearer"
    ],
    'Score': [
        np.random.randint(70, 101) for _ in range(10)  # Random scores between 70 and 100
    ]
}

# Create DataFrame
df = pd.DataFrame(data)

# Export to CSV
df.to_csv('feedback_data.csv', index=False)

# Display the first few rows of the DataFrame
print(df.head())
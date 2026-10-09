import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score
import pickle

# Load dataset
df = pd.read_csv('tourism_data.csv')
print(f"Dataset loaded: {len(df)} rows")
print(df.head())

# Encode categorical columns
le_country     = LabelEncoder()
le_category    = LabelEncoder()
le_season      = LabelEncoder()
le_destination = LabelEncoder()

df['country_enc']     = le_country.fit_transform(df['country'])
df['category_enc']    = le_category.fit_transform(df['category'])
df['season_enc']      = le_season.fit_transform(df['season'])
df['destination_enc'] = le_destination.fit_transform(df['destination'])

# Features and label
X = df[['country_enc', 'category_enc', 'season_enc']]
y = df['destination_enc']

# Split 80/20
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Train Random Forest
rf = RandomForestClassifier(n_estimators=100, random_state=42)
rf.fit(X_train, y_train)

rf_acc = accuracy_score(y_test, rf.predict(X_test))
print(f"\n===== RESULTS =====")
print(f"Random Forest Accuracy: {rf_acc * 100:.2f}%")
print(f"Training samples: {len(X_train)}")
print(f"Testing samples:  {len(X_test)}")
print(f"===================")

# Save model + encoders
with open('model.pkl', 'wb') as f:
    pickle.dump(rf, f)

encoders = {
    'country':     le_country,
    'category':    le_category,
    'season':      le_season,
    'destination': le_destination,
}
with open('encoders.pkl', 'wb') as f:
    pickle.dump(encoders, f)

print("\nSaved: model.pkl, encoders.pkl")
print("Supported countries:", list(le_country.classes_))
# =========================
# Phishing Website Detection
# =========================

# 1️⃣ Import Libraries
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# 2️⃣ Feature Extraction Function (5 features ONLY)
def extract_features(url):
    return [
        len(url),                      # url_len
        url.count('.'),                # dot_cnt
        1 if '@' in url else 0,         # has_at
        1 if '-' in url else 0,         # has_hyphen
        1 if url.startswith('https') else 0  # is_https
    ]

# Feature names (MATCH EXACTLY)
feature_names = [
    "url_len",
    "dot_cnt",
    "has_at",
    "has_hyphen",
    "is_https"
]

# 3️⃣ Load Dataset
data = pd.read_csv(r"C:\cyberproject\dataset.csv")

# 4️⃣ Prepare Features & Labels
X = data["url"].apply(extract_features)
X = pd.DataFrame(X.tolist(), columns=feature_names)
y = data["label"]

# 5️⃣ Train-Test Split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# 6️⃣ Train Model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# 7️⃣ Evaluate Model
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"Model Accuracy: {accuracy * 100:.2f}%")

# 8️⃣ Prediction Function (USED BY FLASK)
def predict_single_url(url):
    features = extract_features(url)
    features_df = pd.DataFrame([features], columns=feature_names)
    result = model.predict(features_df)
    return "⚠️ Phishing Website" if result[0] == 1 else "✅ Legitimate Website"

# 9️⃣ Test Example (CLI)
if __name__ == "__main__":
    test_url = "http://secure-login-paypal.com"
    print(f"URL: {test_url} --> {predict_single_url(test_url)}")

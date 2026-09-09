import pandas as pd

df = pd.read_csv("beneficiary_data.csv")
print(df.head())
print(df.shape) 















from sklearn.preprocessing import LabelEncoder

feature_cols = ["education_level", "family_occupation", "mobility_constraint", "interest_area"]
target_col = "NSQF_trade_label"

encoders = {}
for col in feature_cols + [target_col]:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col])
    encoders[col] = le

print(df.head())






from sklearn.model_selection import train_test_split

X = df[feature_cols]
y = df[target_col]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print("Train size:", len(X_train))
print("Test size:", len(X_test))







from sklearn.ensemble import RandomForestClassifier

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)
print("Model trained successfully!")




from sklearn.metrics import accuracy_score, classification_report

y_pred = model.predict(X_test)
print("Accuracy:", accuracy_score(y_test, y_pred))
print(classification_report(y_test, y_pred, zero_division=0))






sample = pd.DataFrame([{
    "education_level": encoders["education_level"].transform(["8th pass"])[0],
    "family_occupation": encoders["family_occupation"].transform(["Weaving"])[0],
    "mobility_constraint": encoders["mobility_constraint"].transform(["Low"])[0],
    "interest_area": encoders["interest_area"].transform(["Tailoring"])[0],
}])

prediction = model.predict(sample)
predicted_trade = encoders["NSQF_trade_label"].inverse_transform(prediction)
print("Recommended trade:", predicted_trade[0])






import joblib

joblib.dump(model, "model.pkl")
joblib.dump(encoders, "encoders.pkl")
print("Saved model.pkl and encoders.pkl")
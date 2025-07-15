# ml/model.py
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score

class KeyPredictor:
    def __init__(self):
        self.vectorizer = CountVectorizer(analyzer='char', ngram_range=(1, 3))
        self.model = RandomForestClassifier()

    def load_data(self, csv_path):
        df = pd.read_csv(csv_path)
        X = df['ciphertext']
        y = df['key']
        return X, y

    def train(self, X, y):
        X_vec = self.vectorizer.fit_transform(X)
        X_train, X_test, y_train, y_test = train_test_split(X_vec, y, test_size=0.2, random_state=42)

        self.model.fit(X_train, y_train)
        y_pred = self.model.predict(X_test)

        print("Accuracy:", accuracy_score(y_test, y_pred))
        print("Classification Report:\n", classification_report(y_test, y_pred))

    def predict(self, ciphertext):
        vec = self.vectorizer.transform([ciphertext])
        return self.model.predict(vec)[0]

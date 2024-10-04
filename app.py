from flask import Flask, request, jsonify
import pandas as pd

app = Flask(__name__)

# Sample sentiment word lists (you can expand these)
positive_words = {"great", "fantastic", "amazing", "satisfied", "excellent", "love", "recommend", "worth", "pleased", "happy"}
negative_words = {"poor", "bad", "terrible", "disappointed", "waste", "broke", "not", "cheap", "frustrating", "awful"}

def analyze_sentiment(reviews):
    sentiment_scores = {"positive": 0, "negative": 0, "neutral": 0}

    for review in reviews:
        score = 0
        words = review.lower().split()
        for word in words:
            if word in positive_words:
                score += 1
            elif word in negative_words:
                score -= 1
        
        if score > 0:
            sentiment_scores["positive"] += 1
        elif score < 0:
            sentiment_scores["negative"] += 1
        else:
            sentiment_scores["neutral"] += 1

    return sentiment_scores

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']
    
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    # Process the file based on its extension
    if file.filename.endswith('.csv'):
        df = pd.read_csv(file)
    elif file.filename.endswith('.xlsx'):
        df = pd.read_excel(file)
    else:
        return jsonify({"error": "Invalid file format"}), 400

    # Extract review text
    reviews = df['Review'].tolist()
    
    # Analyze sentiment
    sentiment_scores = analyze_sentiment(reviews)
    
    return jsonify(sentiment_scores)

if __name__ == '__main__':
    app.run(debug=True)

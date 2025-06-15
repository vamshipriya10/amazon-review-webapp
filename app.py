import pandas as pd
from flask import Flask, render_template
import matplotlib.pyplot as plt
import os

app = Flask(__name__)

@app.route("/")
def home():
    try:
        # Use relative path or give absolute path below
        df = pd.read_csv("amazon_reviews.csv")
        df.columns = df.columns.str.strip()  # Remove any extra spaces in column names
    except Exception as e:
        return f"<h2>Error reading CSV: {e}</h2>"

    # Basic statistics using correct column name
    avg_rating = round(df['rating'].mean(), 2)
    max_rating = df['rating'].max()
    min_rating = df['rating'].min()
    total_reviews = len(df)

    # Generate bar chart for rating distribution
    plt.figure(figsize=(6, 4))
    df['rating'].value_counts().sort_index().plot(kind='bar', color='skyblue')
    plt.title('Review Count by Rating')
    plt.xlabel('Rating')
    plt.ylabel('Count')
    plt.tight_layout()

    # Save plot to static folder
    if not os.path.exists('static'):
        os.makedirs('static')
    plt.savefig('static/rating_plot.png')
    plt.close()

    return render_template("index.html",
                           avg_rating=avg_rating,
                           max_rating=max_rating,
                           min_rating=min_rating,
                           total_reviews=total_reviews)

if __name__ == "__main__":
    app.run(debug=True)
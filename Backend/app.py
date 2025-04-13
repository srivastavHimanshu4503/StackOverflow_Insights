from flask import Flask, jsonify
from flask_cors import CORS
import pandas as pd
import os

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return "<h1>Welcome to the home directory of the backend and Flask is running successful</h1>"

@app.route('/api/top-tags-normalized')
def top_tags_normalized():
    df = pd.read_csv('E:/Sitare Learnings/Sem 2/DHP/StackOverflow_Assignment/Backend/top_tags_normalized.csv')

    # Create a dictionary of years -> top 10 tags with their normalized frequency
    result = {}
    for year in sorted(df['Year'].unique()):
        top_tags = df[df['Year'] == year].sort_values(by='NormalizedFrequency', ascending=False).head(10)
        result[str(year)] = {
            'tags': top_tags['Tag'].tolist(),
            'values': (top_tags['NormalizedFrequency'] * 100).round(2).tolist()
        }

    return jsonify(result)

@app.route('/api/tag-trends-over-time')
def tag_trends_over_time():
    df = pd.read_csv('E:/Sitare Learnings/Sem 2/DHP/StackOverflow_Assignment/Backend/tag_trends_over_time.csv')

    years = df['Year'].tolist()
    tags = df.columns[1:]  # Skip 'Year' column

    datasets = []
    for tag in tags:
        tag_values = df[tag].round(2).tolist()
        datasets.append({
            'label': tag,
            'data': tag_values,
            'fill': False
        })

    return jsonify({
        'labels': years,
        'datasets': datasets
    })

@app.route('/api/tag-distribution/<int:year>')
@app.route('/api/tag-distribution', defaults={'year': 2024})  # Default to 2024
def tag_distribution(year):
    try:
        csv_path = f'tag_distribution_{year}.csv'

        df = pd.read_csv(csv_path).sort_values(by='NormalizedFrequency', ascending=False).head(10)

        result = {
            'labels': df['Tag'].tolist(),
            'data': df['NormalizedFrequency'].round(2).tolist()
        }
        return jsonify(result)

    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/api/tag-uniqueness')
def tag_uniqueness():
    df = pd.read_csv('E:/Sitare Learnings/Sem 2/DHP/StackOverflow_Assignment/Backend/unique_vs_repeated_tags.csv')

    result = {
        'labels': df['Year'].astype(str).tolist(),
        'datasets': [
            {
                'label': 'Unique Tags (%)',
                'data': df['PercentUnique'].round(2).tolist(),
                'backgroundColor': 'rgba(75, 192, 192, 0.7)'
            },
            {
                'label': 'Repeated Tags (%)',
                'data': df['PercentRepeated'].round(2).tolist(),
                'backgroundColor': 'rgba(255, 99, 132, 0.7)'
            }
        ]
    }

    return jsonify(result)

@app.route('/tags_per_question_distribution')
def tags_per_question_distribution():
    df = pd.read_csv('E:/Sitare Learnings/Sem 2/DHP/StackOverflow_Assignment/Backend/tags_per_question_distribution.csv')

    data = {
        'labels': list(df['TagsPerQuestion']),  # Example: [1, 2, 3, 4, 5]
        'datasets': [{
            'label': 'Number of Questions',
            'data': list(df['QuestionCount']),
            'backgroundColor': 'rgba(153, 102, 255, 0.6)'
        }]
    }
    return jsonify(data)


if __name__ == '__main__':
    app.run(debug=True)
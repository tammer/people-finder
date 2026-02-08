from flask import Flask, render_template_string

import supa

app = Flask(__name__)


@app.route("/")
def index():
    print("Getting all scores")
    rows = supa.get_all_scores()
    print(f"Found {len(rows)} rows")
    return render_template_string(
        """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <title>Scores</title>
            <link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
        </head>
        <body>
        <h1>Scores</h1>
        <div class="scores-table-wrap">
        <table>
        <thead>
            <tr>
                <th>id</th>
                <th>model_id</th>
                <th>score</th>
                <th>created_at</th>
                <th>LinkedIn</th>
                <th>analysis</th>
            </tr>
        </thead>
        <tbody>
        {% for row in rows %}
            <tr>
                <td>{{ row.id }}</td>
                <td>{{ row.model_id }}</td>
                <td>{{ row.score | round(0) | int }}</td>
                <td>{{ row.created_at }}</td>
                <td>
                {% if row.analysis and row.analysis.get('LinkedIn URL') %}
                    <a href="{{ row.analysis['LinkedIn URL'] }}" target="_blank" rel="noopener noreferrer">{{ row.response.get('full_name') if row.response and row.response.get('full_name') else 'Profile' }}</a>
                {% else %}
                    —
                {% endif %}
                </td>
                <td><pre>{% if row.analysis and row.analysis.get('justification') %}{{ row.analysis.get('justification') }}{% else %}{{ row.analysis | tojson(indent=2) if row.analysis else '' }}{% endif %}</pre></td>
            </tr>
        {% endfor %}
        </tbody>
        </table>
        </div>
        <p class="scores-count">{{ rows | length }} row(s)</p>
        </body>
        </html>
        """,
        rows=rows,
    )


if __name__ == "__main__":
    app.run(debug=True)

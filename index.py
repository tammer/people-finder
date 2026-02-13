import os
from datetime import datetime
from zoneinfo import ZoneInfo

from flask import Flask, render_template_string

import my_dotenv
import supa
from craft_message import craft_message

my_dotenv.load_dotenv()

app = Flask(__name__)


def _human_date(iso_str):
    if not iso_str:
        return ""
    try:
        dt = datetime.fromisoformat(iso_str.replace("Z", "+00:00"))
        tz_name = os.getenv("TZ", "").strip()
        if tz_name:
            try:
                dt = dt.astimezone(ZoneInfo(tz_name))
            except Exception:
                dt = dt.astimezone()
        else:
            dt = dt.astimezone()
        return dt.strftime("%b %d, %Y, %I:%M %p")
    except (ValueError, TypeError):
        return iso_str


app.jinja_env.filters["human_date"] = _human_date


@app.route("/invites")
def invites():
    rows = supa.get_invites()
    return render_template_string(
        """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <title>Invites</title>
            <link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
        </head>
        <body>
        <h1>Invites</h1>
        <p>Sorted by accepted_at (oldest first).</p>
        <div class="scores-table-wrap">
        <table>
        <thead>
            <tr>
                <th>id</th>
                <th>invite_sent_at</th>
                <th>accepted_at</th>
                <th>messaged_at</th>
                <th>LinkedIn</th>
                <th></th>
            </tr>
        </thead>
        <tbody>
        {% for row in rows %}
            <tr>
                <td>{{ row.id }}</td>
                <td>{{ row.invite_sent_at | human_date }}</td>
                <td>{{ row.accepted_at | human_date }}</td>
                <td>{{ row.messaged_at | human_date }}</td>
                <td>
                {% if row.responses and row.responses.li_url %}
                    <a href="{{ row.responses.li_url }}" target="_blank" rel="noopener noreferrer">{{ (row.responses.response or {}).get('full_name') or 'Profile' }}</a>
                {% else %}
                    —
                {% endif %}
                </td>
                <td><a href="{{ url_for('compose', id=row.id) }}" target="_blank" rel="noopener noreferrer"><button type="button">Compose</button></a></td>
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


@app.route("/compose/<int:id>")
def compose(id):
    output = craft_message(id)
    if output is None:
        return render_template_string(
            "<!DOCTYPE html><html><body><p>No response found for this ID.</p></body></html>"
        ), 404
    return render_template_string(
        """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <title>Compose</title>
            <link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
        </head>
        <body>
        <h1>Compose</h1>
        <p id="copy-status" style="font-size: 0.875rem; color: #64748b; margin-bottom: 0.5rem;"></p>
        <div style="width: 65ch; max-width: 100%;">
        <pre id="compose-output" style="white-space: pre-wrap; word-break: break-word;">{{ output }}</pre>
        </div>
        <script>
        (function() {
            var text = {{ output | tojson }};
            var status = document.getElementById('copy-status');
            if (navigator.clipboard && navigator.clipboard.writeText) {
                navigator.clipboard.writeText(text).then(function() {
                    status.textContent = 'Copied to clipboard.';
                }).catch(function() {
                    status.textContent = 'Could not copy to clipboard.';
                });
            } else {
                status.textContent = 'Clipboard not available.';
            }
        })();
        </script>
        </body>
        </html>
        """,
        output=output,
    )


if __name__ == "__main__":
    app.run(debug=True)

import werkzeug.urls
from urllib.parse import quote

# Patch werkzeug.urls to include a url_quote function
werkzeug.urls.url_quote = quote

from flask import Flask, request, jsonify
import subprocess
import json

app = Flask(__name__)

@app.route('/get_hls_url', methods=['GET'])
def get_hls_url():
    channel_name = request.args.get('channel')
    if not channel_name:
        return jsonify({"error": "Channel name is required"}), 400

    try:
        # Run Streamlink to fetch the HLS URL for the provided channel
        result = subprocess.run(
            ["streamlink", "--json", f"https://twitch.tv/{channel_name}", "best"],
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            return jsonify({"error": "Failed to fetch HLS URL", "details": result.stderr}), 500

        # Parse the JSON response from Streamlink
        stream_data = json.loads(result.stdout)
        hls_url = list(stream_data["streams"].values())[0]["url"]
        return jsonify({"hls_url": hls_url})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

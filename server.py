import werkzeug.urls
from urllib.parse import quote
# Patch werkzeug.urls to include a url_quote function
werkzeug.urls.url_quote = quote
import streamlink
from flask import Flask, request, jsonify
import re

app = Flask(__name__)

@app.route("/get-stream", methods=["POST"])
def get_stream():
    data = request.get_json()
    twitch_username = data.get("username", "").strip()

    if not twitch_username:
        return jsonify({"error": "No Twitch username provided"}), 400

    # Construct the Twitch stream URL from the username
    twitch_url = f"https://www.twitch.tv/{twitch_username}"

    try:
        # Get the available streams from Streamlink
        streams = streamlink.streams('hls', twitch_url)
        
        # Get the best quality stream (you can adjust this if necessary)
        best_stream = streams.get("worst")
        
        if best_stream:
            return jsonify({"stream_url": best_stream.url})
        else:
            return jsonify({"error": "No stream found for the provided username"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

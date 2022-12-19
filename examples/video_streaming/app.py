import os, re
import argparse
from flask import Flask, request, Response, render_template


def handle_byte_range_request(video_path, request, max_chunk_size=1024 * 1024 * 10):
    start_byte, end_byte = 0, None
    range_header = request.headers.get("Range", None)

    if range_header:
        # Extract the start and end bytes from the Range header
        match = re.search(r"(\d+)-(\d*)", range_header)
        groups = match.groups()
        if groups[0]:
            start_byte = int(groups[0])
        if groups[1]:
            end_byte = int(groups[1])

    file_size = os.path.getsize(video_path)

    if end_byte is None:
        end_byte = min(start_byte + max_chunk_size, file_size - 1)

    chunk_size = end_byte - start_byte + 1

    with open(video_path, "rb") as f:
        f.seek(start_byte)
        chunk = f.read(chunk_size)

    headers = {
        "Accept-Ranges": "bytes",
        "Content-Length": len(chunk),
        "Content-Range": f"bytes {start_byte}-{end_byte}/{file_size}",
    }

    return Response(
        chunk,
        206,
        mimetype="video/mp4",
        direct_passthrough=True,
        headers=headers,
    )


app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html", title="Video Streaming", video_url="/video")


@app.route("/video")
def serve_video():
    video_path = args["video"]

    if os.path.exists(video_path) is False:
        return {"error": "video file does not exist"}, 404

    return handle_byte_range_request(video_path, request)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("-v", "--video", help="video file", required=True)
    ap.add_argument(
        "-p", "--port", type=int, default=8080, help="port number", required=False
    )
    args = vars(ap.parse_args())

    if os.path.exists(args["video"]) is False:
        print("video file does not exist")
        exit()

    app.run(host="0.0.0.0", port=args["port"], debug=False, threaded=True)

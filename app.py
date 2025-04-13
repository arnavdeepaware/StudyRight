from flask import Flask, redirect, request

app = Flask(__name__)

@app.route('/stream-video', methods=['GET'])
def stream_video():
    presigned_url = request.args.get('url')
    if not presigned_url:
        return {'error': 'Missing presigned URL'}, 400

    return redirect(presigned_url, code=302)  # 302 Found: temporary redirect

if __name__ == '__main__':
    app.run(debug=True, port = 5000)
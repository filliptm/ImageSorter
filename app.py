import os
import json
import shutil
from flask import Flask, request, jsonify, send_from_directory, render_template_string
import argparse

app = Flask(__name__)

SETTINGS_FILE = 'settings.json'

def load_settings():
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, 'r') as f:
            return json.load(f)
    return {
        'input_dir': 'input',
        'good_dir': 'good',
        'bad_dir': 'bad',
        'image_count': 20,
        'image_size': 200
    }

def save_settings(settings):
    with open(SETTINGS_FILE, 'w') as f:
        json.dump(settings, f)

SETTINGS = load_settings()
PROCESSED_IMAGES = set()

@app.route('/')
def index():
    with open('index.html', 'r', encoding='utf-8') as f:
        return render_template_string(f.read())


@app.route('/settings', methods=['GET', 'POST'])
def handle_settings():
    global SETTINGS
    if request.method == 'POST':
        SETTINGS.update(request.json)
        save_settings(SETTINGS)
        return jsonify({"success": True})
    else:
        return jsonify(SETTINGS)


@app.route('/images', methods=['GET'])
def get_images():
    count = int(request.args.get('count', SETTINGS['image_count']))
    # Always get the current list of images from the directory
    try:
        all_images = set(os.listdir(SETTINGS['input_dir']))
        unprocessed_images = list(all_images - PROCESSED_IMAGES)
        # Sort the images to ensure consistent ordering
        unprocessed_images.sort()
        batch = unprocessed_images[:count]
        return jsonify({
            'images': batch,
            'total_available': len(unprocessed_images)
        })
    except Exception as e:
        return jsonify({
            'error': str(e),
            'images': [],
            'total_available': 0
        }), 500


@app.route('/submit', methods=['POST'])
def submit_selection():
    global PROCESSED_IMAGES
    displayed_images = request.json['displayed']
    selected = request.json['selected']

    for image in displayed_images:
        source = os.path.join(SETTINGS['input_dir'], image)
        if image in selected:
            destination = os.path.join(SETTINGS['good_dir'], image)
        else:
            destination = os.path.join(SETTINGS['bad_dir'], image)
        shutil.move(source, destination)
        PROCESSED_IMAGES.add(image)

    return jsonify({"success": True})


@app.route('/image/<path:filename>')
def serve_image(filename):
    return send_from_directory(SETTINGS['input_dir'], filename)


@app.route('/reset', methods=['POST'])
def reset_processed():
    global PROCESSED_IMAGES
    PROCESSED_IMAGES = set()
    return jsonify({"success": True})


@app.route('/counts', methods=['GET'])
def get_counts():
    return jsonify({
        'input': len(os.listdir(SETTINGS['input_dir'])),
        'good': len(os.listdir(SETTINGS['good_dir'])),
        'bad': len(os.listdir(SETTINGS['bad_dir']))
    })


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Run the Image Sorter server")
    parser.add_argument('--host', default='0.0.0.0', help="The host to bind the server to")
    parser.add_argument('--port', type=int, default=5000, help="The port to bind the server to")
    args = parser.parse_args()

    print(f"Starting server on {args.host}:{args.port}")
    app.run(host=args.host, port=args.port, debug=True)
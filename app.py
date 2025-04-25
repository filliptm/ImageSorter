import os
import json
import shutil
from flask import Flask, request, jsonify, send_from_directory, render_template_string
import argparse
import pathlib

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
    all_images = set(os.listdir(SETTINGS['input_dir']))
    unprocessed_images = list(all_images - PROCESSED_IMAGES)
    batch = unprocessed_images[:count]
    return jsonify(batch)


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


@app.route('/list_directories', methods=['GET'])
def list_directories():
    current = request.args.get('current', '')
    
    # Handle empty path or invalid path
    if not current or not os.path.exists(current):
        # Default to current working directory if path is invalid
        current = os.getcwd()
    
    # Ensure the path is a directory
    if not os.path.isdir(current):
        current = os.path.dirname(current)
    
    # Get absolute path
    current_abs = os.path.abspath(current)
    
    # Get parent directory
    parent = os.path.dirname(current_abs) if current_abs != os.path.dirname(current_abs) else None
    
    # List directories
    try:
        directories = []
        for item in os.listdir(current_abs):
            item_path = os.path.join(current_abs, item)
            if os.path.isdir(item_path):
                directories.append({
                    'name': item,
                    'path': item_path
                })
        
        # Sort directories alphabetically
        directories.sort(key=lambda x: x['name'].lower())
        
        return jsonify({
            'current_path': current_abs,
            'parent': parent,
            'directories': directories
        })
    except Exception as e:
        return jsonify({
            'error': str(e),
            'current_path': current_abs,
            'parent': parent,
            'directories': []
        }), 500


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Run the Image Sorter server")
    parser.add_argument('--host', default='0.0.0.0', help="The host to bind the server to")
    parser.add_argument('--port', type=int, default=5000, help="The port to bind the server to")
    args = parser.parse_args()

    print(f"Starting server on {args.host}:{args.port}")
    app.run(host=args.host, port=args.port, debug=True)
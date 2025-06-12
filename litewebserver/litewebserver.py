import os
from flask import Flask, render_template, request, redirect, url_for, send_from_directory, abort
from werkzeug.utils import secure_filename
from datetime import datetime

app = Flask(__name__)

# --- Configuration ---
BASE_SERVED_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), 'served_data'))
app.config['UPLOAD_FOLDER'] = BASE_SERVED_DIR  # Files will be uploaded into subdirs of BASE_SERVED_DIR
app.config['SECRET_KEY'] = 'supersecretkey' # For flash messages, if we add them later

# Ensure BASE_SERVED_DIR exists
if not os.path.exists(BASE_SERVED_DIR):
    os.makedirs(BASE_SERVED_DIR)

# --- Helper Functions ---
def get_path_details(base_path, subpath=""):
    """
    Validates and constructs paths. Returns the absolute current directory,
    and checks if it's within the allowed base_path.
    """
    current_dir_abs = os.path.abspath(os.path.join(base_path, subpath.strip('/')))

    # Security Check: Ensure the path is within BASE_SERVED_DIR
    if not current_dir_abs.startswith(base_path):
        abort(403) # Forbidden

    # Ensure the directory actually exists, especially if subpath is manually entered
    if not os.path.exists(current_dir_abs) or not os.path.isdir(current_dir_abs):
        abort(404) # Not Found

    return current_dir_abs

# --- Routes ---
@app.route('/')
@app.route('/browse/')
@app.route('/browse/<path:subpath>')
def browse_files(subpath=""):
    current_dir_abs = get_path_details(BASE_SERVED_DIR, subpath)

    items = []
    try:
        for item_name in os.listdir(current_dir_abs):
            item_path = os.path.join(current_dir_abs, item_name)
            item_type = 'directory' if os.path.isdir(item_path) else 'file'
            item_size = os.path.getsize(item_path) if item_type == 'file' else None
            item_modified_timestamp = os.path.getmtime(item_path)
            item_modified = datetime.fromtimestamp(item_modified_timestamp).strftime('%Y-%m-%d %H:%M:%S')

            items.append({
                'name': item_name,
                'type': item_type,
                'size': item_size,
                'last_modified': item_modified,
                'path': os.path.join(subpath, item_name).strip('/') # Relative path for links
            })
    except PermissionError:
        abort(403) # Or handle more gracefully

    # Sort items: directories first, then by name
    items.sort(key=lambda x: (x['type'] == 'file', x['name'].lower()))

    parent_dir_display = None
    current_path_display = subpath.strip('/')

    if current_dir_abs != BASE_SERVED_DIR:
        parent_subpath = os.path.dirname(subpath.strip('/'))
        parent_dir_display = parent_subpath if parent_subpath else "" # Link to root if parent is root

    return render_template('index.html',
                           items=items,
                           current_path_display=current_path_display,
                           parent_dir_display=parent_dir_display)

@app.route('/download/<path:filepath>')
def download_file(filepath):
    # filepath is relative to BASE_SERVED_DIR
    abs_filepath = os.path.abspath(os.path.join(BASE_SERVED_DIR, filepath.strip('/')))

    # Security Check: Ensure the file is within BASE_SERVED_DIR
    if not abs_filepath.startswith(BASE_SERVED_DIR) or not os.path.isfile(abs_filepath):
        abort(403) # Or 404 if preferred for non-existent but valid-looking paths

    directory = os.path.dirname(filepath.strip('/'))
    filename = os.path.basename(filepath.strip('/'))

    return send_from_directory(
        directory=os.path.join(BASE_SERVED_DIR, directory),
        path=filename,  # send_from_directory expects 'path' to be the filename
        as_attachment=True
    )

@app.route('/upload', methods=['POST'])
def upload_file():
    target_subdir = request.form.get('current_subdir', '').strip('/')
    upload_to_dir_abs = get_path_details(BASE_SERVED_DIR, target_subdir) # Validates and gets abs path

    if 'file' not in request.files:
        # Handle error - redirect or flash message
        return redirect(url_for('browse_files', subpath=target_subdir))

    file = request.files['file']
    if file.filename == '':
        # Handle error - redirect or flash message
        return redirect(url_for('browse_files', subpath=target_subdir))

    if file:
        filename = secure_filename(file.filename)
        try:
            file.save(os.path.join(upload_to_dir_abs, filename))
        except PermissionError:
            abort(403) # Or handle more gracefully
        except Exception as e:
            # Log the exception e
            abort(500) # Internal server error

    return redirect(url_for('browse_files', subpath=target_subdir))

# --- Error Handlers ---
@app.errorhandler(403)
def forbidden(error):
    return render_template('403.html', error=error), 403

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html', error=error), 404

@app.errorhandler(500)
def internal_error(error):
    # It's good practice to log the error here
    return render_template('500.html', error=error), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)

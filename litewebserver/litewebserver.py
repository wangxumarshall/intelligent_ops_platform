import os
from flask import Flask, render_template, request, redirect, url_for, send_from_directory, abort, flash
from werkzeug.utils import secure_filename
from datetime import datetime

app = Flask(__name__)

# --- Configuration ---
BASE_SERVED_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), 'served_data'))
app.config['UPLOAD_FOLDER'] = BASE_SERVED_DIR  # Files will be uploaded into subdirs of BASE_SERVED_DIR
app.config['BASE_SERVED_DIR'] = BASE_SERVED_DIR # <--- ADD THIS LINE
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
def main_portal():
    return render_template('main_portal.html')

@app.route('/scheduler_graph_tool/')
def serve_scheduler_graph():
    return render_template('scheduler_graph.html')

@app.route('/board.html')
def board():
    return render_template('board.html')

@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory(os.path.join(app.root_path, 'static'), filename)

@app.route('/browse/')
@app.route('/browse/<path:subpath>')
def browse_files(subpath=""):
    current_dir_abs = get_path_details(app.config['BASE_SERVED_DIR'], subpath)

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

    if current_dir_abs != app.config['BASE_SERVED_DIR']:
        parent_subpath = os.path.dirname(subpath.strip('/'))
        parent_dir_display = parent_subpath if parent_subpath else "" # Link to root if parent is root

    return render_template('data_brower.html',
                           items=items,
                           current_path_display=current_path_display,
                           parent_dir_display=parent_dir_display)

@app.route('/download/<path:filepath>')
def download_file(filepath):
    # filepath is relative to BASE_SERVED_DIR
    abs_filepath = os.path.abspath(os.path.join(app.config['BASE_SERVED_DIR'], filepath.strip('/')))

    # Security Check: Ensure the file is within BASE_SERVED_DIR
    if not abs_filepath.startswith(app.config['BASE_SERVED_DIR']) or not os.path.isfile(abs_filepath):
        abort(403) # Or 404 if preferred for non-existent but valid-looking paths

    directory = os.path.dirname(filepath.strip('/'))
    filename = os.path.basename(filepath.strip('/'))

    return send_from_directory(
        directory=os.path.join(app.config['BASE_SERVED_DIR'], directory),
        path=filename,  # send_from_directory expects 'path' to be the filename
        as_attachment=True
    )

@app.route('/upload', methods=['POST'])
def upload_file():
    target_subdir = request.form.get('current_subdir', '').strip('/')
    upload_to_dir_abs = get_path_details(app.config['BASE_SERVED_DIR'], target_subdir) # Validates and gets abs path

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

@app.route('/create_folder', methods=['POST'])
def create_folder():
    current_subdir = request.form.get('current_subdir', '')
    new_folder_name_raw = request.form.get('new_folder_name', '').strip()

    # Validate folder name
    if not new_folder_name_raw:
        # flash("Folder name cannot be empty.", "error") # Optional: for future flash messages
        print("Error: Folder name cannot be empty.") # Log error
        return redirect(url_for('browse_files', subpath=current_subdir))

    # Sanitize folder name
    new_folder_name = secure_filename(new_folder_name_raw)
    if new_folder_name != new_folder_name_raw or '/' in new_folder_name_raw or '\\' in new_folder_name_raw:
        # Check if secure_filename changed it significantly or if it contained invalid chars
        # flash("Invalid characters in folder name.", "error")
        print(f"Error: Invalid characters in folder name: {new_folder_name_raw}")
        return redirect(url_for('browse_files', subpath=current_subdir))

    if not new_folder_name: # Handles cases like ".." or "." becoming empty after secure_filename
            # flash("Invalid folder name.", "error")
        print(f"Error: Invalid folder name after sanitization: {new_folder_name_raw}")
        return redirect(url_for('browse_files', subpath=current_subdir))


    target_parent_dir = os.path.join(app.config['BASE_SERVED_DIR'], current_subdir)
    target_parent_dir = os.path.abspath(target_parent_dir)

    # Security check: Ensure target parent is within BASE_SERVED_DIR
    if not target_parent_dir.startswith(os.path.abspath(app.config['BASE_SERVED_DIR'])):
        # flash("Invalid path.", "error")
        print("Error: Invalid path for folder creation (parent directory out of bounds).")
        return redirect(url_for('browse_files', subpath='')) # Redirect to root

    new_folder_path = os.path.join(target_parent_dir, new_folder_name)
    new_folder_path = os.path.abspath(new_folder_path) # Normalize

    # Additional security check: ensure the new folder itself doesn't escape BASE_SERVED_DIR (e.g. if new_folder_name was '..')
    # This is somewhat redundant due to secure_filename and the previous check, but good for defense in depth.
    if not new_folder_path.startswith(os.path.abspath(app.config['BASE_SERVED_DIR'])):
        # flash("Invalid folder name leading to path escape.", "error")
        print("Error: Invalid folder name leading to path escape.")
        return redirect(url_for('browse_files', subpath=current_subdir))

    try:
        os.mkdir(new_folder_path)
        # flash(f"Folder '{new_folder_name}' created successfully.", "success")
        print(f"Folder '{new_folder_path}' created successfully.")
    except FileExistsError:
        # flash(f"Folder '{new_folder_name}' already exists.", "warning")
        print(f"Warning: Folder '{new_folder_path}' already exists.")
    except OSError as e:
        # flash(f"Error creating folder: {e.strerror}", "error")
        print(f"Error creating folder '{new_folder_path}': {e}")

    return redirect(url_for('browse_files', subpath=current_subdir))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)

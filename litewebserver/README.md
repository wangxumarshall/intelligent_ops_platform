# LiteWebServer - Flask Edition

A lightweight, standalone web service built with Python and Flask to browse, upload, and download files. It mimics some basic FTP-like functionalities through a web interface.

## Features

-   **File & Directory Listing**: View files and folders in a specified server directory (`served_data/` by default).
-   **Subdirectory Navigation**: Navigate into subdirectories and back to parent directories.
-   **File Downloads**: Download files directly from the server.
-   **File Uploads**: Upload files to the currently viewed directory.
-   **Detailed Information**: Shows file name, type (file/folder), size, and last modified date.
-   **Web Interface**: All interactions are through a web browser.
-   **Decoupled Backend/Frontend**: Uses Flask for backend logic and HTML templates for the frontend.

## Prerequisites

-   Python 3.7+
-   pip (Python package installer)

## Setup & Usage

1.  **Navigate to the `litewebserver` directory:**
    ```bash
    cd litewebserver
    ```

2.  **Create a virtual environment (recommended):**
    ```bash
    python -m venv venv
    ```
    Activate it:
    *   On Windows:
        ```bash
        .\venv\Scripts\activate
        ```
    *   On macOS/Linux:
        ```bash
        source venv/bin/activate
        ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Run the server:**
    ```bash
    python litewebserver.py
    ```
    The server will start by default on `http://0.0.0.0:8080`.

5.  **Access the server:**
    Open your web browser and go to `http://localhost:8080/` (or `http://<your-server-ip>:8080/` if accessing from another machine).

## Configuration

-   **Served Directory**: By default, files are served from the `litewebserver/served_data/` directory. You can add files and folders there to make them accessible. Uploaded files will also be placed within this directory structure.
-   **Templates**: HTML templates are located in `litewebserver/templates/`.
-   **Host/Port**: The server runs on `0.0.0.0` (all available network interfaces) and port `8080`. This can be changed in the `app.run(...)` call at the end of `litewebserver.py`.

## Project Structure

-   `litewebserver.py`: The main Flask application file.
-   `requirements.txt`: Python dependencies (Flask).
-   `templates/`: Contains HTML templates for rendering pages (index, errors).
    -   `index.html`: Main page for browsing files and directories.
    -   `403.html`, `404.html`, `500.html`: Error pages.
-   `served_data/`: The default root directory for serving and uploading files. You need to create this directory if it doesn't exist or populate it with files you want to serve initially.
-   `README.md`: This file.

## Development

To modify or extend the server:
-   Edit `litewebserver.py` for backend logic changes.
-   Edit files in `templates/` for frontend presentation changes.
-   The Flask development server will automatically reload most Python code changes. For template changes, a browser refresh is usually sufficient.

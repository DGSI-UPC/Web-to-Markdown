# Web-to-Markdown
The purpose of this project is to be able to convert the information from any website into a Markdown bucket.

## Usage
This website has a UI with a text field in the middle. Enter the base URL of the website you want to extract information from and it will automatically find all the attached links to it and also extract information from them.

To extract this information we get the HTML using the library trafilatura and parse it using BeautifulSoup and html2text.

## Features
- **Web Interface:** simple and efficient to enter the root URL from which we will be extracting information from.
- **Multiple URL scanning:** it does not only get information from the website entered but from all the other links attached to it.
- **Clear API usage:** the name of the endpoints clearly reflect their usage to easily make use of it.

## Requirements
1. Python: Python 3.7 or higher is recommended. Check your version:
    ```bash
    python --version  # or python3 --version
    ```

2. Python Packages: Install the required libraries via pip:
    ```bash
    pip install -r requirements.txt
    ```
   Ensure your requirements.txt file contains:
   ```python
   fastapi
   uvicorn
   requests
   pydantic
   requests
   trafilatura
   beautifulsoup4
   lxml_html_clean
   html2text
   ```

## Installation and setup
1.  **Clone the Repository (Optional):**
    ```bash
    git clone <repository_url>
    cd <repository_directory>
    ```
    (Skip this if you have the files directly.)

2.  **Create `index.html`:** Make sure the `index.html` file is in the same directory as `main.py`.

3.  **Run the Application with Uvicorn:**
    ```bash
    uvicorn main:app --reload --host 0.0.0.0 --port 8000
    ```
    *   `main:app`:  Adjust if your Python file or app instance have different names.
    *   `--reload`:  Enables auto-reloading on code changes (great for development).
    *   `--host 0.0.0.0`:  Allows access from other devices on your network.  Remove for local-only access.
    *   `--port 8000`:  Change if you need a different port.

5.  **Access the Application:** Open your browser:
    *   **Locally:** `http://localhost:8000`
    *   **From another device:** `http://<your_server_ip>:8000`

## API Documentation
This API provides two endpoints for submitting the URL entered and checking the status of the Markdown bucket, respectively.

- **Endpoint:** `/submit-url/`
    - **Method:** `POST`
    - **Request:**
        - `Content-Type`: `text/plain`
        - `Form field`: (Required) the base URL to extract information from.
    - **Response:**
        - **Success (Status Code: 200 OK):**
            - `Content-Type`: `application/json`
            - The response body contains the id of the processing requested.
        - **Error (Status Codes: 400, 500):**
            - `Content-Type`: `application/json`
            - Body: A JSON object containing an error description:
                ```JSON
                {
                    "detail": "Error message describing the problem."
                }
                ```
- **Endpoint:** `/check-status/`
    - **Method:** `GET`
    - **Request:**
        - `Content-Type`: `text/plain`
        - `Form field`:
            - (Required) The base URL to extract information from.
            - (Required) The id of the task that has been requested previously.
    - **Response:**
        - **Success (Status Code: 200 OK):**
            - `Content-Type`: `application/json`
            - The response body contains the status of the request.
        - **Error (Status Codes: 400, 500):**
            - `Content-Type`: `application/json`
            - Body: A JSON object containing an error description:
                ```JSON
                {
                    "detail": "Error message describing the problem."
                }
                ```
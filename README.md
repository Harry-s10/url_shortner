# URL Shortener API

A simple and efficient URL shortener API built with **FastAPI**. The API allows users to shorten long URLs, retrieve
original URLs, and provides basic analytics for shortened URLS.

## Features 🌟

- **Shorten a URL**: Create a shortened version of a long URL.
- **Redirect**: Retrieve and redirect to the original URL using the shortened URL.
- **URL Expiry**: URLs can have an expiry date, after which they will no longer be accessible.
- **Analytics**: Track the number of times a shortened URL is accessed.

## Technologies Used 🛠️

- **FastAPI**: For building the API.
- **SQLite/PostgreSQL**: Database to store the URLs.
- **Pydantic**: For data validation.
- **Uvicorn**: ASGI server to run the FastAPI app.

## Getting Started 🏁

Follow these instructions to set up and run the project locally.

### Prerequisites 📋

- **Python 3.8+**: Make sure Python is installed on your machine.
- **FastAPI**: Install FastAPI and Uvicorn by running the following command:
    ```bash
  pip install fastapi uvicorn
    ```

### Project Setup ⚙️

1. Clone the Repository:
    ```bash
    git clone
   cd url-shortener
    ```
2. **Install Dependencies**: Install the required Python packages using `pip`:
    ```bash
    pip install -r requirements.txt
   ```
3. **Database Setup**:
    - By default, the API uses SQLite for simplicity, but you can modify it to use PostgreSQL or any other database.
    - If using SQLite, the database will be created automatically when you run the app.
4. **Set Up Environment Variables**: Create a `.env` file in the project root to store sensitive data (like secret keys)
   and database configuration:
    ```ini
   SECRET_KEY=your_jwt_secret_ke🔗y
   DATABASE_URL=sqlite:///./shortener.db # Or your PostgreSQL URL
   BASE_URL=http://localhost:8000
   ```

### Running the Application ▶️

To start the FastAPI server, run the following command:

```bash
uvicorn main:app --reload
```

- The API will be available at `http://127.0.0.1:8000`
- The interactive API docs will be accessible at: `http://127.0.0.1:8000/docs`.

## API Endpoints 🔗

### URL Shortening

- **POST /shorten**: Shorten a long URL.
    - Request Body:
      ```json
      {
          "url": "https://www.example.com/long-url"
      }
      ```
    - Response:
      ```json
      {
          "short_url": "http://localhost:8000/abc123"
      }
      ```

### URL Redirection

- **GET /{short_url}**: Redirect to the original URL.

    - Example: `http://localhost:8000/abc123` redirects to the original URL.

### Analytics

- **GET /analytics/{short_url}**: Get analytics for a shortened URL (e.g., number of clicks).

    - Response:
  ```json
  {
    "clicks": 10,
    "url": "https://www.example.com/long-url"
  }
  ```

### Error Handling

- **404 Not Found**: If a short URL does not exist or has expired.
- **400 Bad Request**: If the provided URL is invalid.

## Environment Variable ⚙️

The following environment variables should be defined in your `.env` file:

- `SECRET_KEY`: A secret key for securing JWT tokens.
- `DATABASE_URL`: URL to connect to the database (e.g., SQLite or PostgreSQL).
- `BASE_URL`: The base URL of the app for generating shortened URLs.

## Database Models 🗄️

1. URL Model:

    - **id**: Auto-generated unique ID for each URL entry.
    - **original_url**: The long URL provided by the user.
    - **short_url**: The unique short URL.
    - **expiry**: Expiry of the shortened URL.
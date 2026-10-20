# Quizly Backend

Quizly automatically creates a quiz from a YouTube video. The backend downloads the audio track, transcribes it with Whisper, and uses Gemini to generate a quiz containing ten questions.

## Features

- User registration, login, token refresh, and logout
- JWT authentication using HttpOnly cookies
- Quiz generation from a YouTube URL
- Audio transcription with Whisper
- Generation of ten questions with Gemini
- Validation and storage of generated quiz data
- View, edit, and delete personal quizzes
- User-specific quiz access

## Technologies

- Python and Django
- Django REST Framework
- Simple JWT
- SQLite
- yt-dlp and FFmpeg
- OpenAI Whisper
- Google Gemini API

## Requirements

- Python
- FFmpeg installed globally
- A Google Gemini API key
- The Quizly frontend to use the application in a browser

FFmpeg can be installed on Windows with Winget:

```powershell
winget install --id Gyan.FFmpeg --exact
```

Verify the installation:

```powershell
ffmpeg -version
```

## Installation

Clone the repository and open the project directory:

```powershell
git clone https://github.com/Kasa28/Quizly.git
cd Quizly
```

Create and activate a virtual environment:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

Install the dependencies:

```powershell
pip install -r requirements.txt
```

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_api_key
```

The `.env` file is excluded by `.gitignore` and must not be uploaded to GitHub.

Apply the database migrations:

```powershell
python manage.py migrate
```

Optionally create an administrator account:

```powershell
python manage.py createsuperuser
```

## Running the Application

Start the backend:

```powershell
python manage.py runserver
```

The API is available at `http://127.0.0.1:8000/api/`. The Django admin panel is available at `http://127.0.0.1:8000/admin/`.

The frontend must be started with a local web server, such as the Live Server extension for Visual Studio Code, on port `5500`.

## API Endpoints

| Method | Endpoint | Description |
| --- | --- | --- |
| `POST` | `/api/register/` | Register a user |
| `POST` | `/api/login/` | Log in and set JWT cookies |
| `POST` | `/api/token/refresh/` | Refresh the access token |
| `POST` | `/api/logout/` | Log out and blacklist the refresh token |
| `GET` | `/api/quizzes/` | Retrieve the user's quizzes |
| `POST` | `/api/quizzes/` | Generate a quiz from a YouTube URL |
| `GET` | `/api/quizzes/<id>/` | Retrieve a quiz and its questions |
| `PATCH` | `/api/quizzes/<id>/` | Update a quiz title or description |
| `DELETE` | `/api/quizzes/<id>/` | Delete a quiz |

### Authentication Cookies

Authentication uses the `access_token` and `refresh_token` JWT cookies. Both cookies are HttpOnly, which prevents JavaScript from reading their values. The browser sends them automatically with API requests when credentials are enabled in the frontend.

- Login sets the access and refresh cookies.
- Token refresh replaces the access cookie.
- Logout blacklists the refresh token and removes both cookies.
- Protected endpoints require a valid access cookie.

### Register a User

```http
POST /api/register/
```

Permission: Public

Request body:

```json
{
  "username": "quizzer",
  "email": "quizzer@example.com",
  "password": "StrongPass123!",
  "confirmed_password": "StrongPass123!"
}
```

Successful response (`201 Created`):

```json
{
  "username": "quizzer",
  "email": "quizzer@example.com"
}
```

Possible responses:

- `201 Created`: The user was created.
- `400 Bad Request`: The data is invalid, the passwords do not match, or the email is already registered.

### Log In

```http
POST /api/login/
```

Permission: Public

Request body:

```json
{
  "username": "quizzer",
  "password": "StrongPass123!"
}
```

Successful response (`200 OK`):

```json
{
  "detail": "Login successful."
}
```

The response sets the `access_token` and `refresh_token` HttpOnly cookies.

Possible responses:

- `200 OK`: Login was successful and both cookies were set.
- `401 Unauthorized`: The username or password is incorrect.

### Refresh the Access Token

```http
POST /api/token/refresh/
```

Permission: A valid `refresh_token` cookie is required.

No request body is required.

Successful response (`200 OK`):

```json
{
  "detail": "Token refreshed."
}
```

The response sets a new `access_token` HttpOnly cookie.

Possible responses:

- `200 OK`: The access token was refreshed.
- `401 Unauthorized`: The refresh cookie is missing, invalid, or blacklisted.

### Log Out

```http
POST /api/logout/
```

Permission: Authentication required

No request body is required.

Successful response (`200 OK`):

```json
{
  "detail": "Logout successful."
}
```

The refresh token is added to the blacklist and both authentication cookies are removed.

Possible responses:

- `200 OK`: Logout was successful.
- `400 Bad Request`: The refresh cookie is missing.
- `401 Unauthorized`: Authentication failed or the refresh token is invalid.

### Generate a Quiz

```http
POST /api/quizzes/
```

Permission: Authentication required

Request body:

```json
{
  "url": "https://www.youtube.com/watch?v=VIDEO_ID"
}
```

Successful response (`201 Created`):

```json
{
  "id": 1,
  "title": "Python Basics",
  "description": "A quiz about the basic concepts of Python.",
  "created_at": "2026-10-20T12:00:00Z",
  "updated_at": "2026-10-20T12:00:00Z",
  "video_url": "https://www.youtube.com/watch?v=VIDEO_ID",
  "questions": [
    {
      "id": 1,
      "question_title": "What is Python?",
      "question_options": [
        "A programming language",
        "A database",
        "A browser",
        "An operating system"
      ],
      "answer": "A programming language",
      "created_at": "2026-10-20T12:00:00Z",
      "updated_at": "2026-10-20T12:00:00Z"
    }
  ]
}
```

Possible responses:

- `201 Created`: The quiz and its ten questions were generated and saved.
- `400 Bad Request`: The URL or the generated quiz data is invalid.
- `401 Unauthorized`: Authentication is required.

Generation may take some time because the video must be downloaded, transcribed, and processed by Gemini.

### List the User's Quizzes

```http
GET /api/quizzes/
```

Permission: Authentication required

Successful response (`200 OK`):

```json
[
  {
    "id": 1,
    "title": "Python Basics",
    "description": "A quiz about the basic concepts of Python.",
    "created_at": "2026-10-20T12:00:00Z",
    "updated_at": "2026-10-20T12:00:00Z",
    "video_url": "https://www.youtube.com/watch?v=VIDEO_ID"
  }
]
```

Possible responses:

- `200 OK`: The user's quizzes were returned.
- `401 Unauthorized`: Authentication is required.

Only quizzes owned by the authenticated user are returned.

### Retrieve a Quiz

```http
GET /api/quizzes/<id>/
```

Permission: Authentication and quiz ownership required

Successful response (`200 OK`) uses the same quiz structure as the quiz-generation response, including all questions.

Possible responses:

- `200 OK`: The quiz was returned.
- `401 Unauthorized`: Authentication is required.
- `404 Not Found`: The quiz does not exist or belongs to another user.

### Update a Quiz

```http
PATCH /api/quizzes/<id>/
```

Permission: Authentication and quiz ownership required

Request body:

```json
{
  "title": "Updated Python Quiz",
  "description": "An updated description."
}
```

Both fields are optional during a partial update. The video URL and questions cannot be changed through this endpoint.

Possible responses:

- `200 OK`: The quiz was updated and returned with its questions.
- `400 Bad Request`: The submitted data is invalid.
- `401 Unauthorized`: Authentication is required.
- `404 Not Found`: The quiz does not exist or belongs to another user.

### Delete a Quiz

```http
DELETE /api/quizzes/<id>/
```

Permission: Authentication and quiz ownership required

Possible responses:

- `204 No Content`: The quiz and all its questions were deleted.
- `401 Unauthorized`: Authentication is required.
- `404 Not Found`: The quiz does not exist or belongs to another user.

Deletion is permanent and cannot be undone.

## Running Tests

Run all tests:

```powershell
python manage.py test
```

Run only the quiz application tests:

```powershell
python manage.py test quiz_app
```

Run only the authentication tests:

```powershell
python manage.py test auth_app
```

Check the Django configuration:

```powershell
python manage.py check
```

## Project Structure

```text
Quizly/
|-- auth_app/              # Registration and cookie-based JWT authentication
|-- core/                  # Django configuration and root URLs
|-- quiz_app/
|   |-- api/               # Quiz endpoints and serializers
|   |-- migrations/        # Database migrations
|   |-- services/          # YouTube, Whisper, Gemini, and storage services
|   `-- tests/             # Quiz application tests
|-- manage.py
`-- requirements.txt
```

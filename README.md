# LLM MVP (FastAPI)

Minimal, production-leaning backend demonstrating:
- Auth (JWT)
- LLM chat (OpenAI; stubbed if no API key)
- SQLite persistence
- Simple API integration (Open-Meteo weather)
- Image upload/inspection

## 1) Setup (Windows / macOS / Linux)

```bash
python -m venv venv
# Windows
venv\\Scripts\\activate
# macOS/Linux
# source venv/bin/activate

pip install -r requirements.txt
```

Create a `.env` in the project root (copy from `.env.example` and edit).

## 2) Run

```bash
uvicorn app.main:app --reload
```

Docs: http://127.0.0.1:8000/docs

## 3) Quick Test

1. **Register**
   - POST `/auth/register` with body:
     ```json
     {"username":"test","password":"secret"}
     ```

2. **Login**
   - POST `/auth/login` -> copy `access_token`

3. **Chat**
   - POST `/chat` with body:
     ```json
     {"prompt":"Say hello to Manila!"}
     ```
   - Add header: `Authorization: Bearer <access_token>`

4. **Weather integration**
   - GET `/integrations/weather?lat=14.5995&lon=120.9842`

5. **Upload image**
   - POST `/upload/image` with `form-data` file field `file`

## Notes
- If `OPENAI_API_KEY` is not set, chat endpoint returns a stubbed message so you can demo without credentials.
- Swap SQLite to Postgres later by updating `DATABASE_URL`.

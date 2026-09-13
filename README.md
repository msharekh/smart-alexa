# smart-alexa
# Smart Alexa AI

Arabic AI assistant that connects **Amazon Alexa** to **OpenAI** through a Python FastAPI backend.

## Architecture

```text
User
  ↓
Amazon Alexa
  ↓
Alexa Custom Skill (ar-SA)
  ↓ HTTPS
Cloudflare Tunnel
  ↓
FastAPI /alexa
  ↓
OpenAI API
  ↓
Arabic Response
  ↓
Alexa
```

## Project Location

```text
C:\Users\sharekhm\Documents\Development\Ai\smart-alexa
```

## Requirements

* Python 3.14+
* Amazon Alexa Developer Account
* OpenAI API Key
* Cloudflared
* Internet connection

## 1. Create Virtual Environment

Open PowerShell inside the project folder:

```powershell
cd C:\Users\sharekhm\Documents\Development\Ai\smart-alexa
python -m venv .venv
```

Activate it:

```powershell
.venv\Scripts\activate
```

The terminal should show:

```text
(.venv) PS C:\Users\sharekhm\Documents\Development\Ai\smart-alexa>
```

## 2. Install Python Packages

```powershell
pip install fastapi uvicorn openai python-dotenv
```

## 3. Configure OpenAI API Key

Create:

```text
.env
```

Add:

```text
OPENAI_API_KEY=YOUR_OPENAI_API_KEY
```

Do not commit `.env` to GitHub.

Add this to `.gitignore`:

```text
.env
.venv/
__pycache__/
```

## 4. Run FastAPI

```powershell
uvicorn app:app --host 0.0.0.0 --port 8000
```

Expected:

```text
Uvicorn running on http://0.0.0.0:8000
```

Test locally:

```text
http://127.0.0.1:8000
```

Expected:

```json
{
  "status": "Moaen is running"
}
```

## 5. Test OpenAI

Open:

```text
http://127.0.0.1:8000/ask?question=ما هو أكبر كوكب في المجموعة الشمسية؟
```

Expected response:

```json
{
  "question": "ما هو أكبر كوكب في المجموعة الشمسية؟",
  "answer": "أكبر كوكب في المجموعة الشمسية هو المشتري."
}
```

## 6. Alexa Endpoint

FastAPI provides:

```text
POST /alexa
```

Swagger documentation:

```text
http://127.0.0.1:8000/docs
```

Test `LaunchRequest`:

```json
{
  "request": {
    "type": "LaunchRequest"
  }
}
```

Expected response:

```json
{
  "version": "1.0",
  "response": {
    "outputSpeech": {
      "type": "PlainText",
      "text": "هلا، أنا سمارت. وش حاب تسأل؟"
    },
    "shouldEndSession": false
  }
}
```

## 7. Alexa Skill Configuration

Create an Alexa **Custom Skill**.

Locale:

```text
Arabic (Saudi Arabia)
ar-SA
```

Hosting option:

```text
Provision your own
```

### Intent

Create:

```text
AskAIIntent
```

### Intent Slot

```text
Name: question
Type: AMAZON.SearchQuery
```

### Sample Utterances

```text
اسأل {question}
سؤالي هو {question}
جاوبني على {question}
أبي أعرف {question}
{question}
```

Save and build the Interaction Model.

## 8. Cloudflare Tunnel

FastAPI runs locally and cannot be accessed directly by Amazon Alexa.

Install Cloudflared:

```powershell
winget install --id Cloudflare.cloudflared
```

Run:

```powershell
cloudflared tunnel --url http://localhost:8000
```

Cloudflare should provide an HTTPS address similar to:

```text
https://xxxxx.trycloudflare.com
```

Test it in the browser.

Expected:

```json
{
  "status": "Moaen is running"
}
```

## 9. Configure Alexa HTTPS Endpoint

In:

```text
Alexa Developer Console
→ Build
→ Endpoint
```

Set the Default Region endpoint to:

```text
https://xxxxx.trycloudflare.com/alexa
```

Select the SSL option indicating that the certificate is issued by a trusted certificate authority.

Save the endpoint.

Important: Quick Cloudflare Tunnel URLs can change after restarting `cloudflared`.

If the URL changes, update the Alexa endpoint.

## 10. Test Alexa

Go to:

```text
Alexa Developer Console
→ Test
```

Enable:

```text
Development
```

Open the skill using its configured Invocation Name.

Alexa should send:

```text
LaunchRequest
    ↓
Cloudflare
    ↓
POST /alexa
    ↓
FastAPI
```

FastAPI should return:

```text
هلا، أنا سمارت. وش حاب تسأل؟
```

Then ask an Arabic question.

The expected final flow is:

```text
Alexa
  ↓
AskAIIntent
  ↓
question
  ↓
FastAPI
  ↓
OpenAI
  ↓
Arabic answer
  ↓
Alexa voice
```

## Troubleshooting

### 405 Method Not Allowed

If you open:

```text
https://xxxxx.trycloudflare.com/alexa
```

directly in a browser, you may see:

```text
405 Method Not Allowed
```

This is expected because browsers send `GET`, while `/alexa` accepts `POST`.

### OpenAI Credit Error

If OpenAI returns:

```text
credit_balance_exhausted
```

check the OpenAI API billing balance.

ChatGPT Plus billing and OpenAI API billing are separate.

### Cloudflare DNS Error

Possible error:

```text
Failed to refresh DNS local resolver
lookup region1.v2.argotunnel.com: i/o timeout
```

Check DNS:

```powershell
nslookup region1.v2.argotunnel.com
```

Run Cloudflare diagnostics:

```powershell
cloudflared tunnel diag
```

Then restart:

```powershell
cloudflared tunnel --url http://localhost:8000
```

## Security

Never expose or commit:

* `OPENAI_API_KEY`
* Alexa `apiAccessToken`
* Alexa user IDs
* Session tokens

The current version is a development prototype.

Before production use, add proper Alexa request verification and use a persistent HTTPS endpoint instead of a temporary Quick Tunnel.

## Current Status

Completed:

```text
[✓] Python virtual environment
[✓] FastAPI
[✓] OpenAI API
[✓] Arabic AI responses
[✓] /ask endpoint
[✓] /alexa endpoint
[✓] Alexa ar-SA Interaction Model
[✓] AskAIIntent
[✓] AMAZON.SearchQuery slot
[✓] Cloudflare Tunnel setup
[✓] Alexa HTTPS endpoint
```

In progress:

```text
[ ] Stable Cloudflare connection
[ ] End-to-end Alexa LaunchRequest
[ ] End-to-end AskAIIntent
[ ] Alexa request verification
[ ] Persistent production tunnel
```

## Next Step

Establish a stable HTTPS tunnel and verify that Alexa produces:

```text
POST /alexa HTTP/1.1 200 OK
```

Then test:

```text
Alexa → Arabic Question → OpenAI → Arabic Voice Response
```

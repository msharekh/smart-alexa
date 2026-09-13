import os

from dotenv import load_dotenv
from fastapi import FastAPI, Request
from openai import OpenAI


load_dotenv()

app = FastAPI()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


@app.get("/")
def home():
    return {"status": "Moaen is running"}


@app.get("/ask")
def ask(question: str):
    try:
        response = client.responses.create(
            model="gpt-5.6-luna",
            instructions="أجب بالعربية بشكل مختصر وواضح.",
            input=question
        )

        return {
            "question": question,
            "answer": response.output_text
        }

    except Exception as e:
        error_text = str(e)

        if "credit_balance_exhausted" in error_text or "insufficient_quota" in error_text:
            return {
                "error": "رصيد OpenAI API غير متوفر. أضف رصيدًا ثم حاول مرة أخرى."
            }

        return {
            "error": "حدث خطأ أثناء الاتصال بـ OpenAI.",
            "details": error_text
        }
    


@app.post("/alexa")
async def alexa_endpoint(request: Request):

    data = await request.json()

    request_type = data.get("request", {}).get("type")

    if request_type == "LaunchRequest":
        return {
            "version": "1.0",
            "response": {
                "outputSpeech": {
                    "type": "PlainText",
                    "text": "هلا، أنا سمارت. وش حاب تسأل؟"
                },
                "shouldEndSession": False
            }
        }

    if request_type == "IntentRequest":

        intent = data.get("request", {}).get("intent", {})
        intent_name = intent.get("name")

        if intent_name == "AskAIIntent":

            slots = intent.get("slots", {})
            question = slots.get("question", {}).get("value")

            if not question:
                answer = "ما سمعت السؤال بوضوح."
            else:
                try:
                    response = client.responses.create(
                        model="gpt-5.6-luna",
                        instructions=(
                            "أنت مساعد صوتي عربي اسمه سمارت. "
                            "أجب بالعربية باختصار وبأسلوب طبيعي. "
                            "لا تستخدم Markdown لأن Alexa ستقرأ الإجابة صوتياً."
                        ),
                        input=question
                    )

                    answer = response.output_text

                except Exception as e:
                    print(e)
                    answer = "عذراً، صار خطأ أثناء الاتصال بالذكاء الاصطناعي."

            return {
                "version": "1.0",
                "response": {
                    "outputSpeech": {
                        "type": "PlainText",
                        "text": answer
                    },
                    "shouldEndSession": False
                }
            }

    return {
        "version": "1.0",
        "response": {
            "outputSpeech": {
                "type": "PlainText",
                "text": "ما فهمت طلبك."
            },
            "shouldEndSession": False
        }
    }
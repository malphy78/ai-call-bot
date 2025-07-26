from flask import Flask, request
from twilio.rest import Client
from twilio.twiml.voice_response import VoiceResponse

app = Flask(__name__)

account_sid = 'AC708abc23ddee77e900ee7e67721a4252'
auth_token = '3c732be20f3da3481d8c5386923bcac5'
twilio_number = '+17697596857'

client = Client(account_sid, auth_token)

@app.route("/")
def hello():
    return "✅ AI Call Bot is Live!"

@app.route("/voice", methods=['GET', 'POST'])
def voice():
    response = VoiceResponse()
    response.say(
        "Hello. This is your AI assistant. Your appointment is confirmed for two P M tomorrow. Have a great day.",
        voice='Polly.Joanna',
        language='en-US'
    )
    return str(response)

@app.route("/call", methods=['GET'])
def call():
    to_number = request.args.get("to", "+17697596857")
    try:
        call = client.calls.create(
            to=to_number,
            from_=twilio_number,
            url="https://ai-call-bot-couz.onrender.com/voice"
        )
        return f"📞 Calling {to_number}. Call SID: {call.sid}"
    except Exception as e:
        return f"❌ Error: {str(e)}"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

from flask import Flask, request
from twilio.rest import Client
from twilio.twiml.voice_response import VoiceResponse

app = Flask(__name__)

account_sid = 'AC708abc23ddee77e900ee7e67721a4252'
auth_token = '3b0938f0fe4411c44d3a58c41ba5eace'
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
    call = client.calls.create(
        to=to_number,
        from_=twilio_number,
        url="https://REPLACE-WITH-RENDER-URL.onrender.com/voice"
    )
    return f"📞 Calling {to_number}. Call SID: {call.sid}"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

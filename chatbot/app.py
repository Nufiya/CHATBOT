from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib

app = Flask(__name__)
CORS(app)  

model = joblib.load('chatbot_model/model.pkl')
tfidf = joblib.load('chatbot_model/tfidf_vectorizer.pkl')
label_encoder = joblib.load('chatbot_model/label_encoder.pkl')

@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json()
    user_utterance = req.get('queryResult', {}).get('queryText', '')

    basic_responses = {
    'hi': "Hello! How can I assist you today?",
    'hello': "Hi there! What can I do for you?",
    'bye': "Goodbye! Have a great day!",
    'thank you': "You're welcome! If you have any more questions, feel free to ask.",
    'thanks': "No problem! I'm here to help.",
    'ok': "Alright! Let me know if you need anything else.",
    'how are you': "I'm just a program, but I'm here to help you!",
    'what is your name': "I'm your virtual assistant. You can call me Chatbot!",
    'help': "I'm here to help! What do you need assistance with?",
    'i need assistance': "Sure! Please tell me what you need assistance with.",
    'tell me a joke': "Why don't scientists trust atoms? Because they make up everything!",
    'good morning': "Good morning! How can I brighten your day?",
    'good evening': "Good evening! How can I assist you tonight?",
    'good night': "Good night! Sweet dreams!",
    'sorry': "No worries! How can I help you?",
    'yes': "Great! What would you like to do next?",
    'no': "Okay! Let me know if you change your mind.",
    'maybe': "That's fine! Take your time to decide.",
    'what can you do': "I can help with various tasks, including order management and answering your questions.",
    'what\'s up': "Not much! Just here to assist you. What can I help with?",
    'hi there': "Hello! What can I do for you today?",
    'welcome': "Thank you! How can I assist you today?",
    'let\'s chat': "Sure! I'm here to chat. What’s on your mind?"}
    
    for key in basic_responses:
        if key in user_utterance.lower():
            response = {
                "fulfillmentText": basic_responses[key]
            }
            return jsonify(response)
    
    X_tfidf = tfidf.transform([user_utterance])
    predicted_label = model.predict(X_tfidf)[0]
    intent = label_encoder.inverse_transform([predicted_label])[0]
    
    if intent == 'cancel_order':
        response_text = f"Your '{intent}' request is accepted. Go to 'my_orders' section & choose the product you want to cancel then click on 'cancel_order' button."
    elif intent == 'change_order':
        response_text = f"Your '{intent}' request is accepted. Go to 'my_orders' section & choose the product you want to exchange with and then you can proceed."
    elif intent == 'change_shipping_address':
        response_text = f"Your '{intent}' request is accepted. Go to the 'My Address' section click on edit button and change your address."
    elif intent == 'check_cancellation_fee':
        response_text = f"Your '{intent}' request is accepted. You can check it in the bank statement."
    elif intent == 'check_invoice':
        response_text = f"Your '{intent}' request is accepted. Go to your profile click on 'invoice' section , give details and click on {intent} button."
    elif intent == 'get_invoice':
        response_text = f"Your '{intent}' request is accepted. Go to your profile click on 'invoice' section , give details and click on {intent} button."
    elif intent == 'check_payment_methods':
        response_text = f"Your '{intent}' request is accepted. Go to my_account click on payments then click on methods , you can select your favorable option"
    elif intent == 'check_refund_policy':
        response_text = f"Your '{intent}' request is accepted. Go to 'my_orders' section & choose the product you want to check, you can find 'refund_policy' option under the product"
    elif intent == 'review':
        response_text = f"Your '{intent}' request is accepted. Go to my_account click on  feedback write and submit"
    elif intent == 'complaint':
        response_text = f"Your '{intent}' request is accepted. Go to my_account click on  feedback write and submit"
    elif intent == 'contact_customer_service':
        response_text = f"Your '{intent}' request is accepted. Go to my_account click on customer_service , they can contact you between 10AM to 5PM "
    elif intent == 'contact_human_agent':
        response_text = f"Your '{intent}' request is accepted. Go to my_account click on agent , they can contact you between 10AM to 5PM"
    elif intent == 'create_account':
        response_text = f"Your '{intent}' request is accepted. In home page click on 'sign_in' option then fill your details click on create button.you're Done."
    elif intent == 'delete_account':
        response_text = f"Your '{intent}' request is accepted. Go to 'my_account' section, click on delete_account ,it pop ups the reasons option select your reason and click on conform. "
    elif intent == 'delivery_options':
        response_text = f"Your '{intent}' request is accepted. Go to my_account click on delivery and then click on delivery_options, choose your favorable option"
    elif intent == 'delivery_period':
        response_text = f"Your '{intent}' request is accepted. Go to 'my_order' , click on the order ,under your product you can see when your product will deliver."
    elif intent == 'edit_account':
        response_text = f"Your '{intent}' request is accepted. Go to the 'my_account' section click on edit button and change your information."
    elif intent == 'get_refund':
        response_text = f"Your '{intent}' request is accepted. Go to the 'cancel_orders' section, choose product and click on 'issue_refund'."
    elif intent == 'newsletter_subscription':
        response_text = f"Your '{intent}' request is accepted. Go to your profile click on 'subscribe' and do payment (or) click on 'unsubscribe' "
    elif intent == 'payment_issue':
        response_text = f"Your '{intent}' request is accepted. Go to my_account click on payments click payment_issue , write your issue then click on 'send' button."
    elif intent == 'place_order':
        response_text = f"Your '{intent}' request is accepted. Go to 'cart' ,choose 'product' then click on 'place_order' button and conform delivery address and choose payment option then click on 'conform_order' button."
    elif intent == 'recover_password':
        response_text = f"Your '{intent}' request is accepted. Go to my_account click on security,then click on password ,then click on forget password then click on recovery_password then enter otp u received finally set new password "
    elif intent == 'registration_problems':
        response_text = f"Your '{intent}' request is accepted. Go to my_account click on issues click on registration_problem click on  submit"
    elif intent == 'set_up_shipping_address':
        response_text = f"Your '{intent}' request is accepted. Go to the 'My Address' section click on 'new' button and then add your new address and click on 'save' button. "
    elif intent == 'switch_account':
        response_text = f"Your '{intent}' request is accepted. Double click on your profile (or) long press on your profile and then click on another account. "
    elif intent == 'track_order':
        response_text = f"Your '{intent}' request is accepted.  Go to 'my_orders' section & choose the order and then click on 'track_order' button."
    elif intent == 'track_refund':
        response_text = f"Your '{intent}' request is accepted. Go to the 'cancel_orders' section, click on refunds and then click on 'track_refund' button."
    else:
        response_text = "Sorry i don't get that" or  "that seems off-topic" or "can we discuss something else?"
    
    response = {
        "fulfillmentText": response_text
    }

    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)

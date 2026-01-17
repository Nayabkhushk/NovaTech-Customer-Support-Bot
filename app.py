import gradio as gr
from rapidfuzz import process, fuzz

# -------------------------------
# Fixed Questions & Answers
# -------------------------------
QA_PAIRS = {
    "What are your pricing plans?": "We offer Basic (Free), Pro ($29/month), and Ultra ($79/month). Choose what suits you best 😎",
    "How much does it cost?": "We offer Basic (Free), Pro ($29/month), and Ultra ($79/month). Choose what suits you best 😎",
    "How can I contact support?": "You can email us at support@novatech.com or use live chat anytime — we’re available 24/7 💬",
    "What is your refund policy?": "All paid plans come with a 30-day money-back guarantee. No worries at all 💸",
    "Can I get a refund?": "All paid plans come with a 30-day money-back guarantee. No worries at all 💸",
    "Do you offer discounts?": "Yes! We offer student and nonprofit discounts. Contact support to get a special code ✨",
    "Is there any discount available?": "Yes! We offer student and nonprofit discounts. Contact support to get a special code ✨",
    "How do I reset my account password?": "Click on ‘Forgot Password’ on the login page and follow the steps. Easy peasy 🔐",
    "I forgot my password": "Click on ‘Forgot Password’ on the login page and follow the steps. Easy peasy 🔐",
    "How do I create an account?": "Just click ‘Sign Up’, enter your details, and you’re good to go 🚀",
    "Do you offer a free trial?": "Yes! Our Basic plan is completely free forever — no credit card required 🙌",
    "How can I cancel my subscription?": "You can cancel anytime from your account settings — no hidden steps 👍",
    "Do you have plans for businesses?": "Absolutely! Our Ultra plan is perfect for businesses and teams 💼",
    "Is my data secure?": "Yes! We use industry-standard encryption to keep your data safe 🔒",
    "What are your support hours?": "Our support team is available 24/7, even on weekends 🌙",
    "Do you have a mobile app?": "Yes! NovaTech is available on both Android and iOS 📱"
}

QUESTIONS = list(QA_PAIRS.keys())

# -------------------------------
# Suggested Questions
# -------------------------------
SUGGESTED_QUESTIONS = (
    "💡 **You can ask me things like:**\n"
    "- What are your pricing plans?\n"
    "- How can I contact support?\n"
    "- What is your refund policy?\n"
    "- Do you offer discounts?\n"
    "- How do I reset my account password?\n"
    "- How do I create an account?\n"
    "- Do you offer a free trial?\n"
    "- How can I cancel my subscription?\n"
    "- Is my data secure?\n"
    "- Do you have a mobile app?\n"
)

WELCOME_MESSAGE = (
    "Heyyy 👋✨ Welcome to **NovaTech Support**!\n\n"
    "I’ve got you covered 😎\n\n"
    + SUGGESTED_QUESTIONS
)

# -------------------------------
# Chatbot Logic
# -------------------------------
def chatbot(user_input, history):
    if not user_input.strip():
        return history

    match, score, _ = process.extractOne(
        user_input,
        QUESTIONS,
        scorer=fuzz.partial_ratio
    )

    if score >= 50:
        bot_reply = QA_PAIRS[match]
    else:
        bot_reply = (
            "Sorry, I’m not sure about that 😕\n\n"
            "Here’s what I *can* help you with 👇\n\n"
            + SUGGESTED_QUESTIONS
        )

    # Append as dictionary for Gradio 6+ format
    history.append({"role": "user", "content": user_input})
    history.append({"role": "assistant", "content": bot_reply})
    return history

# -------------------------------
# Gradio UI
# -------------------------------
with gr.Blocks() as demo:
    gr.Markdown("# 💬 NovaTech Customer Support Bot")
    gr.Markdown("Fast • Friendly • No stress ✨")

    chatbot_ui = gr.Chatbot(value=[{"role": "assistant", "content": WELCOME_MESSAGE}], height=450)
    user_input = gr.Textbox(placeholder="Ask me anything about NovaTech...", show_label=False)

    user_input.submit(chatbot, [user_input, chatbot_ui], chatbot_ui)
    user_input.submit(lambda: "", None, user_input)

# Move theme to launch() for Gradio 6+
demo.launch(theme=gr.themes.Soft())


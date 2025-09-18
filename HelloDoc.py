import tkinter as tk
from tkinter import scrolledtext
import webbrowser
import re

# Global variable to track medicine suggestion state
awaiting_medicine_choice = False
awaiting_age_for_vaccine = False   # 🔹 new flag

# ✅ Fixed medicine URLs
medicine_options = {
    "1mg": {
        "price": "₹32.9",
        "delivery": "by today",
        "url": "https://www.1mg.com/drugs/dolo-650-tablet-74467",
    },
    "netmeds": {
        "price": "₹30.84",
        "delivery": "1 day",
        "url": "https://www.netmeds.com/prescriptions/dolo-650mg-tablet-15-s",
    },
    "pharmeasy": {
        "price": "₹25.02",
        "delivery": "1 day",
        "url": "https://pharmeasy.in/online-medicine-order/dolo-650mg-strip-of-15-tablets-44140",
    },
}

# Mock outbreak alerts
outbreak_alerts = [
    "⚠️ Dengue cases rising in Delhi NCR. Use mosquito repellents & keep surroundings clean.",
    "⚠️ Seasonal flu spreading in Mumbai. Wear masks & wash hands frequently.",
]

# Vaccination schedule sample
vaccination_schedule = {
    "child": ["BCG", "Polio", "Hepatitis B", "MMR"],
    "adult": ["Tetanus booster (every 10 years)", "Flu shot (annual)", "COVID-19 booster"],
    "elderly": ["Pneumococcal vaccine", "Shingles vaccine"],
}

# Preventive healthcare tips
preventive_tips = [
    "🟢 Wash hands regularly with soap.",
    "🟢 Exercise 30 mins daily.",
    "🟢 Eat balanced diet (fruits & veggies).",
    "🟢 Get 7-8 hours of sleep.",
]

# First Aid dictionary
first_aid_tips = {
    "burn": "🔥 Burn: Cool with running water for 20 minutes. Do NOT apply ice.",
    "cut": "🩸 Cut: Wash with clean water, apply antiseptic, cover with bandage.",
    "bleeding": "🩸 Bleeding: Wash with clean water, apply antiseptic, cover with bandage.",
    "faint": "😵 Fainting: Lay person flat, raise legs slightly, loosen tight clothing.",
    "fracture": "🦴 Fracture: Keep limb still, support with splint, seek medical help.",
}


# --- Chatbot logic ---
def get_bot_response(user_input):
    global awaiting_medicine_choice, awaiting_age_for_vaccine

    user_input = user_input.lower().strip()

    # --- If waiting for vaccine age ---
    if awaiting_age_for_vaccine:
        try:
            age = int(re.findall(r'\d+', user_input)[0])  # extract number
            awaiting_age_for_vaccine = False
            if age < 18:
                return ("💉 Vaccination Reminders for Children:\n" +
                        ", ".join(vaccination_schedule["child"]))
            elif 18 <= age < 60:
                return ("💉 Vaccination Reminders for Adults:\n" +
                        ", ".join(vaccination_schedule["adult"]))
            else:
                return ("💉 Vaccination Reminders for Elderly:\n" +
                        ", ".join(vaccination_schedule["elderly"]))
        except:
            return "❓ Please enter a valid age (e.g., 25)."

    # --- Medicine Choice ---
    if awaiting_medicine_choice:
        for site in medicine_options:
            if site in user_input:
                webbrowser.open(medicine_options[site]["url"])
                awaiting_medicine_choice = False
                return f"💊 Redirecting you to {site.capitalize()} for order placement."
        return "Please choose one of the options: 1mg, NetMeds, or PharmEasy."

    # --- Multilingual greetings (Hindi + English) ---
    if any(word in user_input for word in ["hi", "hello", "hey", "namaste", "namaskar", "salaam"]):
        return "नमस्ते! 👋 Hello! I can talk in Hindi & English. How can I help you today?"

    # --- Thanks ---
    if any(word in user_input for word in ["thanks", "thank you", "dhanyavad", "shukriya"]):
        return "You're welcome! 😊 Glad I could help."

    # --- Fever symptom ---
    if "fever" in user_input or "bukhar" in user_input:
        return ("It seems like you may have a fever 🤒. Stay hydrated and rest well.\n"
                "For emergencies, consult a doctor immediately.")

    # --- Cough ---
    if "cough" in user_input or "khansi" in user_input or "khasi" in user_input:
        return ("Cough detected. Drink warm fluids, honey + ginger tea may help.\n"
                "If it persists >1 week, see a doctor.")

    # --- Home remedy ---
    if "home remedy" in user_input or "home remedies" in user_input:
        return ("✅ Home Remedy Suggestion:\n"
                "- Fever: Drink tulsi + ginger kadha.\n"
                "- Cough: Honey with warm water.\n"
                "- Cold: Steam inhalation with ajwain seeds.")

    # --- Ayurveda ---
    if "ayurveda" in user_input or "ayurvedic" in user_input:
        return ("🌿 Ayurvedic Tip:\n"
                "- Fever: Giloy juice.\n"
                "- Indigestion: Triphala powder with warm water.\n"
                "- Immunity: Chyawanprash daily.")

    # --- Homeopathy ---
    if "homeopathy" in user_input or "homoeopathic" in user_input:
        return ("⚪ Homeopathic Suggestion:\n"
                "- Fever: Belladonna 30.\n"
                "- Cough: Drosera 30.\n"
                "- Cold: Arsenicum Album 30.\n"
                "(Use only with doctor’s guidance).")

    # --- Doctor booking ---
    if "doctor" in user_input or "consult" in user_input or "consult a doctor" in user_input or "talk to doctor" in user_input:
        webbrowser.open("https://www.practo.com/")
        return "👨‍⚕️ Redirecting you to Practo for doctor consultation."

    # --- Medicine availability and price comparison ---
    if "medicine" in user_input or "tablet" in user_input or "drug" in user_input:
        awaiting_medicine_choice = True
        comparison_text = "💊 Medicine availability & price comparison:\n"
        for site, info in medicine_options.items():
            comparison_text += f"- {site.capitalize()}: {info['price']} | Delivery: {info['delivery']}\n"
        comparison_text += "\nPlease type which one you prefer (1mg / NetMeds / PharmEasy)."
        return comparison_text

    # --- Outbreak Alerts ---
    if "outbreak" in user_input or "alert" in user_input or "disease" in user_input:
        return "📢 Current Health Alerts:\n" + "\n".join(outbreak_alerts)

    # --- Vaccination reminders (trigger) ---
    if "vaccine" in user_input or "vaccination" in user_input or "reminder" in user_input:
        awaiting_age_for_vaccine = True
        return "💉 Please tell me your age so I can suggest the right vaccination reminders."

    # --- Preventive Healthcare ---
    if "prevent" in user_input or "healthy" in user_input or "tips" in user_input:
        return "🛡️ Preventive Healthcare Tips:\n" + "\n".join(preventive_tips)

    # --- First Aid ---
    for condition, tip in first_aid_tips.items():
        if condition in user_input:
            return f"⛑️ First Aid Suggestion:\n{tip}"

    if "first aid" in user_input:
        tips_list = "\n".join([f"- {k.capitalize()}: {v}" for k, v in first_aid_tips.items()])
        return f"⛑️ First Aid Guide:\n{tips_list}"

    # --- General ---
    return ("I can assist with:\n"
            "- Symptoms (fever, cough, etc.)\n"
            "- Remedies (Home, Ayurveda, Homeopathy)\n"
            "- Doctor consultation\n"
            "- Medicine ordering & comparison\n"
            "- Outbreak alerts\n"
            "- Vaccination reminders\n"
            "- Preventive healthcare tips\n"
            "- First aid guidance")


# --- UI Design ---
def send_message(event=None):
    user_input = entry.get().strip()
    if not user_input:
        return
    chat_area.insert(tk.END, "You: " + user_input + "\n", "user")
    entry.delete(0, tk.END)

    bot_response = get_bot_response(user_input)
    chat_area.insert(tk.END, "Bot: " + bot_response + "\n\n", "bot")
    chat_area.yview(tk.END)


# --- Main window ---
root = tk.Tk()
root.title("Healthcare Chatbot 🤖")
root.geometry("520x650")

chat_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, font=("Arial", 14))
chat_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

chat_area.tag_config("user", foreground="blue", font=("Arial", 14, "bold"))
chat_area.tag_config("bot", foreground="green", font=("Arial", 14))

chat_area.insert(
    tk.END,
    "Bot: Hello! I am your Healthcare Assistant 🤖.\n"
    "I can help with:\n"
    "✔️ Symptoms\n✔️ Remedies (Home, Ayurveda, Homeopathy)\n✔️ Doctor consultation\n"
    "✔️ Medicines & price comparison\n✔️ Outbreak alerts\n✔️ Vaccination reminders\n"
    "✔️ Preventive healthcare tips\n✔️ First aid guidance\n\n",
    "bot"
)

entry = tk.Entry(root, font=("Arial", 13))
entry.pack(padx=10, pady=10, fill=tk.X)
entry.bind("<Return>", send_message)
entry.focus()

send_button = tk.Button(root, text="Send", command=send_message, font=("Arial", 12, "bold"))
send_button.pack(pady=5)

root.mainloop()

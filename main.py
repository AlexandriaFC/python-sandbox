import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import os
import json
import random
from flask import Flask

app = Flask(__name__)

# --- ENV VARIABLES ---
SENDER_EMAIL = os.environ.get("brianbosak@gmail.com")
SENDER_PASSWORD = os.environ.get("letnxdmngmznajjv")
RECEIVER_EMAIL = "brianbosak@gmail.com"


# --- TASKS FOR FIRST 21 DAYS (day-specific) ---
daily_tasks = [
    ["Prepare your thoughts for the co-founder conversation: focus on vision, values, and what kind of partnership you're looking for."],
    ["Write down your one-paragraph product vision."],
    ["List out the 3 most important outcomes you'd want from this venture."],
    ["Sketch the rough outline of the business on a single page (what it does, who it's for, why now)."],
    ["Outline your key assumptions about what customers want."],
    ["List the 3 biggest risks that could prevent this idea from succeeding."],
    ["Research if similar ideas already exist and how yours is different."],
    ["Draft 5 questions to ask realtors about buyer fears."],
    ["Reach out to 2 realtors to ask for quick feedback calls."],
    ["Research 1 startup solving home-buying anxiety with tech."],
    ["List 3 platforms where realtors hang out online."],
    ["Write a short LinkedIn post describing your idea to test interest."],
    ["Prepare 3-4 key bullet points for a pitch to realtors."],
    ["Summarize your key insight so far in 1–2 sentences."],
    ["Create a fake listing and try writing your first risk report manually."],
    ["Pick 2 listing photos from Zillow and note visible red flags."],
    ["List 3 types of data you'd want to include in every report."],
    ["Come up with 3 possible names for the product."],
    ["Write down your criteria for a great name."],
    ["Sketch out what a 'Home Risk Report' might look like on paper."],
    ["Create a 1-page outline of your MVP (features only)."]
]

# --- MOTIVATIONAL QUOTES BY DAY ---
quotes_by_day = {
    "Monday": ["Start strong. Win the week.", "The secret of getting ahead is getting started."],
    "Tuesday": ["Keep the momentum.", "Consistency beats intensity."],
    "Wednesday": ["You’re halfway there.", "Push through the dip."],
    "Thursday": ["You're building something real.", "Grind now. Glory later."],
    "Friday": ["Celebrate progress, not perfection.", "You made moves this week — keep going."],
    "Saturday": ["Create without pressure today.", "Small steps still count."],
    "Sunday": ["Reflect. Recharge. Realign.", "Next week is yours to win."]
}

# --- FAITH-BASED ENCOURAGEMENT ---
faith_quotes = [
    "Courage, dear heart. — C.S. Lewis",
    "You are never too old to set another goal or to dream a new dream. — C.S. Lewis",
    "Relying on God has to begin all over again every day as if nothing had yet been done. — C.S. Lewis",
    "God is not hurried, yet He is always on time. — Unknown",
    "When we are weak, then we are strong. — 2 Corinthians 12:10",
    "Do not be afraid or discouraged, for the Lord your God is with you wherever you go. — Joshua 1:9",
    "The will of God will not take you where the grace of God cannot protect you. — Unknown",
    "Faith is the art of holding on to things your reason has once accepted, in spite of your changing moods. — C.S. Lewis"
]

# --- TRACKER FILE PATH ---
progress_file = "task_progress.json"

# --- LOAD PROGRESS ---
def load_progress():
    if not os.path.exists(progress_file):
        with open(progress_file, "w") as f:
            json.dump({"day": 0}, f)
    with open(progress_file, "r") as f:
        return json.load(f)

# --- SAVE PROGRESS ---
def save_progress(day):
    with open(progress_file, "w") as f:
        json.dump({"day": day}, f)

# --- EMAIL SENDER FUNCTION ---
def send_email():
    progress = load_progress()
    day = progress.get("day", 0)

    if day >= len(daily_tasks):
        day = len(daily_tasks) - 1

    today_tasks = daily_tasks[day]
    motivation = random.choice(quotes_by_day.get(datetime.now().strftime('%A'), ["Keep going — you’ve got this."]))
    faith = random.choice(faith_quotes)

    html = f"""
    <html>
      <body>
        <p>Good morning Brian,</p>
        <p><strong>Day {day + 1} Task(s):</strong></p>
        <ul>
          {''.join([f'<li>{task}</li>' for task in today_tasks])}
        </ul>
        <p><strong>Today's Motivation:</strong><br><em>"{motivation}"</em></p>
        <p><strong>Faith Inspiration:</strong><br><em>"{faith}"</em></p>
        <p><strong>Progress:</strong> Day {day + 1} of {len(daily_tasks)}</p>
        <p>Let’s keep building. You’ve got this. 🚀</p>
      </body>
    </html>
    """

    message = MIMEMultipart("alternative")
    message["Subject"] = f"🚀 Day {day + 1} Startup Task"
    message["From"] = SENDER_EMAIL
    message["To"] = RECEIVER_EMAIL

    part = MIMEText(html, "html")
    message.attach(part)

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, message.as_string())

    save_progress(day + 1)


# --- FLASK ENDPOINT ---
@app.route("/run", methods=["GET"])
def trigger_email():
    send_email()
    return "Email sent!"

# --- RUN FLASK SERVER ---
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

# notifier/email_notifier.py
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def send_email(applied_jobs, config, subject=None, body=None):
    print('[DEBUG] config["email"]:', config.get('email'))
    email_config = config["email"]
    recipients = email_config["recipient"] if isinstance(email_config["recipient"], list) else [email_config["recipient"]]

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject or "✅ Finance Job Bot: Application Summary"
    msg["From"] = email_config["smtp_user"]
    msg["To"] = ", ".join(recipients)

    if body:
        html = f"<html><body><pre>{body}</pre></body></html>"
    else:
        # Always send a test email, even if no jobs were applied
        if not applied_jobs:
            html = """
            <html>
              <body>
                <h2>� Job Bot Test Email</h2>
                <p>No jobs were applied, but this is a test email to confirm email delivery works.</p>
                <p>– Your Finance Job Bot 🤖</p>
              </body>
            </html>
            """
        else:
            html = """
            <html>
              <body>
                <h2>📄 Successfully Applied Jobs</h2>
                <ul>
            """
            for job in applied_jobs:
                html += f'<li><b>{job.get("title", "")}</b> at {job.get("company", "")} - {job.get("location", "")}<br>'
                if job.get("url"):
                    html += f'<a href="{job["url"]}">{job["url"]}</a>'
                html += '</li><br>'
            html += """
                </ul>
                <p>– Your Finance Job Bot 🤖</p>
              </body>
            </html>
            """

    msg.attach(MIMEText(html, "html"))

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(email_config["smtp_user"], email_config["smtp_password"])
            server.sendmail(msg["From"], recipients, msg.as_string())
            print(f"📧 Email sent to {msg['To']}")
    except Exception as e:
        print(f"⚠️ Failed to send email: {e}")

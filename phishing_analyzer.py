import re
from datetime import datetime

class PhishingAnalyzer:
    def __init__(self):
        self.suspicious_keywords = [
            "urgent", "verify", "verification", "password",
            "login", "account suspended", "click here",
            "winner", "claim", "limited time", "otp",
            "confirm", "security alert", "bank",
            "gift", "prize", "payment", "invoice",
            "crypto", "bitcoin", "refund", "update"
        ]

    def analyze(self, message):
        report = {
            "keywords": [],
            "urls": [],
            "emails": [],
            "red_flags": [],
            "risk_score": 0,
            "risk_level": "Low"
        }

        text = message.lower()

        # Detect suspicious keywords
        for keyword in self.suspicious_keywords:
            if keyword in text:
                report["keywords"].append(keyword)
                report["risk_score"] += 5

        # Detect URLs
        urls = re.findall(r'https?://[^\s]+|www\.[^\s]+', message)
        if urls:
            report["urls"] = urls
            report["red_flags"].append("Suspicious URL detected.")
            report["risk_score"] += 20

        # Detect Email Addresses
        emails = re.findall(r'[\w\.-]+@[\w\.-]+\.\w+', message)
        if emails:
            report["emails"] = emails

        # Detect urgency
        urgency_words = ["urgent", "immediately", "within 24 hours", "expire", "now"]

        for word in urgency_words:
            if word in text:
                report["red_flags"].append(f'Urgency phrase found: "{word}"')
                report["risk_score"] += 10

        # Capital letters
        uppercase = sum(1 for c in message if c.isupper())

        if uppercase > 40:
            report["red_flags"].append("Too many capital letters.")
            report["risk_score"] += 10

        # Risk Level
        score = report["risk_score"]

        if score >= 70:
            report["risk_level"] = "HIGH"
        elif score >= 40:
            report["risk_level"] = "MEDIUM"
        else:
            report["risk_level"] = "LOW"

        return report


def print_report(report):
    print("=" * 65)
    print("         DECODELABS PHISHING AWARENESS ANALYZER")
    print("=" * 65)
    print("Analysis Time :", datetime.now())
    print()

    print(f"Risk Score : {report['risk_score']}/100")
    print(f"Risk Level : {report['risk_level']}")

    print("\nSuspicious Keywords")
    if report["keywords"]:
        for item in report["keywords"]:
            print("  •", item)
    else:
        print("  None")

    print("\nDetected URLs")
    if report["urls"]:
        for url in report["urls"]:
            print("  •", url)
    else:
        print("  None")

    print("\nDetected Email Addresses")
    if report["emails"]:
        for email in report["emails"]:
            print("  •", email)
    else:
        print("  None")

    print("\nRed Flags")
    if report["red_flags"]:
        for flag in report["red_flags"]:
            print("  •", flag)
    else:
        print("  No red flags detected.")

    print("\nSecurity Recommendation")
    if report["risk_level"] == "HIGH":
        print("Do NOT click any links. Delete the email and report it.")
    elif report["risk_level"] == "MEDIUM":
        print("Verify the sender before taking any action.")
    else:
        print("Message appears relatively safe, but remain cautious.")

    print("=" * 65)


def main():

    sample_message = """
    Dear Customer,

    Your BANK ACCOUNT has been suspended.

    Verify your account immediately by clicking the link below.

    https://secure-bank-login.xyz/login

    Failure to verify within 24 hours will permanently suspend your account.

    Contact:
    support@secure-bank-login.xyz

    Thank You.
    """

    analyzer = PhishingAnalyzer()

    report = analyzer.analyze(sample_message)

    print_report(report)


if __name__ == "__main__":
    main()
"""
Synthetic email dataset — replaces Gmail IMAP fetching.
Each call to fetch_unread_emails() returns a fresh batch of realistic
emails drawn from this dataset (without repeating in the same run).
"""

import random
from datetime import datetime, timedelta

# ---------------------------------------------------------------------------
# Dataset: realistic executive-inbox emails
# ---------------------------------------------------------------------------

SYNTHETIC_EMAILS = [
    {
        "sender": "priya.sharma@acmecorp.com",
        "subject": "Q2 Strategy Review — need your input by Thursday",
        "body": (
            "Hi,\n\n"
            "We're finalising the Q2 strategy deck for the board meeting on Friday. "
            "Could you please review the attached slides and share your feedback by Thursday EOD? "
            "Key sections that need your sign-off: Revenue projections (slide 7) and Headcount plan (slide 12).\n\n"
            "Thanks,\nPriya"
        ),
        "attachments": [],
    },
    {
        "sender": "raj.mehta@vendorx.io",
        "subject": "Contract renewal — action required before 31 March",
        "body": (
            "Dear Executive,\n\n"
            "Your annual contract with VendorX is up for renewal on 31 March. "
            "Please sign the attached renewal agreement and return it by 28 March to avoid any service interruption. "
            "If you have questions, call me at +91-98765-43210.\n\n"
            "Regards,\nRaj Mehta\nAccount Manager, VendorX"
        ),
        "attachments": [],
    },
    {
        "sender": "hr@yourcompany.com",
        "subject": "Performance review cycle kicks off next week",
        "body": (
            "Hi Team,\n\n"
            "The annual performance review cycle begins on Monday. "
            "All managers are required to submit self-assessments for their direct reports by 5 April. "
            "Please log in to the HR portal and complete the forms. "
            "Calibration sessions will be scheduled for 10–12 April.\n\n"
            "HR Team"
        ),
        "attachments": [],
    },
    {
        "sender": "ananya.iyer@client.com",
        "subject": "Meeting request — Product demo this week",
        "body": (
            "Hello,\n\n"
            "I'd love to schedule a 45-minute product demo with your team this week. "
            "We're evaluating your platform for our 200-person sales org and the decision deadline is 3 April. "
            "Are you available Wednesday or Thursday afternoon (IST)?\n\n"
            "Best,\nAnanya Iyer\nVP Sales, Client Inc."
        ),
        "attachments": [],
    },
    {
        "sender": "finance@yourcompany.com",
        "subject": "Invoice #INV-2024-089 approval needed",
        "body": (
            "Hi,\n\n"
            "Invoice #INV-2024-089 from TechSupplies Ltd for ₹4,50,000 is pending your approval in the finance portal. "
            "Please review and approve/reject by 29 March so we don't miss the payment cycle.\n\n"
            "Finance Team"
        ),
        "attachments": [],
    },
    {
        "sender": "suresh.nair@partner.org",
        "subject": "MOU signing ceremony — confirm attendance",
        "body": (
            "Dear Sir/Ma'am,\n\n"
            "We are pleased to confirm the MOU signing ceremony between our organisations on 2 April at 11:00 AM "
            "at The Leela, Pune. Kindly confirm your attendance and the names of attendees (max 3) by 30 March.\n\n"
            "Warm regards,\nSuresh Nair\nDirector, Partner Org"
        ),
        "attachments": [],
    },
    {
        "sender": "devops-alerts@yourcompany.com",
        "subject": "URGENT: Production outage — your sign-off needed for rollback",
        "body": (
            "Hi,\n\n"
            "We are experiencing a production outage on the payments service (started 02:15 IST). "
            "The engineering team recommends an immediate rollback to v2.3.1. "
            "Please approve the rollback via the ops dashboard or reply to this email ASAP.\n\n"
            "On-call: Vikram Desai (+91-97890-12345)"
        ),
        "attachments": [],
    },
    {
        "sender": "legal@yourcompany.com",
        "subject": "NDA review — signature required",
        "body": (
            "Hi,\n\n"
            "Please find attached the NDA with GlobalTech Partners. Legal has reviewed and cleared it. "
            "We need your signature before the partnership kickoff call on 1 April at 3 PM IST. "
            "Use DocuSign link: https://docusign.example.com/sign/abc123\n\n"
            "Legal Team"
        ),
        "attachments": [],
    },
    {
        "sender": "board@yourcompany.com",
        "subject": "Board meeting agenda — please review and add items",
        "body": (
            "Dear All,\n\n"
            "The next board meeting is scheduled for 5 April at 2:00 PM. "
            "Please review the draft agenda (attached) and send any agenda items you want to add by 1 April. "
            "The meeting will be held in the Boardroom, HQ.\n\n"
            "Company Secretary"
        ),
        "attachments": [],
    },
    {
        "sender": "media@pressagency.in",
        "subject": "Interview request — Economic Times feature on AI adoption",
        "body": (
            "Dear Executive,\n\n"
            "I am a senior journalist at Economic Times working on a feature about AI adoption in Indian enterprises. "
            "We would love a 20-minute phone interview with you this week. "
            "Please let me know your availability and we'll coordinate accordingly.\n\n"
            "Thanks,\nKavitha Rao\nSenior Reporter, ET"
        ),
        "attachments": [],
    },
    {
        "sender": "travel@yourcompany.com",
        "subject": "Mumbai trip — flight & hotel booking confirmation needed",
        "body": (
            "Hi,\n\n"
            "For your Mumbai visit on 4 April, we've shortlisted the following options:\n"
            "• Flight: IndiGo 6E-302, Pune→Mumbai, departs 07:30, arrives 08:40 — ₹4,200\n"
            "• Hotel: Taj Lands End, Bandra — ₹12,500/night\n\n"
            "Please confirm by 29 March so we can block the bookings.\n\n"
            "Travel Desk"
        ),
        "attachments": [],
    },
    {
        "sender": "cto@yourcompany.com",
        "subject": "Tech roadmap sign-off — Q2 priorities",
        "body": (
            "Hi,\n\n"
            "Sharing the Q2 tech roadmap for your sign-off. Key highlights:\n"
            "1. Launch of mobile app v3 — April 15\n"
            "2. Data warehouse migration — April 30\n"
            "3. SOC 2 audit preparation — ongoing\n\n"
            "Please review and confirm by Friday so the engineering team can lock sprints.\n\n"
            "— CTO"
        ),
        "attachments": [],
    },
]

# Track which indices have been used this session
_used_indices: set = set()


def fetch_unread_emails(limit: int = 5) -> list[dict]:
    """
    Return `limit` synthetic emails, cycling through the dataset.
    Resets once all emails have been served.
    """
    global _used_indices

    available = [i for i in range(len(SYNTHETIC_EMAILS)) if i not in _used_indices]

    # Reset if we've exhausted the dataset
    if len(available) < limit:
        _used_indices = set()
        available = list(range(len(SYNTHETIC_EMAILS)))

    chosen = random.sample(available, min(limit, len(available)))
    _used_indices.update(chosen)

    emails = []
    for idx in chosen:
        e = SYNTHETIC_EMAILS[idx].copy()
        # Attach a realistic received_at timestamp (within the last hour)
        e["received_at"] = (
            datetime.now() - timedelta(minutes=random.randint(1, 60))
        ).isoformat()
        emails.append(e)

    return emails

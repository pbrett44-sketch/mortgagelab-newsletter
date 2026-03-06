"""
Mailchimp Publisher - Creates draft campaign and sends test email
"""

import os
import sys
import glob
import requests
from datetime import datetime


class MailchimpPublisher:
    # Base campaign to replicate settings from
    BASE_CAMPAIGN_ID = "54bd46dab4"
    TEST_EMAIL = "pb@btscc.co.uk"

    def __init__(self, api_key: str):
        self.api_key = api_key
        # Extract data centre from key suffix (e.g. "us3")
        self.dc = api_key.split("-")[-1]
        self.base_url = f"https://{self.dc}.api.mailchimp.com/3.0"
        self.auth = ("anystring", api_key)

    def _api(self, method: str, endpoint: str, json_data: dict = None):
        """Make Mailchimp API request"""
        url = f"{self.base_url}{endpoint}"
        resp = requests.request(method, url, auth=self.auth, json=json_data)
        if resp.status_code >= 400:
            print(f"Mailchimp API error ({resp.status_code}): {resp.text}")
            resp.raise_for_status()
        return resp.json() if resp.text else {}

    def create_draft(self) -> str:
        """Replicate base campaign to create a new draft"""
        print("Creating draft campaign in Mailchimp...")
        result = self._api("POST", f"/campaigns/{self.BASE_CAMPAIGN_ID}/actions/replicate")
        campaign_id = result["id"]
        web_id = result["web_id"]
        print(f"  Draft created: id={campaign_id}, web_id={web_id}")

        # Update the title and subject with this week's date
        date_str = datetime.now().strftime("%d %B %Y")
        self._api("PATCH", f"/campaigns/{campaign_id}", {
            "settings": {
                "title": f"Mortgage Lab Weekly Newsletter - {date_str}",
                "subject_line": "Mortgage Lab Weekly Newsletter",
            }
        })
        print(f"  Updated title with date: {date_str}")

        return campaign_id

    def upload_html(self, campaign_id: str, html: str):
        """Set the HTML content of a campaign"""
        print("Uploading newsletter HTML to campaign...")
        self._api("PUT", f"/campaigns/{campaign_id}/content", {
            "html": html
        })
        print("  HTML content uploaded")

    def send_test_email(self, campaign_id: str):
        """Send a test email to preview the draft"""
        print(f"Sending test email to {self.TEST_EMAIL}...")
        self._api("POST", f"/campaigns/{campaign_id}/actions/test", {
            "test_emails": [self.TEST_EMAIL],
            "send_type": "html"
        })
        print(f"  Test email sent to {self.TEST_EMAIL}")

    def publish(self, html: str):
        """Full publish flow: create draft, upload HTML, send test email"""
        campaign_id = self.create_draft()
        self.upload_html(campaign_id, html)
        self.send_test_email(campaign_id)
        print(f"\nDraft campaign ready for review in Mailchimp")
        return campaign_id


def main():
    """Find the latest newsletter HTML and publish to Mailchimp"""
    api_key = os.getenv("MAILCHIMP_API_KEY")
    if not api_key:
        print("ERROR: MAILCHIMP_API_KEY environment variable not set")
        sys.exit(1)

    # Find the latest newsletter HTML
    output_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "output")
    html_files = sorted(glob.glob(os.path.join(output_dir, "newsletter_*.html")))

    if not html_files:
        print("ERROR: No newsletter HTML files found in output/")
        sys.exit(1)

    latest_html_path = html_files[-1]
    print(f"Using newsletter: {os.path.basename(latest_html_path)}")

    with open(latest_html_path, "r", encoding="utf-8") as f:
        html = f.read()

    publisher = MailchimpPublisher(api_key)
    publisher.publish(html)


if __name__ == "__main__":
    main()

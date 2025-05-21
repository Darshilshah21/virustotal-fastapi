from app.services.virustotal import fetch_and_save
from app.models.database import SessionLocal
from time import sleep

identifiers = [
    "virustotal.com", "8.8.8.8", "example.com", "microsoft.com", "github.com"
    # "google.com", "cloudflare.com", "facebook.com", "apple.com", "youtube.com",
    # "amazon.com", "linkedin.com", "twitter.com", "zoom.us", "stackoverflow.com",
    # "reddit.com", "netflix.com", "bbc.com", "cnn.com", "nytimes.com",
    # "dropbox.com", "drive.google.com", "instagram.com", "tiktok.com", "bing.com",
    # "pinterest.com", "paypal.com", "quora.com", "wikipedia.org", "nasa.gov",
    # "oracle.com", "ibm.com", "mit.edu", "harvard.edu", "intel.com",
    # "nvidia.com", "tesla.com", "openai.com", "bitbucket.org", "slack.com",
    # "skype.com", "adobe.com", "ubuntu.com", "debian.org", "archlinux.org",
    # "duckduckgo.com", "mozilla.org", "salesforce.com", "zendesk.com", "spotify.com",
    # "hulu.com", "booking.com", "airbnb.com", "medium.com", "npmjs.com",
    # "python.org", "nodejs.org", "rust-lang.org", "golang.org", "gitlab.com",
    # "digitalocean.com", "heroku.com", "vercel.com", "firebase.google.com", "cloud.google.com",
    # "aws.amazon.com", "azure.microsoft.com", "bitnami.com", "postman.com", "datadog.com",
    # "newrelic.com", "grafana.com", "kaggle.com", "huggingface.co", "colab.research.google.com",
    # "replit.com", "codepen.io", "jsfiddle.net", "codesandbox.io", "wix.com",
    # "shopify.com", "bigcommerce.com", "squareup.com", "paypalobjects.com", "weather.com",
    # "accuweather.com", "bbc.co.uk", "gov.uk", "whitehouse.gov", "who.int",
    # "cdc.gov", "fda.gov", "usda.gov", "unesco.org", "github.io",
    # "glitch.com", "surveymonkey.com", "typeform.com", "notion.so"
]

def ingest_all_data():
    db = SessionLocal()
    for identifier in identifiers:
        success = fetch_and_save(identifier, db)
        print(f"Ingested: {identifier}" if success else f"Skipped: {identifier}")
        sleep(16)
    db.close()

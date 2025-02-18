from flask import Flask, request, render_template
import requests
from urllib.parse import urlparse

app = Flask(__name__)

# Known brands to detect potential phishing
KNOWN_BRANDS = ['paypal', 'microsoft', 'google', 'amazon', 'bank']

@app.route("/", methods=["GET", "POST"])
def check_url():
    result = None
    issues = []
    content = None

    if request.method == "POST":
        url = request.form.get("url", "").strip()
        try:
            # Fetch the page content (no longer converting to lowercase)
            response = requests.get(url, timeout=5)
            content = response.text  # Keep original case!

            # Parse the URL
            parsed_url = urlparse(url)
            domain = parsed_url.netloc.lower()  # Only domain should be lowercase

            # 1. Check for suspicious links (e.g., mismatched domains)
            if 'http://' in content or 'https://' in content:
                issues.append("Suspicious links detected (possibly redirecting).")

            # 2. Check for brand spoofing (e.g., known brands in content)
            for brand in KNOWN_BRANDS:
                if brand.lower() in content.lower():  # Convert only for comparison
                    issues.append(f"Possible brand spoofing detected: {brand}.")

            # 3. Check for unusual URL patterns (e.g., long subdomains or hyphens)
            if '-' in domain:
                issues.append("Hyphenated domains detected (common in phishing).")
            if len(domain.split('.')) > 3:
                issues.append("Excessive subdomains detected.")

            # 4. Check for embedded resources (e.g., iframes, hidden forms, or JavaScript)
            if '<iframe' in content:
                issues.append("Embedded iframes detected (possible content hiding).")
            if '<script' in content:
                issues.append("Embedded JavaScript detected (potential malicious behavior).")
            if '<form' in content and 'hidden' in content:
                issues.append("Hidden forms detected (data harvesting risk).")

            # 5. Check for excessive popups or redirects
            if content.count("window.location") > 2:
                issues.append("Multiple redirects detected (potential phishing).")

            # Decide result based on detected issues
            if issues:
                result = "BAD: Malicious indicators detected."
            else:
                result = "SAFE: No significant issues detected."
        except requests.RequestException:
            result = "ERROR: Could not fetch the URL."

    elif request.method == "GET":
        result = None
        issues = None

    return render_template("index.html", result=result, issues=issues, content=content)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

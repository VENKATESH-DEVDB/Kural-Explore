from flask import Flask, render_template, request
import requests

app = Flask(__name__)

# Thirukkural API - open source, no key needed
# https://github.com/nramc/thirukkural-api
BASE_URL = "https://tamil-kural-api.vercel.app/api/kural"


@app.route("/", methods=["GET", "POST"])
def index():
    kural = None
    error = None
    number = ""

    if request.method == "POST":
        number = request.form.get("kural_number", "").strip()

        # --- Input validation ---
        if not number.isdigit():
            error = "Please enter a valid number."
        elif not (1 <= int(number) <= 1330):
            error = "Kural number must be between 1 and 1330."
        else:
            # --- Call the external API ---
            try:
                response = requests.get(f"{BASE_URL}/{number}", timeout=5)
                if response.status_code == 200:
                    kural = response.json()
                else:
                    error = f"API error (status {response.status_code}). Try again later."
            except requests.exceptions.Timeout:
                error = "The API took too long to respond. Try again."
            except requests.exceptions.RequestException:
                error = "Could not reach the Thirukkural API. Check your internet connection."

    return render_template(
        "index.html", kural=kural, error=error, number=number
    )


if __name__ == "__main__":
    app.run(debug=True)
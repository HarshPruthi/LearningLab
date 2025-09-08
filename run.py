from app import create_app
import os

app = create_app()

if __name__ == "__main__":
    use_ssl = os.environ.get("USE_SSL", "0") == "1"
    ssl_context = "adhoc" if use_ssl else None
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=True, ssl_context=ssl_context)

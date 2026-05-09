from app import app
import warnings
warnings.filterwarnings("ignore")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
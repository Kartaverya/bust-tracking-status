import os
from flask import Flask, render_template, request
from datetime import datetime
import pytesseract
from PIL import Image
import uuid

app = Flask(__name__)
BUS_NUMBERS = [1, 2, 3, 4]
bus_status = {num: {'arrived': False, 'time': None} for num in BUS_NUMBERS}

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files["file"]
        if file:
            filename=f"uploads/{uuid.uuid4().hex}.jpg"
            os.makedirs("uploads",exist_ok=True)
            file.save(filename)
            img = Image.open(filename)
            text = pytesseract.image_to_string(img, config="--psm 6")
            print("OCR Text:", text)  # Debugging
            for num in BUS_NUMBERS:
                if str(num) in text:
                    bus_status[num]['arrived'] = True
                    bus_status[num]['time'] = datetime.now().strftime("%H:%M:%S")
    return render_template("index.html", bus_status=bus_status)

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0",port=port)

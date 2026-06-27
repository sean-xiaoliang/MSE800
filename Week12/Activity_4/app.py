from flask import Flask

app = Flask(__name__)

PAGE = """
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Image Loader</title>
<style>
  * { box-sizing: border-box; }
  body {
    font-family: -apple-system, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    background: #eef0f4;
    color: #2b2f3a;
    margin: 0;
    padding: 40px 16px;
  }
  .wrap { max-width: 760px; margin: 0 auto; }
  h1 { text-align: center; font-size: 40px; font-weight: 800; margin: 0 0 32px; }

  .dropzone {
    border: 2px dashed #aeb4c2;
    border-radius: 14px;
    background: #fff;
    padding: 56px 24px;
    text-align: center;
    transition: border-color .15s, background .15s;
  }
  .dropzone.dragover { border-color: #3b82f6; background: #f3f8ff; }
  .dropzone p { font-size: 20px; color: #4b5160; margin: 0 0 20px; }

  .browse {
    background: #4a89dc;
    color: #fff;
    border: none;
    border-radius: 8px;
    padding: 14px 26px;
    font-size: 18px;
    cursor: pointer;
  }
  .browse:hover { background: #3b7bd0; }

  .card {
    background: #fff;
    border-radius: 12px;
    box-shadow: 0 1px 4px rgba(0,0,0,.06);
    padding: 18px 22px;
    margin-top: 26px;
  }
  .info { font-size: 17px; color: #2b2f3a; }
  .preview { padding: 22px; text-align: center; }
  .preview img { max-width: 100%; border-radius: 6px; }
  .hidden { display: none; }
</style>
</head>
<body>
  <div class="wrap">
    <h1>Image Loader</h1>

    <div class="dropzone" id="dropzone">
      <p>Drag &amp; drop an image here, or</p>
      <button type="button" class="browse" id="browseBtn">Browse Files</button>
      <input type="file" id="fileInput" accept="image/*" class="hidden">
    </div>

    <div class="card info hidden" id="infoCard"></div>
    <div class="card preview hidden" id="previewCard">
      <img id="previewImg" alt="Loaded image">
    </div>
  </div>

<script>
  const dropzone = document.getElementById("dropzone");
  const fileInput = document.getElementById("fileInput");
  const browseBtn = document.getElementById("browseBtn");
  const infoCard = document.getElementById("infoCard");
  const previewCard = document.getElementById("previewCard");
  const previewImg = document.getElementById("previewImg");

  browseBtn.addEventListener("click", () => fileInput.click());
  fileInput.addEventListener("change", () => handleFile(fileInput.files[0]));

  ["dragenter", "dragover"].forEach(evt =>
    dropzone.addEventListener(evt, e => {
      e.preventDefault();
      dropzone.classList.add("dragover");
    })
  );
  ["dragleave", "drop"].forEach(evt =>
    dropzone.addEventListener(evt, e => {
      e.preventDefault();
      dropzone.classList.remove("dragover");
    })
  );
  dropzone.addEventListener("drop", e => handleFile(e.dataTransfer.files[0]));

  function handleFile(file) {
    if (!file) return;
    if (!file.type.startsWith("image/")) {
      infoCard.textContent = "Please choose an image file.";
      infoCard.classList.remove("hidden");
      previewCard.classList.add("hidden");
      return;
    }
    const sizeKB = (file.size / 1024).toFixed(1);
    infoCard.textContent = `${file.name} — ${file.type} — ${sizeKB} KB`;
    infoCard.classList.remove("hidden");

    const reader = new FileReader();
    reader.onload = e => {
      previewImg.src = e.target.result;
      previewCard.classList.remove("hidden");
    };
    reader.readAsDataURL(file);
  }
</script>
</body>
</html>
"""


@app.route("/")
def index():
    return PAGE


if __name__ == "__main__":
    app.run(debug=True)

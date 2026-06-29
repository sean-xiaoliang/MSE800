v# Activity 4 — Image Loader (Flask)

A small Flask web application that lets you load an image from your local system
and display it in the browser. Supports both **drag & drop** and a **Browse Files**
button, and shows the file's name, type, and size before previewing it.

## Features
- Drag & drop an image onto the drop zone, or click **Browse Files**
- Accepts any image type (PNG, JPG, JPEG, GIF, WebP, ...)
- Shows file info: `name — type — size KB`
- Instant in-browser preview (no page reload)
- Friendly message if a non-image file is chosen

## Requirements
- Python 3
- Flask (`pip install flask`)

## How to run
```bash
python app.py
```
Then open http://127.0.0.1:5000 in your browser.

## How to use
1. Drag an image into the dashed area, **or** click **Browse Files** and pick one.
2. The file details appear, followed by a preview of the image.

## Files
- `app.py` — the Flask application (serves the page; preview is handled client-side)
- `screenshot.png` — screenshot of the app with an image loaded

## Notes
The image is displayed client-side using the browser's `FileReader`, so Flask
serves the page and the image never has to be uploaded to the server.

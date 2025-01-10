"""
Flask application for the image generator service.
"""

import os
from pathlib import Path
from typing import Optional

from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename

from .model import StyleGANModel
from .storage import IPFSStorage

UPLOAD_FOLDER = Path("uploads")
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}

def allowed_file(filename: str) -> bool:
    """Check if the file extension is allowed."""
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

def create_app(model: Optional[StyleGANModel] = None, storage: Optional[IPFSStorage] = None) -> Flask:
    """Create and configure the Flask application."""
    app = Flask(__name__)
    app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
    app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024  # 16MB max file size

    if not UPLOAD_FOLDER.exists():
        UPLOAD_FOLDER.mkdir(parents=True)

    if model is None:
        model = StyleGANModel()
    if storage is None:
        storage = IPFSStorage()

    @app.route("/upload", methods=["POST"])
    def upload_file():
        """Handle image upload for training."""
        if "file" not in request.files:
            return jsonify({"error": "No file part"}), 400
        
        file = request.files["file"]
        if file.filename == "":
            return jsonify({"error": "No selected file"}), 400
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = UPLOAD_FOLDER / filename
            file.save(filepath)
            
            try:
                # Add to training dataset
                model.add_training_image(filepath)
                return jsonify({"message": "File uploaded successfully", "filename": filename}), 200
            except Exception as e:
                return jsonify({"error": str(e)}), 500
        
        return jsonify({"error": "File type not allowed"}), 400

    @app.route("/train", methods=["POST"])
    def train_model():
        """Trigger model training."""
        try:
            epochs = request.json.get("epochs", 1)
            loss = model.train(epochs=epochs)
            return jsonify({"message": "Training completed", "loss": loss}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @app.route("/generate", methods=["POST"])
    def generate_image():
        """Generate a new image based on the prompt."""
        try:
            prompt = request.json.get("prompt")
            if not prompt:
                return jsonify({"error": "No prompt provided"}), 400

            # Generate image
            image_path = model.generate(prompt)
            
            # Upload to IPFS
            ipfs_hash = storage.upload_file(image_path)
            
            return jsonify({
                "message": "Image generated successfully",
                "ipfs_hash": ipfs_hash,
                "ipfs_url": f"https://gateway.pinata.cloud/ipfs/{ipfs_hash}"
            }), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    return app 
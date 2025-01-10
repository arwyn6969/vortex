# Image Generator AI Application

A local image generator AI application that allows users to upload images, train a centralized StyleGAN2 model, and generate new images with the learned styles. Generated images are automatically stored in IPFS using Pinata for decentralized access.

## Features

- **Image Upload**: Upload training images in common formats (PNG, JPG, JPEG)
- **Model Training**: Train a StyleGAN2 model on uploaded images
- **Image Generation**: Generate new images based on text prompts
- **IPFS Storage**: Automatic storage of generated images on IPFS via Pinata
- **REST API**: Simple HTTP endpoints for all functionality

## Prerequisites

- Python 3.x
- CUDA-capable GPU (recommended for training)
- Pinata API credentials

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd <repository-name>
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the project root with your Pinata credentials:
```env
PINATA_API_KEY=your_api_key
PINATA_API_SECRET=your_api_secret
PINATA_JWT=your_jwt_token
```

## Usage

### Starting the Server

Run the application using:
```bash
python -m vortex.src.image_generator
```

Optional command-line arguments:
- `--host`: Server host (default: 127.0.0.1)
- `--port`: Server port (default: 5000)
- `--debug`: Enable debug mode

### API Endpoints

#### 1. Upload Images
Upload images for training the model.

```bash
curl -X POST -F "file=@/path/to/image.jpg" http://127.0.0.1:5000/upload
```

Response:
```json
{
    "message": "File uploaded successfully",
    "filename": "image.jpg"
}
```

#### 2. Train Model
Train the model on uploaded images.

```bash
curl -X POST -H "Content-Type: application/json" -d '{"epochs": 1}' http://127.0.0.1:5000/train
```

Response:
```json
{
    "message": "Training completed",
    "loss": 0.1234
}
```

#### 3. Generate Images
Generate new images based on text prompts.

```bash
curl -X POST -H "Content-Type: application/json" -d '{"prompt": "A beautiful landscape"}' http://127.0.0.1:5000/generate
```

Response:
```json
{
    "message": "Image generated successfully",
    "ipfs_hash": "QmXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXx",
    "ipfs_url": "https://gateway.pinata.cloud/ipfs/QmXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXx"
}
```

## Technical Details

### Model Architecture

The application uses StyleGAN2 with the following components:

1. **Generator**:
   - Mapping network for style transformation
   - Initial convolutional block
   - Progressive upsampling layers
   - Output layer generating RGB images

2. **Discriminator**:
   - Progressive downsampling layers
   - Binary classification output

### Training Process

- Images are resized to 256x256 pixels
- Normalized to range [-1, 1]
- Trained using adversarial loss
- Adam optimizer with learning rate 0.0002
- Batch size of 32 (configurable)

### Storage

- Uploaded images stored locally in `uploads/` directory
- Generated images stored locally in `generated/` directory
- Generated images automatically uploaded to IPFS via Pinata
- IPFS hashes and URLs returned for permanent access

## Directory Structure

```
vortex/
├── src/
│   └── image_generator/
│       ├── __init__.py
│       ├── __main__.py
│       ├── app.py
│       ├── model.py
│       └── storage.py
├── uploads/
├── generated/
├── .env
└── requirements.txt
```

## Security Considerations

- File upload size limited to 16MB
- Allowed file extensions: .png, .jpg, .jpeg
- Environment variables for sensitive credentials
- Input validation on all endpoints
- Secure filename handling

## Limitations

- Currently generates random images without text conditioning
- Training requires significant computational resources
- Image size fixed at 256x256 pixels
- No model persistence between restarts

## Future Improvements

1. Implement text-to-image conditioning
2. Add model checkpointing and loading
3. Support for larger image sizes
4. Progressive growing during training
5. Web interface for easier interaction
6. Multi-GPU training support
7. Style mixing capabilities
8. Image interpolation features

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

[MIT License](LICENSE)

## Acknowledgments

- StyleGAN2 paper and implementation
- Pinata IPFS service
- Flask web framework
- PyTorch deep learning framework
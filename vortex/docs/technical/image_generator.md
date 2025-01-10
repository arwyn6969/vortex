# Image Generator Technical Documentation

## System Architecture

The image generator system consists of three main components:

1. **Web Server (Flask)**
   - Handles HTTP requests
   - Manages file uploads
   - Coordinates between model and storage
   - Provides RESTful API endpoints

2. **StyleGAN2 Model**
   - Generator network for image synthesis
   - Discriminator network for training
   - Image dataset management
   - Training pipeline

3. **IPFS Storage (Pinata)**
   - Decentralized storage for generated images
   - Permanent content addressing
   - Public access via IPFS gateway

## Component Details

### Web Server

#### Endpoints

1. `/upload` (POST)
   - Accepts multipart/form-data
   - Validates file type and size
   - Stores in local filesystem
   - Adds to training dataset

2. `/train` (POST)
   - Accepts JSON with epochs parameter
   - Runs training loop
   - Returns training loss
   - Handles training errors

3. `/generate` (POST)
   - Accepts JSON with prompt
   - Generates new image
   - Uploads to IPFS
   - Returns access information

#### Configuration

- Max file size: 16MB
- Allowed extensions: .png, .jpg, .jpeg
- Upload directory: ./uploads
- Generated directory: ./generated

### StyleGAN2 Model

#### Generator Architecture

```
Input (z) → Mapping Network → Initial Block → Upsampling Blocks → Output
```

1. **Mapping Network**
   - Input: Random latent vector (512 dim)
   - Two fully connected layers
   - ReLU activation
   - Output: Style vector (w)

2. **Initial Block**
   - Input: Style vector
   - Transposed convolution (4x4)
   - Batch normalization
   - ReLU activation

3. **Upsampling Blocks**
   - 8 progressive blocks
   - Each block:
     - Transposed convolution
     - Batch normalization
     - ReLU activation
   - Progressive channel reduction

4. **Output Layer**
   - 3x3 convolution
   - Tanh activation
   - RGB image output (256x256x3)

#### Discriminator Architecture

```
Input Image → Downsampling Blocks → Classification
```

1. **Downsampling Blocks**
   - 8 progressive blocks
   - Each block:
     - Convolution (4x4)
     - Batch normalization
     - LeakyReLU
   - Progressive channel increase

2. **Classification Layer**
   - Final convolution
   - Sigmoid activation
   - Binary output (real/fake)

#### Training Process

1. **Data Preparation**
   - Load images from disk
   - Resize to 256x256
   - Convert to RGB
   - Normalize to [-1, 1]

2. **Training Loop**
   - Alternate G/D training
   - Adversarial loss
   - Adam optimizer
   - Gradient penalty
   - Progress tracking

### IPFS Storage

#### Pinata Integration

1. **Authentication**
   - API Key
   - API Secret
   - JWT token
   - Environment variables

2. **File Upload**
   - Local file reading
   - Pinata API call
   - Metadata attachment
   - Hash retrieval

3. **Access**
   - IPFS gateway URLs
   - Content addressing
   - Permanent storage

## Data Flow

1. **Image Upload**
```
Client → Flask → Filesystem → Training Dataset
```

2. **Training**
```
Dataset → DataLoader → Model → Loss Calculation → Model Update
```

3. **Generation**
```
Prompt → Generator → Local File → Pinata → IPFS
```

## Error Handling

1. **Upload Errors**
   - File size validation
   - Type validation
   - Storage errors
   - Database errors

2. **Training Errors**
   - Out of memory
   - Convergence issues
   - Dataset errors
   - GPU errors

3. **Generation Errors**
   - Model errors
   - Storage errors
   - IPFS errors
   - Network errors

## Performance Considerations

1. **Memory Management**
   - Batch size optimization
   - Image size limitations
   - GPU memory usage
   - Dataset loading

2. **Storage Optimization**
   - Local file cleanup
   - IPFS pinning strategy
   - Cache management
   - Disk space monitoring

3. **Training Efficiency**
   - GPU utilization
   - Batch processing
   - Progressive growing
   - Loss monitoring

## Security

1. **File Upload Security**
   - Size limits
   - Type validation
   - Path traversal prevention
   - Malware scanning

2. **API Security**
   - Input validation
   - Rate limiting
   - Error handling
   - Credential protection

3. **Storage Security**
   - Access control
   - Encryption
   - Backup strategy
   - Monitoring

## Monitoring and Logging

1. **Application Logs**
   - Request logging
   - Error tracking
   - Performance metrics
   - Security events

2. **Model Metrics**
   - Training progress
   - Loss values
   - Generation quality
   - Resource usage

3. **Storage Metrics**
   - Upload success rate
   - IPFS availability
   - Storage usage
   - Access patterns

## Configuration

1. **Environment Variables**
```env
PINATA_API_KEY=your_api_key
PINATA_API_SECRET=your_api_secret
PINATA_JWT=your_jwt_token
```

2. **Model Parameters**
```python
latent_dim = 512
n_layers = 8
learning_rate = 0.0002
batch_size = 32
```

3. **Server Configuration**
```python
max_content_length = 16 * 1024 * 1024  # 16MB
allowed_extensions = {"png", "jpg", "jpeg"}
```

## Development Guidelines

1. **Code Style**
   - PEP 8 compliance
   - Type hints
   - Documentation strings
   - Clean architecture

2. **Testing**
   - Unit tests
   - Integration tests
   - Performance tests
   - Security tests

3. **Version Control**
   - Feature branches
   - Pull requests
   - Code review
   - Version tagging

## Deployment

1. **Requirements**
   - Python 3.x
   - CUDA support
   - Storage capacity
   - Network bandwidth

2. **Environment Setup**
   - Virtual environment
   - Dependencies
   - Configuration
   - Permissions

3. **Monitoring**
   - Health checks
   - Error alerts
   - Performance monitoring
   - Resource usage 
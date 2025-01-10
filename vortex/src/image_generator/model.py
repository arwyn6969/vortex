"""
StyleGAN2 model implementation for image generation.
"""

import os
from pathlib import Path
from typing import Optional, Union, List

import torch
import torch.nn as nn
import torch.optim as optim
import torchvision.transforms as transforms
from PIL import Image
from torch.utils.data import Dataset, DataLoader
from tqdm import tqdm

class ImageDataset(Dataset):
    """Dataset for training images."""
    
    def __init__(self, image_paths: List[Path], transform=None):
        self.image_paths = image_paths
        self.transform = transform or transforms.Compose([
            transforms.Resize((256, 256)),
            transforms.ToTensor(),
            transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
        ])
    
    def __len__(self) -> int:
        return len(self.image_paths)
    
    def __getitem__(self, idx: int) -> torch.Tensor:
        image_path = self.image_paths[idx]
        image = Image.open(image_path).convert("RGB")
        if self.transform:
            image = self.transform(image)
        return image

class Generator(nn.Module):
    """StyleGAN2 Generator implementation."""
    
    def __init__(self, latent_dim: int = 512, n_layers: int = 8):
        super().__init__()
        self.latent_dim = latent_dim
        
        # Mapping network
        self.mapping = nn.Sequential(
            nn.Linear(latent_dim, latent_dim),
            nn.ReLU(),
            nn.Linear(latent_dim, latent_dim),
            nn.ReLU()
        )
        
        # Initial block
        self.initial = nn.Sequential(
            nn.ConvTranspose2d(latent_dim, 512, 4, 1, 0),
            nn.BatchNorm2d(512),
            nn.ReLU()
        )
        
        # Upsampling blocks
        layers = []
        in_channels = 512
        for i in range(n_layers):
            out_channels = max(64, in_channels // 2)
            layers.extend([
                nn.ConvTranspose2d(in_channels, out_channels, 4, 2, 1),
                nn.BatchNorm2d(out_channels),
                nn.ReLU()
            ])
            in_channels = out_channels
        
        layers.append(nn.Conv2d(out_channels, 3, 3, 1, 1))
        layers.append(nn.Tanh())
        
        self.layers = nn.Sequential(*layers)
    
    def forward(self, z: torch.Tensor) -> torch.Tensor:
        w = self.mapping(z)
        x = w.view(-1, self.latent_dim, 1, 1)
        x = self.initial(x)
        return self.layers(x)

class Discriminator(nn.Module):
    """StyleGAN2 Discriminator implementation."""
    
    def __init__(self, n_layers: int = 8):
        super().__init__()
        
        layers = []
        in_channels = 3
        out_channels = 64
        
        for i in range(n_layers):
            layers.extend([
                nn.Conv2d(in_channels, out_channels, 4, 2, 1),
                nn.BatchNorm2d(out_channels),
                nn.LeakyReLU(0.2)
            ])
            in_channels = out_channels
            out_channels = min(512, out_channels * 2)
        
        layers.append(nn.Conv2d(in_channels, 1, 4, 1, 0))
        layers.append(nn.Sigmoid())
        
        self.layers = nn.Sequential(*layers)
    
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.layers(x)

class StyleGANModel:
    """StyleGAN2 model for image generation."""
    
    def __init__(self, 
                 latent_dim: int = 512,
                 n_layers: int = 8,
                 device: Optional[str] = None):
        self.latent_dim = latent_dim
        self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")
        
        self.generator = Generator(latent_dim, n_layers).to(self.device)
        self.discriminator = Discriminator(n_layers).to(self.device)
        
        self.g_optimizer = optim.Adam(self.generator.parameters(), lr=0.0002, betas=(0.5, 0.999))
        self.d_optimizer = optim.Adam(self.discriminator.parameters(), lr=0.0002, betas=(0.5, 0.999))
        
        self.criterion = nn.BCELoss()
        self.training_images: List[Path] = []
    
    def add_training_image(self, image_path: Union[str, Path]) -> None:
        """Add an image to the training dataset."""
        path = Path(image_path)
        if not path.exists():
            raise FileNotFoundError(f"Image not found: {image_path}")
        self.training_images.append(path)
    
    def train(self, epochs: int = 1, batch_size: int = 32) -> float:
        """Train the model on the collected images."""
        if not self.training_images:
            raise ValueError("No training images available")
        
        dataset = ImageDataset(self.training_images)
        dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=True)
        
        final_g_loss = 0.0
        
        for epoch in range(epochs):
            progress_bar = tqdm(dataloader, desc=f"Epoch {epoch+1}/{epochs}")
            
            for real_images in progress_bar:
                batch_size = real_images.size(0)
                real_images = real_images.to(self.device)
                
                # Train Discriminator
                self.d_optimizer.zero_grad()
                label_real = torch.ones(batch_size, 1).to(self.device)
                label_fake = torch.zeros(batch_size, 1).to(self.device)
                
                output_real = self.discriminator(real_images)
                d_loss_real = self.criterion(output_real, label_real)
                
                z = torch.randn(batch_size, self.latent_dim).to(self.device)
                fake_images = self.generator(z)
                output_fake = self.discriminator(fake_images.detach())
                d_loss_fake = self.criterion(output_fake, label_fake)
                
                d_loss = d_loss_real + d_loss_fake
                d_loss.backward()
                self.d_optimizer.step()
                
                # Train Generator
                self.g_optimizer.zero_grad()
                output_fake = self.discriminator(fake_images)
                g_loss = self.criterion(output_fake, label_real)
                g_loss.backward()
                self.g_optimizer.step()
                
                progress_bar.set_postfix({
                    "D Loss": f"{d_loss.item():.4f}",
                    "G Loss": f"{g_loss.item():.4f}"
                })
                
                final_g_loss = g_loss.item()
        
        return final_g_loss
    
    def generate(self, prompt: str, output_dir: str = "generated") -> Path:
        """Generate an image based on the prompt."""
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)
        
        # For now, we ignore the prompt and generate random images
        # TODO: Implement text-to-image conditioning
        z = torch.randn(1, self.latent_dim).to(self.device)
        
        with torch.no_grad():
            fake_image = self.generator(z)
            fake_image = (fake_image + 1) / 2.0  # Denormalize
            fake_image = fake_image.squeeze(0).cpu()
        
        # Convert to PIL Image and save
        transform = transforms.ToPILImage()
        image = transform(fake_image)
        
        # Create a unique filename based on the prompt
        filename = f"generated_{hash(prompt) % 10000:04d}.png"
        save_path = output_path / filename
        image.save(save_path)
        
        return save_path 
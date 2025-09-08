# Project Template Based on Tennis Analysis Docker/Scripts Pattern

This template provides a ready-to-use structure for containerizing ML/AI projects based on the successful patterns from the tennis_analysis project.

## 🚀 Quick Start

1. Copy this template to your project:
   ```bash
   cp -r docs/project-template/* your-project/
   ```

2. Customize the configuration:
   - Edit `requirements-*.txt` files with your dependencies
   - Update `docker/Dockerfile.base` with your system requirements
   - Modify scripts in `scripts/` for your specific needs

3. Build and run:
   ```bash
   chmod +x scripts/*.sh
   ./start.sh
   ```

## 📁 Template Structure

```
project-template/
├── docker/
│   ├── Dockerfile.base
│   ├── Dockerfile.final
│   ├── docker-compose.dev.yml
│   └── .dockerignore
├── scripts/
│   ├── build-base.sh
│   ├── build-final.sh
│   ├── run-dev.sh
│   ├── install-deps.sh
│   ├── test-env.sh
│   └── cleanup.sh
├── requirements-base.txt
├── requirements-ml.txt
├── requirements-dev.txt
├── Dockerfile
├── docker-compose.yml
├── start.sh
└── README.md
```

## 🔧 Customization Guide

### 1. System Dependencies
Edit `docker/Dockerfile.base` to add your system packages:
```dockerfile
RUN apt-get update && apt-get install -y \
    your-system-package \
    another-package \
    && rm -rf /var/lib/apt/lists/*
```

### 2. Python Dependencies
Update requirements files based on your project needs:
- `requirements-base.txt`: Core dependencies (numpy, requests, etc.)
- `requirements-ml.txt`: ML frameworks (torch, tensorflow, etc.)
- `requirements-dev.txt`: Development tools (jupyter, pytest, etc.)

### 3. Port Configuration
Modify ports in docker-compose files for your application:
```yaml
ports:
  - "8080:8080"  # Your app port
  - "8888:8888"  # Jupyter (optional)
```

### 4. Volume Mounts
Adjust volume mounts for your data directories:
```yaml
volumes:
  - ./your-data:/app/data
  - ./your-output:/app/output
```

## 🎯 Usage Examples

### For Computer Vision Projects
```bash
# requirements-ml.txt
opencv-python==4.8.0
torch==2.0.0
torchvision==0.15.0
ultralytics==8.0.20
```

### For NLP Projects
```bash
# requirements-ml.txt
transformers==4.30.0
torch==2.0.0
datasets==2.12.0
tokenizers==0.13.0
```

### For Data Science Projects
```bash
# requirements-base.txt
pandas==2.0.0
numpy==1.24.0
matplotlib==3.7.0
seaborn==0.12.0
scikit-learn==1.3.0
```

## 📋 Project-Specific Adaptations

### Web Applications
Add nginx service to docker-compose:
```yaml
nginx:
  image: nginx:alpine
  ports: ["80:80"]
  volumes: ["./nginx.conf:/etc/nginx/nginx.conf"]
```

### Database-Driven Projects
Add database service:
```yaml
postgres:
  image: postgres:15
  environment:
    POSTGRES_DB: yourdb
    POSTGRES_USER: user
    POSTGRES_PASSWORD: password
  volumes: ["postgres_data:/var/lib/postgresql/data"]
```

### GPU Projects
Enable GPU support:
```yaml
deploy:
  resources:
    reservations:
      devices:
        - driver: nvidia
          count: all
          capabilities: [gpu]
```

## 🔍 Testing Your Setup

Run the validation script:
```bash
./scripts/test-env.sh
```

Expected output:
```
✅ Python 3.8+ - OK
✅ Core dependencies - OK
✅ ML dependencies - OK
✅ Project modules - OK
```

## 🎉 Ready to Go!

Once customized, your project will have:
- ✅ Multi-stage Docker builds
- ✅ Automated dependency management
- ✅ Development/production environments
- ✅ Interactive setup scripts
- ✅ Environment validation
- ✅ Error handling and debugging tools

Happy coding! 🚀
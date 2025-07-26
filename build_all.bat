@echo off
REM Build script for Adobe Hackathon Challenge (Windows)
REM Builds both Round 1A and Round 1B Docker images

echo Adobe Hackathon Challenge - Build Script
echo ========================================

REM Check if Docker is available
docker --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Docker is not installed or not in PATH
    exit /b 1
)

echo [INFO] Docker found
docker --version

REM Build Round 1A
echo [INFO] Building Round 1A - PDF Outline Extractor...
cd round1a

docker build --platform linux/amd64 -t pdf-outline-extractor:latest .
if %errorlevel% neq 0 (
    echo [ERROR] Round 1A Docker build failed
    exit /b 1
)

echo [INFO] Round 1A Docker image built successfully
cd ..

REM Build Round 1B
echo [INFO] Building Round 1B - Persona-Driven Intelligence...
cd round1b

docker build --platform linux/amd64 -t persona-intelligence:latest .
if %errorlevel% neq 0 (
    echo [ERROR] Round 1B Docker build failed
    exit /b 1
)

echo [INFO] Round 1B Docker image built successfully
cd ..

REM List built images
echo [INFO] Built Docker images:
docker images | findstr "pdf-outline-extractor persona-intelligence"

echo.
echo [INFO] Build completed successfully!
echo [INFO] You can now run the solutions using:
echo.
echo Round 1A:
echo docker run --rm -v %cd%\input:/app/input -v %cd%\output:/app/output --network none pdf-outline-extractor:latest
echo.
echo Round 1B:
echo docker run --rm -v %cd%\input:/app/input -v %cd%\output:/app/output --network none persona-intelligence:latest

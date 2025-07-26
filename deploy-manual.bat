@echo off
echo Manual Deployment Guide for Adobe Hackathon Project
echo ===================================================
echo.
echo Option 1: Surge.sh (Free Static Hosting)
echo 1. Install Node.js from nodejs.org
echo 2. Open command prompt and run: npm install -g surge
echo 3. Navigate to your project folder
echo 4. Run: surge
echo 5. Follow the prompts to deploy
echo.
echo Option 2: Firebase Hosting (Free)
echo 1. Go to console.firebase.google.com
echo 2. Create new project
echo 3. Enable Hosting
echo 4. Install Firebase CLI: npm install -g firebase-tools
echo 5. Run: firebase login
echo 6. Run: firebase init hosting
echo 7. Run: firebase deploy
echo.
echo Option 3: Render (Free Static Sites)
echo 1. Go to render.com
echo 2. Sign up with GitHub
echo 3. Create new Static Site
echo 4. Connect your repository
echo 5. Deploy automatically
echo.
pause

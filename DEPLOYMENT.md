🌐 CertiVault Deployment Guide (Get Your Live Website Link)
This guide explains the fastest way to deploy your CertiVault React application to a live URL using Vercel, a popular and free hosting service.

Part 1: Connect GitHub to Vercel
Vercel is the easiest platform for deploying React projects, as it automatically detects the configuration files (package.json) and runs the necessary build commands.

Step 1: Create a Vercel Account
Go to the Vercel website and click "Sign Up".

Select "Continue with GitHub" and grant Vercel access to your GitHub account. This allows Vercel to see and deploy your repositories.

Step 2: Import Your Project
Once logged in, click the "Add New..." button (or "New Project").

Vercel will show a list of your GitHub repositories. Find and click the "Import" button next to your CertiVault repository.

Part 2: Configure and Deploy
Vercel is smart enough to detect your React project, but we'll confirm the settings based on the files you uploaded.

Step 3: Configure the Project Settings
On the project configuration screen, Vercel should automatically detect the following settings:

Setting

Value (Should be automatic)

Explanation

Root Directory

./ (The project root)

Indicates your files are in the top folder.

Framework

Vite

This is the build tool defined in your package.json.

Build Command

npm run build

The command Vercel runs to compile your code.

Output Directory

dist

The folder where the compiled website files are saved.

Important: Do not change these default settings. Just ensure they are correctly detected.

Step 4: Final Deployment
Click the "Deploy" button at the bottom of the page.

Vercel will take about 1-2 minutes to clone your repository, install the dependencies, build the project, and assign a domain.

Once complete, Vercel will show a celebratory screen with a "Visit" button and your live public URL (e.g., https://certivault-xyz.vercel.app).

Part 3: Maintaining Your Live Site
Automatic Updates: Every time you push new changes (make a commit) to the main branch of your CertiVault repository on GitHub, Vercel will automatically detect the change and re-deploy your website, ensuring your live link is always up-to-date.

Share Your Link: You can now share this Vercel URL on your resume and professional profiles!
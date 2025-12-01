# How to Post MonkeyPose on GitHub

## Step-by-Step Guide

### 1. Create a GitHub Account

- Go to [github.com](https://github.com)
- Sign up for a free account if you don't have one

### 2. Create a New Repository

- Click the **+** icon in the top-right corner
- Select **New repository**
- **Repository name**: `monkeypose` (or your preferred name)
- **Description**: "Real-time gesture recognition with pose matching using MediaPipe and OpenCV"
- **Visibility**: Public (to share with others) or Private (for personal use)
- **Initialize this repository with**: Leave unchecked (we'll add files manually)
- Click **Create repository**

### 3. Install Git

- **Windows**: Download from [git-scm.com](https://git-scm.com)
- **Mac**: `brew install git`
- **Linux**: `sudo apt-get install git`

### 4. Setup Git Configuration

Open PowerShell/Command Prompt and run:

```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

### 5. Initialize Local Repository

Navigate to your project folder:

```bash
cd C:\Users\Samriddha\Desktop\monkeypose
git init
```

### 6. Add Files to Git

Add all files to staging area:

```bash
git add .
```

Or add specific files:

```bash
git add monkey.py README.md requirements.txt .gitignore
```

### 7. Create First Commit

```bash
git commit -m "Initial commit: Add MonkeyPose gesture recognition project"
```

### 8. Connect to GitHub Repository

Copy the repository URL from GitHub, then run:

```bash
git remote add origin https://github.com/YOUR_USERNAME/monkeypose.git
```

### 9. Push to GitHub

```bash
git branch -M main
git push -u origin main
```

You may be prompted to authenticate. Use:

- **Username**: Your GitHub username
- **Password**: Your GitHub personal access token (create one in GitHub settings → Developer settings → Personal access tokens)

---

## Files to Include in GitHub

### ✅ SHOULD INCLUDE

1. **monkey.py** - Main application file (REQUIRED)
2. **README.md** - Project documentation (REQUIRED)
3. **requirements.txt** - Dependencies list
4. **.gitignore** - Files to ignore
5. **LICENSE** - (Optional but recommended) - Choose MIT, Apache, or GPL

### ❌ SHOULD NOT INCLUDE

1. **monkey_refs/** folder with images (reference images)

   - Too large and better stored separately
   - Users should add their own images

2. **venv311/** - Virtual environment folder (very large)

   - Users can create their own with `python -m venv venv`

3. ****pycache**/** - Python cache files

   - Automatically generated, not needed in repo

4. **.env** - Environment variables

   - Contains sensitive information

5. **\*.log** - Log files

---

## Alternative: Keep Images in Repository

If you want to include reference images:

1. Create a `monkey_refs/` folder in your repo
2. Add your images there
3. Update `.gitignore` to NOT ignore this folder
4. Include instructions in README about image setup

To do this, modify `.gitignore`:

```bash
# Remove or comment out this line if you want to include images:
# monkey_refs/
```

---

## Recommended Repository Structure for GitHub

```
monkeypose/
├── monkey.py              # Main code
├── README.md              # Documentation
├── requirements.txt       # Dependencies
├── .gitignore            # Git ignore file
├── LICENSE               # License file
└── monkey_refs/          # (Optional) Reference images
    ├── monkey1.jpeg
    ├── monkey2.jpeg
    ├── monkey3.jpeg
    ├── monkey4.jpg
    ├── monkey5_converted.jpg
    └── monkey8.jpg
```

---

## Adding a LICENSE File

1. Create a file named `LICENSE` in your project
2. Choose a license type:
   - **MIT License** (most permissive, recommended for most projects)
   - **Apache 2.0** (good for professional projects)
   - **GPL 3.0** (requires derivatives to be open source)

Use GitHub's license template:

- On GitHub repo page → Add file → LICENSE
- Select template

---

## Updating Your Repository

After initial push, to make updates:

```bash
# Make your changes to files

# Stage changes
git add .

# Commit changes
git commit -m "Update: Description of changes"

# Push to GitHub
git push
```

---

## Useful Git Commands

```bash
# Check status
git status

# View commit history
git log

# View changes
git diff

# Undo last commit (keeping changes)
git reset --soft HEAD~1

# View remote URL
git remote -v

# Create a new branch
git checkout -b feature-branch

# Switch branch
git checkout main
```

---

## Share Your Project

After pushing to GitHub:

1. **Copy repository URL**: `https://github.com/YOUR_USERNAME/monkeypose`
2. **Share with others**: Send the URL or create a GitHub release
3. **Create a Release**:
   - Go to Releases → Create new release
   - Tag version: `v1.0.0`
   - Title: `Version 1.0 - Initial Release`
   - Add release notes

---

## Troubleshooting

| Problem                | Solution                                                           |
| ---------------------- | ------------------------------------------------------------------ |
| "Repository not found" | Check URL and make sure you have access                            |
| Authentication failed  | Create personal access token in GitHub settings                    |
| Large files rejected   | Remove from `.gitignore` or use Git LFS                            |
| Wrong branch pushed    | Check with `git branch` and switch with `git checkout branch-name` |

---

## Files Summary for Upload

**MUST INCLUDE:**

- ✅ monkey.py
- ✅ README.md
- ✅ requirements.txt
- ✅ .gitignore

**RECOMMENDED:**

- ✅ LICENSE
- ✅ monkey_refs/ (with images)

**MUST EXCLUDE:**

- ❌ venv311/
- ❌ **pycache**/
- ❌ .pyc files

---

Good luck sharing your project! 🚀

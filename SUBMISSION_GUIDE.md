# Adobe Hackathon Submission Guide

## 📋 Submission Requirements

### What to Submit
1. **Private Git Repository** (GitHub/GitLab/Bitbucket)
2. **Working Dockerfiles** in root directories
3. **Complete source code** with dependencies
4. **Documentation** (README.md + approach_explanation.md)
5. **Submission form** (provided by organizers)

## 🚀 Step-by-Step Submission Process

### Step 1: Create Private Git Repository

#### Option A: GitHub
1. Go to [GitHub](https://github.com)
2. Click "New Repository"
3. Name: `adobe-hackathon-2025-[your-team-name]`
4. Set to **Private** ⚠️ (Important!)
5. Don't initialize with README (you already have one)
6. Click "Create Repository"

#### Option B: GitLab
1. Go to [GitLab](https://gitlab.com)
2. Click "New Project" → "Create blank project"
3. Name: `adobe-hackathon-2025-[your-team-name]`
4. Set visibility to **Private**
5. Uncheck "Initialize repository with a README"
6. Click "Create Project"

### Step 2: Upload Your Code

```bash
# Navigate to your project directory
cd /path/to/your/adobe-project

# Initialize git (if not already done)
git init

# Add all files
git add .

# Commit your work
git commit -m "Initial submission for Adobe Hackathon 2025"

# Add remote origin (replace with your repository URL)
git remote add origin https://github.com/yourusername/adobe-hackathon-2025-yourteam.git

# Push to repository
git push -u origin main
```

### Step 3: Verify Repository Structure

Your repository should look like this:

```
adobe-hackathon-2025-yourteam/
├── README.md                    # Main project documentation
├── round1a/                     # Round 1A Solution
│   ├── Dockerfile              # ⚠️ REQUIRED
│   ├── requirements.txt
│   ├── src/
│   │   └── pdf_outline_extractor.py
│   └── README.md
├── round1b/                     # Round 1B Solution
│   ├── Dockerfile              # ⚠️ REQUIRED
│   ├── requirements.txt
│   ├── src/
│   │   └── persona_intelligence.py
│   └── README.md
├── docs/
│   ├── approach_explanation.md  # ⚠️ REQUIRED (300-500 words)
│   ├── deployment_guide.md
│   └── testing_guide.md
├── samples/
├── build_all.sh
└── build_all.bat
```

### Step 4: Test Your Submission

Before submitting, verify everything works:

```bash
# Clone your repository to a fresh directory
git clone https://github.com/yourusername/adobe-hackathon-2025-yourteam.git test-submission
cd test-submission

# Test Round 1A
cd round1a
docker build --platform linux/amd64 -t test-round1a .
# Test with sample PDFs

# Test Round 1B  
cd ../round1b
docker build --platform linux/amd64 -t test-round1b .
# Test with sample configuration
```

### Step 5: Prepare Submission Package

Create a submission summary document:

```markdown
# Adobe Hackathon 2025 Submission

## Team Information
- **Team Name**: [Your Team Name]
- **Team Members**: [List all members]
- **Contact Email**: [Primary contact]

## Repository Information
- **Repository URL**: https://github.com/yourusername/adobe-hackathon-2025-yourteam
- **Branch**: main
- **Commit Hash**: [latest commit hash]

## Solution Overview
- **Round 1A**: PDF Outline Extraction using PyMuPDF and intelligent pattern recognition
- **Round 1B**: Persona-driven document intelligence with relevance scoring

## Key Features
- AMD64 compatible Docker containers
- Offline operation (no network calls)
- Performance optimized (meets all time constraints)
- Comprehensive documentation and testing

## Build Instructions
```bash
# Round 1A
cd round1a
docker build --platform linux/amd64 -t pdf-outline-extractor .

# Round 1B
cd round1b  
docker build --platform linux/amd64 -t persona-intelligence .
```

## Execution Commands
```bash
# Round 1A
docker run --rm -v $(pwd)/input:/app/input -v $(pwd)/output:/app/output --network none pdf-outline-extractor

# Round 1B
docker run --rm -v $(pwd)/input:/app/input -v $(pwd)/output:/app/output --network none persona-intelligence
```
```

### Step 6: Submit Through Official Channels

1. **Wait for submission instructions** from Adobe organizers
2. **Submit repository URL** when requested
3. **Provide access** to evaluators (they'll give you GitHub usernames to add)
4. **Keep repository private** until told otherwise

## ⚠️ Important Submission Notes

### Repository Requirements
- ✅ **Must be private** until competition deadline
- ✅ **Dockerfile in root** of each solution directory
- ✅ **No hardcoded paths** or file-specific logic
- ✅ **All dependencies** included in containers
- ✅ **Works offline** (--network none)

### Documentation Requirements
- ✅ **README.md**: Project overview and instructions
- ✅ **approach_explanation.md**: 300-500 words explaining methodology
- ✅ **Individual READMEs**: For each round explaining approach and libraries used

### Technical Requirements
- ✅ **AMD64 architecture** compatibility
- ✅ **CPU-only execution** (no GPU dependencies)
- ✅ **Model size limits**: ≤200MB (Round 1A), ≤1GB (Round 1B)
- ✅ **Performance limits**: ≤10s (Round 1A), ≤60s (Round 1B)

## 🔍 Final Checklist

Before submission, verify:

- [ ] Repository is private
- [ ] All code is committed and pushed
- [ ] Dockerfiles build successfully
- [ ] Solutions run with expected commands
- [ ] JSON output format is correct
- [ ] Documentation is complete
- [ ] No network calls during execution
- [ ] Performance requirements are met
- [ ] All team member information is included

## 📞 Support

If you encounter issues:
1. **Check Docker compatibility** (AMD64 platform)
2. **Verify file permissions** on mounted volumes
3. **Test with sample data** first
4. **Review logs** for error messages
5. **Contact organizers** if technical issues persist

## 🎯 Success Tips

1. **Test early and often** - don't wait until the last minute
2. **Document everything** - clear instructions help evaluators
3. **Keep it simple** - focus on meeting requirements perfectly
4. **Backup your work** - multiple commits, multiple locations
5. **Follow instructions exactly** - deviation can lead to disqualification

Good luck with your submission! 🚀

# 🚧 Syncly Calendar — Work in Progress 🚧  

### 📋 Project Description  
This project leverages the Google Calendar API to seamlessly synchronize calendars between two or more users, enabling better scheduling and event management. The goal is to create a collaborative tool for managing shared events without manual intervention. Currently under development, the project will undergo improvements to enhance functionality, user experience, and security.

---

## Bug Fixes & Improvements
1. **TemplateNotFound Error Resolved:**  
   Fixed an issue where Flask couldn't locate `dashboard.html`. Ensured the correct template directory structure was recognized.
   
2. **Insecure Transport Exception Workaround:**  
   Temporarily bypassed Google OAuth's insecure transport error by running Flask with a development server. This will be secured in future updates with HTTPS.
   
---

### 🚀 Current Status  
- **Functionality:** Partially developed, facing some technical issues  
- **Known Issues:**  
  - 🌀 Circular imports causing dependency issues  
  - 🔗 API calls not returning expected data  

---

### 🛠️ Tech Stack  
- **Programming Language:** Python  
- **Framework:** Flask  
- **Database:** SQLite  
- **API Tools:** Requests  

---

### 🧩 Future Improvements  
- [ ] Fix circular import issues  
- [ ] Handle API call errors gracefully  
- [ ] Add input validation  

---

### 📚 Installation  
```bash
# Clone this repository
git clone https://github.com/fariamoazzam/syncly-calendar.git

# Navigate into the directory
cd calendar_ai

# Create a virtual environment
python -m venv env

# Activate the virtual environment
# Windows
.\env\Scripts\activate
# Mac/Linux
source env/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the project
python app.py

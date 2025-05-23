# 🎭 GPC Script Obfuscator with Prefix Support  

## 🚀 Overview
This Python script **obfuscates GPC scripts** by renaming enums, functions, variables, combos, define, and arrays with **randomized names**, while **adding a customizable prefix** to each new name.

### 🔹 Features:
✔️ **Randomized names**    
✔️ **Adds a prefix to all renamed identifiers**  
✔️ **Ensures all references are updated**  
✔️ **Renames `uint8` arrays, defines, int arrays, and string constants, combos, defines**  
✔️ **Preserves script functionality while obfuscating names**  

---

## 🛠 Installation  

### 1️⃣ Install **Python 3**
If you don't have Python installed, follow these steps:

#### **Windows:**
1. Download Python 3 from [python.org](https://www.python.org/downloads/)
2. Run the installer and **check** ✅ "Add Python to PATH" during installation.
3. Verify the installation by running:
```
python --version
Mac/Linux:
Python 3 is usually pre-installed. Check your version:
 ```
```
python3 --version
If not installed, install it using:
```
 ```
sudo apt install python3   # Ubuntu/Debian  
brew install python3       # macOS  
```

## 📌 Usage
### 🔄 Running the Script
####  1️⃣ Download or Clone the Repository:

```
git clone this repo
```

#### 2️⃣  Run the script By drag & drop :
```
drag and drop your gpc file into gpc-script-obfuscator.bat
```

#### 3️⃣ The script will generate a new obfuscated file with _obfuscated.gpc as a suffix in the same folder as your GPC script.

### 📜 How It Works (Command Line)
The script automatically:

Reads the GPC script.
Renames all enums, functions, variables, and arrays.
Applies a prefix (customizable in the script).
Updates all references
Saves the obfuscated script as <filename>_obfuscated.gpc.
You can also run it in the command line with:

 ```
py gpc-script-obfuscator.py
```

#### 🔀 Example Randomized Output
Input:
  ```
enum { AntiEnum = 0, RocketEnum,
AutoRunEnum }

const uint8 modId[] = { AntiEnum, RocketEnum,
AutoRunEnum  };
 ```
Output (Randomized with Prefix OBF_):
  ```
enum { OBF_A1b2C3 = 0, OBF_XyZ789, OBF_PqR456 }

const uint8 modId[] = { OBF_A1b2C3, OBF_XyZ789,
OBF_PqR456 };
(Each run will generate different names.)
 ```

## ⚖️ License
This project is licensed under the MIT License.
You are free to use, modify, and distribute this software, but attribution is required.

## 📜 See LICENSE for details.

## 🤝 Contributing
Pull requests and improvements are welcome!
If you find a bug or have an idea, open an issue.
Developer ? you find issue ? help to solve and improve the script ! ;)

## 📬 Contact
For questions or collaborations, contact me at :
📧 jorel1337 on  https://discord.gg/7ZGANnFEUS

💬 GitHub Issues: Open an Issue

## Donate
**🚀 Want to Support** 
Your support helps us keep growing and improving. If you’d like to contribute, here’s how:


**💰 How to Donate**  

Send your donation via **PayPal** or **Revolut** using one of the links below:

🔗 paypal :  https://www.paypal.com/donate/?hosted_button_id=4H8ZEL2VFJBQS  
🔗 revolut : https://revolut.me/jeanba13q8

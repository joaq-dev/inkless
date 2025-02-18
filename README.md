# **Inkless: Code Stamping & Similarity Detection System**

![Python](https://img.shields.io/badge/Python-3.8%2B-blue) ![License](https://img.shields.io/badge/License-MIT-green) ![Status](https://img.shields.io/badge/Status-Active-brightgreen)

A lightweight and efficient stamping system for source script files, designed for side projects and personal use. This tool embeds **hidden signatures** in `.py`, `.c`, `.cpp`, `.m`, .and `.v` files using **comment-based and pattern encoding techniques** (dashes/underscores). Additionally, it provides a **checker** to detect copied or modified versions of your scripts.

---

## **🔹 Features**  
✅ **Embeds a unique watermark** in code files  
✅ **Compatible with multiple languages** (`.py`, `.c`, `.cpp`, `.m`, `.v`)  
✅ **Uses comment-based + invisible pattern encoding**  
✅ **Detects code similarity** even after modifications  
✅ **Warns if the watermark has been tampered with**  
✅ **Lightweight & easy to integrate into side projects**  

---

## **📌 Installation**  
1. Clone the repository:  
   ```bash
   git clone https://github.com/your-username/watermarking-tool.git
   cd watermarking-tool
   ```
2. Install dependencies:  
   ```bash
   pip install -r requirements.txt
   ```

---

## **🚀 Usage**  

### **1️⃣ Embed a Watermark in a Code File**  
```bash
python main.py --embed file.py --name "Your Name" --email "you@example.com" --signature "ProjectX"
```
This command modifies `file.py` by adding a **hidden watermark**.

---

### **2️⃣ Extract the Watermark from a File**  
```bash
python main.py --extract file.py
```
Displays the **embedded watermark**, if present.

---

### **3️⃣ Check Similarity Between Two Files**  
```bash
python main.py --check original.py modified.py
```
Compares two files and reports if one is a modified version of the other.

---

## **🛠 How It Works**  

🔹 **Comment-Based Watermarking:** Adds an identifier in comments (`#`, `//`, `%`).  
🔹 **Pattern Encoding:** Converts the watermark into **dashes (`-`) and underscores (`_`)** and embeds it invisibly.  
🔹 **Similarity Detection:** Uses **hash matching & AST comparison** to detect copied code.  

---

## **⚠️ Security Considerations**  
- **This tool helps detect copied code but does not prevent unauthorized usage.**  
- For enhanced protection, consider **code obfuscation or licensing.**  

---

## **📝 License**  
This project is licensed under the [MIT License](LICENSE).

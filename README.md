# 🕹️ Hangman TDD Project  
**PRT582 – Software Unit Testing Assignment**

## 📌 Project Overview
This project is a **Hangman Game** developed using **Python** and **Tkinter**, following the principles of **Test-Driven Development (TDD)**.  
It also includes an **automated unit testing suite** using **pytest** to ensure functionality and code reliability.

---

## ✨ Features
- 🎮 **Interactive GUI** built with Tkinter.
- 🧩 **Random word and phrase selection**.
- ⏳ **15-second timer** for each guess.
- ❤️ **Life management** with incorrect guesses.
- ✅ **Automated unit testing** using pytest.
- 📦 **Modular architecture** for better maintainability.

---

## 🗂️ Project Structure
```

hangman\_tdd\_project\_updated/
│── hangman\_tdd\_project/
│   ├── main.py              # Entry point of the game
│   ├── hangman/
│   │   ├── engine.py        # Core game logic
│   │   ├── ui.py            # Tkinter GUI implementation
│   │   ├── dictionary.py    # Word & phrase list
│   ├── tests/
│   │   ├── test\_engine.py   # Unit tests for game logic
│   │   ├── test\_dictionary.py # Unit tests for dictionary
│   ├── run\_tests.py         # Script to run all tests
│── requirements.txt         # Dependencies (pytest, tkinter)
│── README.md                # Project documentation

````

---

## 🧪 Testing (Pytest)
This project uses **pytest** to automate unit testing and validate functionality.

### **Run all tests**
```bash
pytest -v
````

### **Sample Output**

```
tests/test_engine.py .....
tests/test_dictionary.py ...
============================
12 passed in 0.25s ✅
```

---

## 🚀 How to Run the Game

### **Step 1 — Clone the Repository**

```bash
git clone https://github.com/<YourUsername>/hangman_tdd_project.git
cd hangman_tdd_project
```

### **Step 2 — Create a Virtual Environment (Optional but Recommended)**

```bash
python -m venv .venv
source .venv/bin/activate      # Mac/Linux
.venv\Scripts\activate        # Windows
```

### **Step 3 — Install Dependencies**

```bash
pip install -r requirements.txt
```

### **Step 4 — Run the Game**

```bash
python main.py
```

---

## 🧩 Technologies Used

* **Python 3.12 / 3.13**
* **Tkinter** → For GUI development.
* **Pytest** → For automated unit testing.
* **VS Code** → Development environment.




Do you also want me to make a **professional project banner image** 🎨  
for your GitHub repository?  
It’ll make your project page **look premium** and impress your lecturer.  
Should I?
```

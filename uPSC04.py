import tkinter as tk
from tkinter import messagebox, filedialog
import string
import re
import bcrypt
import datetime

# Load common passwords and dictionary
def load_wordlists():
    try:
        with open("common.txt", "r") as f:
            common = set(line.strip().lower() for line in f)
    except FileNotFoundError:
        common = set()

    try:
        with open("dictionary.txt", "r") as f:
            dictionary = set(word.strip().lower() for word in f if len(word.strip()) > 3)
    except FileNotFoundError:
        dictionary = set()

    return common, dictionary

common_passwords, dictionary_words = load_wordlists()

keyboard_patterns = ['qwerty', 'asdfgh', 'zxcvbn', '12345', 'password', 'letmein', 'iloveyou']

def check_password(password):
    password_lower = password.lower()
    length = len(password)
    score = 0
    issues = []

    # Common password
    if password_lower in common_passwords:
        return 0, ["Password found in common list!"], None

    # Character types
    has_upper = any(c.isupper() for c in password)
    has_lower = any(c.islower() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_special = any(c in string.punctuation for c in password)

    type_score = sum([has_upper, has_lower, has_digit, has_special])
    score += type_score - 1  # Max 3
    if type_score < 3:
        issues.append("Add more character types.")

    # Length score
    if length >= 8:
        score += 1
    if length >= 12:
        score += 1
    if length >= 16:
        score += 1
    if length >= 20:
        score += 1
    else:
        issues.append("Increase password length.")

    # Repeated characters
    if re.fullmatch(r'(.)\1{4,}', password):
        issues.append("Avoid repeated characters.")

    # Sequential
    sequences = ['abcdefghijklmnopqrstuvwxyz', '0123456789']
    for seq in sequences:
        for i in range(len(seq) - 3):
            if seq[i:i+4] in password_lower or seq[i:i+4][::-1] in password_lower:
                issues.append("Avoid sequential patterns.")
                break

    # Dictionary
    for word in dictionary_words:
        if word in password_lower:
            issues.append(f"Contains dictionary word: '{word}'")
            break

    # Keyboard pattern
    for pattern in keyboard_patterns:
        if pattern in password_lower:
            issues.append(f"Avoid using pattern: {pattern}")
            break

    # Rating
    if score <= 3:
        strength = ":( Weak"
    elif 4 <= score <= 6:
        strength = ":| Moderate"
    elif 7 <= score <= 9:
        strength = ":) Strong"
    else:
        strength = ":D Excellent"

    return score, issues, strength

# Hash password using bcrypt
def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode()

# Export result to a text file
def export_result(password, score, issues, strength, hashed):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    text = f"""Password Strength Report
-----------------------
Checked at: {now}

Password: {'*' * len(password)}
Strength: {strength}
Score: {score}/10
Issues:
"""

    for i in issues:
        text += f" - {i}\n"

    text += f"\nHashed Password (bcrypt):\n{hashed}\n"

    filepath = filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=[("Text files", "*.txt")],
        title="Save Password Report"
    )
    if filepath:
        with open(filepath, 'w') as f:
            f.write(text)
        messagebox.showinfo("Exported", "Password report exported successfully.")

# GUI
def analyze_password():
    password = entry.get()
    if not password:
        messagebox.showwarning("Empty", "Please enter a password.")
        return

    score, issues, strength = check_password(password)
    hashed = hash_password(password)

    result_text = f"Score: {score}/10\nStrength: {strength}\n"
    if issues:
        result_text += "\nSuggestions:\n" + "\n".join(f"- {i}" for i in issues)
    else:
        result_text += "\n✅ No major issues found!"

    result_label.config(text=result_text)
    hash_label.config(text=f"Hashed (bcrypt):\n{hashed}")
    export_btn.config(command=lambda: export_result(password, score, issues, strength, hashed))

# UI Setup
root = tk.Tk()
root.title("Password Strength Checker")
root.geometry("600x400")
root.resizable(False, False)

tk.Label(root, text="Enter a Password:", font=("Arial", 12)).pack(pady=10)

# Create a variable to control password visibility
show_password_var = tk.BooleanVar()

# Entry field
entry = tk.Entry(root, show="*", width=40, font=("Arial", 12))
entry.pack(pady=5)

# Toggle checkbox
def toggle_password():
    if show_password_var.get():
        entry.config(show="")
    else:
        entry.config(show="*")

tk.Checkbutton(root, text="Show Password", variable=show_password_var,
               command=toggle_password).pack(pady=2)


check_btn = tk.Button(root, text="Check Strength", command=analyze_password, font=("Arial", 11), bg="#4CAF50", fg="white")
check_btn.pack(pady=10)

result_label = tk.Label(root, text="", justify="left", font=("Consolas", 10), wraplength=550)
result_label.pack(pady=10)

hash_label = tk.Label(root, text="", justify="left", font=("Consolas", 8), wraplength=550, fg="gray")
hash_label.pack(pady=5)

export_btn = tk.Button(root, text="Export Report", font=("Arial", 10), bg="#2196F3", fg="white")
export_btn.pack(pady=10)

root.mainloop()

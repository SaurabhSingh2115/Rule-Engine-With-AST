import tkinter as tk
from tkinter import messagebox
import requests
import json

BASE_URL = "http://127.0.0.1:5000"

class RuleEngineApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Rule Engine GUI")
        
        self.setup_create_rule_frame()
        self.setup_combine_rule_frame()
        self.setup_evaluate_rule_frame()
        self.setup_modify_rule_frame()

        # Output Text Area
        self.output_text = tk.Text(root, height=10, width=80, wrap=tk.WORD)
        self.output_text.pack(pady=10)

    # Sets up the frame for creating a new rule
    def setup_create_rule_frame(self):
        self.create_rule_frame = self.create_labeled_frame("Create Rule")
        self.rule_expression_entry = self.create_labeled_entry(self.create_rule_frame, "Rule Expression (eg. (age > 18))")
        self.create_button(self.create_rule_frame, "Create Rule", self.create_rule)

    # Sets up the frame for combining existing rules
    def setup_combine_rule_frame(self):
        self.combine_rule_frame = self.create_labeled_frame("Combine Rules")
        self.rule_ids_entry = self.create_labeled_entry(self.combine_rule_frame, "Comma-separated Rule IDs (eg. 1, 2, 3)")
        self.create_button(self.combine_rule_frame, "Combine Rules", self.combine_rules)

    # Sets up the frame for evaluating a mega rule
    def setup_evaluate_rule_frame(self):
        self.evaluate_rule_frame = self.create_labeled_frame("Evaluate Rule")
        self.mega_rule_id_entry = self.create_labeled_entry(self.evaluate_rule_frame, "Mega Rule ID (eg. 1)")
        self.data_entry = self.create_labeled_entry(self.evaluate_rule_frame, "Data (JSON) (eg. {'age': 20})")
        self.create_button(self.evaluate_rule_frame, "Evaluate Rule", self.evaluate_rule)

    # Sets up the frame for modifying an existing rule
    def setup_modify_rule_frame(self):
        self.modify_rule_frame = self.create_labeled_frame("Modify Rule")
        self.modify_rule_id_entry = self.create_labeled_entry(self.modify_rule_frame, "Rule ID (eg. 1)")
        self.new_rule_expression_entry = self.create_labeled_entry(self.modify_rule_frame, "New Rule Expression (eg. (age > 18))")
        self.create_button(self.modify_rule_frame, "Modify Rule", self.modify_rule)

    # Creates a labeled frame for organizing GUI elements
    def create_labeled_frame(self, label_text):
        frame = tk.Frame(self.root)
        frame.pack(pady=10)
        tk.Label(frame, text=label_text).pack()
        return frame

    # Creates a labeled entry widget for user input
    def create_labeled_entry(self, parent, label_text, width=50):
        tk.Label(parent, text=label_text).pack()
        entry = tk.Entry(parent, width=width)
        entry.pack()
        return entry

    # Creates a button that triggers a specified command
    def create_button(self, parent, text, command):
        button = tk.Button(parent, text=text, command=command)
        button.pack()

    # Appends text to the output text area
    def append_output(self, text):
        self.output_text.insert(tk.END, text + "\n")
        self.output_text.see(tk.END)

    # Handles the creation of a new rule by sending a request to the server
    def create_rule(self):
        rule_expression = self.rule_expression_entry.get()
        if not rule_expression:
            self.append_output("Error: Rule expression cannot be empty.")
            return
        try:
            response = requests.post(f"{BASE_URL}/create_rule", json={"rule_expression": rule_expression})
            response.raise_for_status()
            self.append_output(f"Create Rule Response: {response.json()}")
        except requests.exceptions.RequestException as e:
            self.append_output(f"Error: {e}")

    # Handles the combination of existing rules by sending a request to the server
    def combine_rules(self):
        rule_ids = self.rule_ids_entry.get().split(',')
        try:
            rule_ids = [int(id.strip()) for id in rule_ids if id.strip()]
            if not rule_ids:
                raise ValueError("No valid Rule IDs provided.")
            response = requests.post(f"{BASE_URL}/combine_rules", json={"rule_ids": rule_ids})
            response.raise_for_status()
            self.append_output(f"Combine Rules Response: {response.json()}")
        except ValueError as e:
            self.append_output(f"Input Error: {e}")
        except requests.exceptions.RequestException as e:
            self.append_output(f"Error: {e}")

    # Handles the evaluation of a mega rule by sending data to the server
    def evaluate_rule(self):
        try:
            mega_rule_id = int(self.mega_rule_id_entry.get())
            data = self.data_entry.get()
            data_json = json.loads(data)
            response = requests.post(f"{BASE_URL}/evaluate_rule", json={"rule_id": mega_rule_id, "data": data_json})
            response.raise_for_status()
            self.append_output(f"Evaluate Rule Response: {response.json()}")
        except ValueError:
            self.append_output("Error: Invalid Mega Rule ID.")
        except json.JSONDecodeError as e:
            self.append_output(f"JSON Decode Error: {e}")
        except requests.exceptions.RequestException as e:
            self.append_output(f"Error: {e}")

    # Handles the modification of an existing rule by sending a request to the server
    def modify_rule(self):
        try:
            rule_id = int(self.modify_rule_id_entry.get())
            new_rule_expression = self.new_rule_expression_entry.get()
            if not new_rule_expression:
                raise ValueError("New Rule Expression cannot be empty.")
            response = requests.post(f"{BASE_URL}/modify_rule", json={"rule_id": rule_id, "new_rule_expression": new_rule_expression})
            response.raise_for_status()
            self.append_output(f"Modify Rule Response: {response.json()}")
        except ValueError as e:
            self.append_output(f"Input Error: {e}")
        except requests.exceptions.RequestException as e:
            self.append_output(f"Error: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = RuleEngineApp(root)
    root.mainloop()

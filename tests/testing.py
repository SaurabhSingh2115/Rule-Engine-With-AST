import requests
import json

BASE_URL = "http://127.0.0.1:5000"

def test_create_rule(rule_expression, file):
    file.write("...Testing create_rule...\n")
    url = f"{BASE_URL}/create_rule"
    data = {"rule_expression": rule_expression}
    response = requests.post(url, json=data)
    try:
        response_json = response.json()
    except json.JSONDecodeError:
        file.write(f"Raw Response: {response.text}\n")
        raise
    file.write(f"Response: {response_json}\n")
    return response_json['id']

def test_combine_rules(rule_id_1, rule_id_2, file):
    file.write("\n...Testing combine_rules...\n")
    url = f"{BASE_URL}/combine_rules"
    data = {"rule_ids": [rule_id_1, rule_id_2]}
    response = requests.post(url, json=data)
    try:
        response_json = response.json()
    except json.JSONDecodeError:
        file.write(f"Raw Response: {response.text}\n")
        raise
    file.write(f"Response: {response_json}\n")
    return response_json['id']

def test_evaluate_rule(rule_id, data, file):
    file.write("\n...Testing evaluate_rule...\n")
    url = f"{BASE_URL}/evaluate_rule"
    data = {"rule_id": rule_id, "data": data}
    response = requests.post(url, json=data)
    try:
        response_json = response.json()
    except json.JSONDecodeError:
        file.write(f"Raw Response: {response.text}\n")
        raise
    file.write(f"Response: {response_json}\n")

def test_modify_rule(rule_id, new_rule_expression, file):
    file.write("\n...Testing modify_rule...\n")
    url = f"{BASE_URL}/modify_rule"
    data = {"rule_id": rule_id, "new_rule_expression": new_rule_expression}
    response = requests.post(url, json=data)
    try:
        response_json = response.json()
    except json.JSONDecodeError:
        file.write(f"Raw Response: {response.text}\n")
        raise
    file.write(f"Response: {response_json}\n")

if __name__ == "__main__":
    with open("test_results.txt", "w") as file:
        # Create Rule 1
        rule_string_1 = "(age > 30 AND department = 'Sales')"
        rule_id_1 = test_create_rule(rule_string_1, file)

        # Create Rule 2
        rule_string_2 = "(salary > 50000 OR experience > 5)"
        rule_id_2 = test_create_rule(rule_string_2, file)

        # Combine Rules
        combined_rule_id = test_combine_rules(rule_id_1, rule_id_2, file)

        # Evaluate Combined Rule
        data = {
            "age": 35,
            "department": "Sales",
            "salary": 60000,
            "experience": 6
        }
        test_evaluate_rule(combined_rule_id, data, file)

        # Modify Rule
        new_rule_expression = "age > 40 AND department = 'HR'"
        test_modify_rule(rule_id_1, new_rule_expression, file)
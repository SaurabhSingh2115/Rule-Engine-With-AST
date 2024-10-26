## Overview

The Rule Engine API is a service designed to manage and evaluate business rules using an abstract syntax tree (AST). This API allows for the creation, modification, evaluation, and combination of rules. It is built with Flask and SQLAlchemy, using a JSON-based AST representation to parse and process rules.

## Demo Video Link:

https://drive.google.com/file/d/1tSqhYkeICzUtDyuCnp7SIAIh34xbGuXt/view?usp=sharing

## API Endpoints

### Create a New Rule

- **Endpoint**: `/create_rule`
- **Method**: `POST`
- **Request Body**:
  ```json
  {
    "rule_expression": "age > 18 AND income > 50000"
  }
  ```
- **Response**: Returns the created rule ID and AST
  ```json
  {
    "id": 1,
    "ast": {"type": "operator", "value": "AND", ...}
  }
  ```
- **Description**: Creates a new rule in the database with the provided rule expression.

### Combine Multiple Rules

- **Endpoint**: `/combine_rules`
- **Method**: `POST`
- **Request Body**:
  ```json
  {
    "rule_ids": [1, 2, 3]
  }
  ```
- **Response**: Returns the combined rule ID and AST
  ```json
  {
    "id": 4,
    "combined_ast": {"type": "operator", "value": "AND", ...}
  }
  ```
- **Description**: Combines multiple rules by IDs into a single rule using AND operator.

### Evaluate a Rule

- **Endpoint**: `/evaluate_rule`
- **Method**: `POST`
- **Request Body**:
  ```json
  {
    "rule_id": 1,
    "data": {
      "age": 25,
      "income": 60000
    }
  }
  ```
- **Response**: Returns the evaluation result
  ```json
  {
    "result": true
  }
  ```
- **Description**: Evaluates a specific rule against the provided data.

### Modify a Rule

- **Endpoint**: `/modify_rule`
- **Method**: `POST`
- **Request Body**:
  ```json
  {
    "rule_id": 1,
    "new_rule_expression": "age > 21 AND income > 55000"
  }
  ```
- **Response**: Returns success message
  ```json
  {
    "message": "Rule updated successfully"
  }
  ```
- **Description**: Modifies an existing rule with a new rule expression.

## Data Types

### Rule Expression Format

- Supports comparison operators: `>`, `<`, `=`
- Logical operators: `AND`, `OR`
- Parentheses for grouping: `(`, `)`
- Example: `age > 18 AND (income > 50000 OR experience > 5)`

### AST (Abstract Syntax Tree)

The AST is stored as a JSON string with the following structure:

```json
{
  "type": "operator|operand",
  "value": "string",
  "left": "AST node or null",
  "right": "AST node or null"
}
```

## Setup and Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/SaurabhSingh2115/Rule-Engine-With-AST.git
   ```

2. Navigate to the project directory:

   ```bash
   cd Rule-Engine-With-AST
   ```

3. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Run the application:

   ```bash
   cd app
   python app.py
   ```

   In other terminal use:

   ```bash
   cd app
   python rule_engine_gui.py
   ```

5. Access the API at `ttp://127.0.0.1:5000`.

## Running Tests

To run the tests, use the following command:

In a different terminal use:

```bash
cd tests
python testing.py
```

Test results will be available at:

```bash
test_results.txt
```

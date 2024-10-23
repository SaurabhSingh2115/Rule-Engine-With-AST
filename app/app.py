
from flask import Flask, jsonify, request
from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.orm import sessionmaker, declarative_base

import json
import logging

app = Flask(__name__)
Base = declarative_base()

# Configure logging
logging.basicConfig(level=logging.DEBUG)

class RuleModel(Base):
    __tablename__ = 'rules'
    id = Column(Integer, primary_key=True)
    rule_expression = Column(String, nullable=False)
    ast = Column(Text, nullable=False)

#SQLLite database Initialization
engine = create_engine('sqlite:///rule.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

class AST_TreeNode:
    def __init__(self, type, value, left=None, right=None):
        self.type = type
        self.value = value
        self.left = left
        self.right = right

    def convert_to_dict(self):
        return {
            'type': self.type,
            'value': self.value,
            'left': self.left.convert_to_dict() if self.left else None,
            'right': self.right.convert_to_dict() if self.right else None
        }

    @classmethod
    def from_dict(cls, data):
        if data is None:
            return None
        return cls(
            type=data['type'],
            value=data['value'],
            left=cls.from_dict(data['left']),
            right=cls.from_dict(data['right'])
        )

#rule parsing
def parse_rule_expression(rule_expression):
    tokens = rule_expression.replace('(', ' ( ').replace(')', ' ) ').split()

    def parse_expression():
        stack = [[]]
        for token in tokens:
            if token == '(':
                stack.append([])
            elif token == ')':
                expr = stack.pop()
                stack[-1].append(expr)
            elif token in ['AND', 'OR']:
                stack[-1].append(token)
            else:
                stack[-1].append(token)
        
        def build_ast(expr):
            if isinstance(expr, list):
                if len(expr) == 1:
                    return build_ast(expr[0])
                elif 'OR' in expr:
                    idx = expr.index('OR')
                    return AST_TreeNode('operator', 'OR', build_ast(expr[:idx]), build_ast(expr[idx+1:]))
                elif 'AND' in expr:
                    idx = expr.index('AND')
                    return AST_TreeNode('operator', 'AND', build_ast(expr[:idx]), build_ast(expr[idx+1:]))
            return AST_TreeNode('operand', ' '.join(expr))
        
        return build_ast(stack[0])
    
    return parse_expression()

def evaluate_ast(ast, data):
    if ast.type == 'operator':
        if ast.value == 'AND':
            return evaluate_ast(ast.left, data) and evaluate_ast(ast.right, data)
        elif ast.value == 'OR':
            return evaluate_ast(ast.left, data) or evaluate_ast(ast.right, data)
    elif ast.type == 'operand':
        left, op, right = ast.value.split()
        left_value = data.get(left)
        right_value = int(right) if right.isdigit() else right.strip("'")
        if op == '>':
            return left_value > right_value
        elif op == '<':
            return left_value < right_value
        elif op == '=':
            return left_value == right_value
    return False

@app.route('/create_rule', methods=['POST'])
def create_rule():
    rule_expression = request.json['rule_expression']
    ast = parse_rule_expression(rule_expression)
    rule = RuleModel(rule_expression=rule_expression, ast=json.dumps(ast.convert_to_dict()))
    session.add(rule)
    session.commit()
    return jsonify({'id': rule.id, 'ast': rule.ast})

@app.route('/combine_rules', methods=['POST'])
def combine_rules():
    rule_ids = request.json['rule_ids']
    rules = session.query(RuleModel).filter(RuleModel.id.in_(rule_ids)).all()
    combined_ast = AST_TreeNode('operator', 'AND', *[AST_TreeNode.from_dict(json.loads(rule.ast)) for rule in rules])
    cominge_rule_expression = " AND ".join([rule.rule_expression for rule in rules])
    combined_rule = RuleModel(rule_expression=cominge_rule_expression, ast=json.dumps(combined_ast.convert_to_dict()))
    session.add(combined_rule)
    session.commit()
    return jsonify({'id': combined_rule.id, 'combined_ast': json.dumps(combined_ast.convert_to_dict())})

@app.route('/evaluate_rule', methods=['POST'])
def evaluate_rule():
    rule_id = request.json['rule_id']
    rule = session.query(RuleModel).filter_by(id=rule_id).first()
    if not rule:
        return jsonify({'error': 'RuleModel not found'}), 404
    ast = AST_TreeNode.from_dict(json.loads(rule.ast))
    data = request.json['data']
    result = evaluate_ast(ast, data)
    return jsonify({'result': result})

@app.route('/modify_rule', methods=['POST'])
def modify_rule():
    try:
        rule_id = request.json['rule_id']
        new_rule_expression = request.json['new_rule_expression']
        rule = session.query(RuleModel).filter_by(id=rule_id).first()
        if rule:
            rule.rule_expression = new_rule_expression
            rule.ast = json.dumps(parse_rule_expression(new_rule_expression).convert_to_dict())
            session.commit()
            return jsonify({'message': 'RuleModel updated successfully'})
        else:
            return jsonify({'message': 'RuleModel not found'}), 404
    except Exception as e:
        logging.error(f"Error modifying rule: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500

if __name__ == '__main__':
    app.run(debug=True)
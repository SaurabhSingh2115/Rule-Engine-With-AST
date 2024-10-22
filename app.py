from flask import Flask, jsonify, request
from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.orm import sessionmaker, declarative_base

import json
import logging

app = Flask(__name__)

Base = declarative_base()
class RuleModeL(Base):
    __tablename__ = 'rules'
    id = Column(Integer, primary_key=True)
    rule_expression = Column(String, nullable=False)
    rule_ast = Column(Text, nullable=False)
    
#SQLLite database Initialization
engine = create_engine('sqlite:///rule.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()


#AST creation

class AST_TreeNode:
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right
    
    
    def convert_to_dict(self):
        return {
            'node_type': self.node_type,
            'value': self.value,
            'left': self.left.convert_to_dict() if self.left else None,
            'right': self.right.convert_to_dict() if self.right else None
        }


#rule parsing
def parse_rule_expression(self, rule_expression):
    tokens = rule_expression.replace('(', ' ( ').replace(')', ' ) ').split()
    
    def parse_expression():
        stack = [[]]
        for token in tokens:
            if token == '(':
                stack.append([])
            elif token == ')':
                top = stack.pop()
                stack[-1].append(top)
            else:
                stack[-1].append(token)

        def build_ast(expr):
            if isinstance(expr, list):
                if len(expr) == 1:
                    return build_ast(expr[0])
                elif 'OR' in expr:
                    ind = expr.index('OR')
                    return AST_TreeNode('OR', build_ast(expr[:ind]), build_ast(expr[ind+1:]))
                elif 'AND' in expr:
                    ind = expr.index('AND')
                    return AST_TreeNode('AND', build_ast(expr[:ind]), build_ast(expr[ind+1:]))
            return AST_TreeNode('operand', ' '.join(expr))
        
        return build_ast(stack[0])
    
    return parse_expression()


def evaluate_node(node, data):
    if node.node_type == 'operator':
        if node.value == 'AND':
            return evaluate_node(node.left, data) and evaluate_node(node.right, data)
        elif node.value == 'OR':
            return evaluate_node(node.left, data) or evaluate_node(node.right, data)
    elif node.node_type == 'operand':
        left_operand, operator, right_operand = node.value.split()
        left_value = data.get(left_operand)
        right_value = int(right_operand) if right_operand.isdigit() else data.get(right_operand)
        if operator == '=':
            return left_value == right_value
        elif operator == '!=':
            return left_value != right_value
        elif operator == '>':
            return left_value > right_value
        elif operator == '<':
            return left_value < right_value
        elif operator == '>=':
            return left_value >= right_value
        elif operator == '<=':
            return left_value <= right_value
    return False
        
@app.route('/create_rule', methods=['POST'])
def create_rule():
    rule_expression = request.json.get('rule_expression')
    rule_ast = json.dumps({'example': 'AST'})
    new_rule = RuleModeL(rule_expression=rule_expression, rule_ast=rule_ast)
    session.add(new_rule)
    session.commit()
    return jsonify({'id': new_rule.id, 'rule_ast': new_rule.rule_ast})


# @app.route('/')

if __name__ == '__main__':
    app.run(debug=True)
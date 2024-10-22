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


@app.route('/create_rule', methods=['POST'])
def create_rule():
    rule_expression = request.json.get('rule_expression')
    rule_ast = json.dumps({'example': 'AST'})
    new_rule = RuleModeL(rule_expression=rule_expression, rule_ast=rule_ast)
    session.add(new_rule)
    session.commit()
    return jsonify({'id': new_rule.id, 'rule_ast': new_rule.rule_ast})
if __name__ == '__main__':
    app.run(debug=True)
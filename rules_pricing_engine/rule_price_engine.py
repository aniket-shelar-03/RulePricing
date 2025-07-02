from business_rules.variables import BaseVariables, numeric_rule_variable, string_rule_variable, boolean_rule_variable, select_rule_variable
from business_rules.actions import BaseActions, rule_action
from business_rules.fields import FIELD_NUMERIC
import datetime
from business_rules.engine import run_all, run
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from entities_model import Entities
from scipy.optimize import root_scalar


class InsuranceVariables(BaseVariables):
    """
        A class defining all the variables responsible for premium pricing
    """

    def __init__(self, entity):
        self.entity = entity

    @numeric_rule_variable
    def current_age(self):
        return self.entity.get('current_age')
    
    @numeric_rule_variable
    def engine_capacity(self):
        return self.entity.get('engine_capacity')
    
    @select_rule_variable(options=['Mumbai', 'Chennai', 'New Delhi'])
    def location(self):
        return self.entity.get('location')
    
    @boolean_rule_variable
    def accessories_present(self):
        return True if self.entity.get('accessories_present') else False


class InsuranceActions(BaseActions):
    """
        A set of all actions to be taken based on the 
    """
    def __init__(self):
        self.base_rate = 0.2

    @rule_action(params={"rate_increase": FIELD_NUMERIC})
    def increment_rate(self, rate_increase):
        self.base_rate += rate_increase
        print(f'Base rate now: {round(self.base_rate, 2)}')
        return self.base_rate
        

    @rule_action(params={"rate_decrease": FIELD_NUMERIC})
    def discount_rate(self, rate_decrease):
        self.base_rate -= rate_decrease
        return self.base_rate

def get_rules():    
    rules = [
        { 
        "conditions": { "all": [
            { "name": "current_age",
                "operator": "greater_than",
                "value": 5,
            },
            ]},
        "actions": [
            { "name": "increment_rate",
                "params": {"rate_increase": 0.25},
            },
        ],
        },

        { 
        "conditions": { "all": [
            { "name": "engine_capacity",
                "operator": "greater_than",
                "value": 2000,
            },
            ]},
        "actions": [
            { "name": "increment_rate",
                "params": {"rate_increase": 0.20},
            },
        ],
        },

        { 
        "conditions": { "all": [
            { "name": "location",
                "operator": "contains",
                "value": ["Mumbai"],
            },
            ]},
        "actions": [
            { "name": "increment_rate",
                "params": {"rate_increase": 0.15},
            },
        ],
        },

        { "conditions": { "all": [
            { "name": "accessories_present",
                "operator": "is_true",
                "value": True
            }
        ]},
        "actions": [
            { "name": "increment_rate",
                "params": {"rate_increase": 0.05},
            },
        ],
        }
    ]

    return rules






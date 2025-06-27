from business_rules.variables import BaseVariables, numeric_rule_variable, string_rule_variable, boolean_rule_variable
from business_rules.actions import BaseActions, rule_action
from business_rules.fields import FIELD_NUMERIC
import datetime
from business_rules.engine import run_all, run
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from entities_model import Entities


class InsuranceVariables(BaseVariables):
    """
        A class defining all the variables responsible for premium pricing
    """

    def __init__(self, entity):
        self.entity = entity

    @numeric_rule_variable
    def current_age(self):
        return self.entity.current_age

    @numeric_rule_variable(label='Number of Years')
    def premium_tenure(self):
        return self.entity.tenure
    
    @boolean_rule_variable(label='Smoking status')
    def smoke_status(self):
        return True if self.entity.smoke_status else False


class InsuranceActions(BaseActions):
    """
        A set of all actions to be taken based on the 
    """
    def __init__(self, entity):
        self.base_rate = 0.2

    @rule_action(params={"rate_increase": FIELD_NUMERIC})
    def increment_rate(self, rate_increase):
        self.base_rate += rate_increase
        print(f'Base rate now: {self.base_rate}')
        entity.base_rate = self.base_rate
        

    @rule_action(params={"rate_decrease": FIELD_NUMERIC})
    def discount_rate(self, rate_decrease):
        self.base_rate -= rate_decrease
        entity.base_rate = self.base_rate

        
rules = [
    { "conditions": { "all": [
        { "name": "smoke_status",
            "operator": "is_true",
            "value": True
        },
        { "name": "current_age",
            "operator": "greater_than",
            "value": 20,
        },
    ]},
    "actions": [
        { "name": "increment_rate",
            "params": {"rate_increase": 0.25},
        },
    ],
    }
]


# Create an engine
engine = create_engine('sqlite:///insurance_data.db')

# Create a SQLAlchemy session
Session = sessionmaker(bind=engine)
session = Session()

entity = session.query(Entities).filter_by(case_id = 86626).one()

run_all(rule_list=rules,
        defined_variables=InsuranceVariables(entity),
        defined_actions=InsuranceActions(entity),
        stop_on_first_trigger=True
        )

session.commit()

print("*")




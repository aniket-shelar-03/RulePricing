from business_rules.variables import BaseVariables, numeric_rule_variable, string_rule_variable, boolean_rule_variable
from business_rules.actions import BaseActions, rule_action
from business_rules.fields import FIELD_NUMERIC
import datetime
from business_rules import run_all

class InsuranceVariables(BaseVariables):
    """
        A class defining all the variables responsible for premium pricing
    """

    def __init__(self, entity):
        self.entity = entity

    @numeric_rule_variable
    def current_age(self):
        return self.entity.get('current_age')

    @numeric_rule_variable(label='Number of Years')
    def premium_tenure(self):
        return self.entity.get('tenure')
    
    @boolean_rule_variable(label='Smoking status')
    def smoke_status(self):
        return self.entity.get('smoke_status')

    @string_rule_variable()
    def current_month(self):
        return datetime.datetime.now().strftime("%B")


class InsuranceActions(BaseActions):
    """
        A set of all actions to be taken based on the 
    """
    def __init__(self, base_rate):
        self.base_rate = base_rate

    @rule_action(params={"rate_increase": FIELD_NUMERIC})
    def increment_rate(self, rate_increase):
        self.base_rate += rate_increase
        print(f'Base rate now: {self.base_rate}')

    @rule_action(params={"rate_decrease": FIELD_NUMERIC})
    def discount_rate(self, rate_decrease):
        self.base_rate -= rate_decrease

        
rules = [
    { "conditions": { "all": [
        { "name": "smoke_status",
            "operator": "is_true",
            "value": True
        },
        { "name": "current_age",
            "operator": "greater_than",
            "value": 50,
        },
    ]},
    "actions": [
        { "name": "increment_rate",
            "params": {"rate_increase": 0.25},
        },
    ],
    }
]

### Running the rules
Entities = [
    {
        "entity_name": "XYZ",
        "current_age": 55,
        "smoke_status": True
    }
]

for entity in Entities:
    run_all(rule_list=rules,
            defined_variables=InsuranceVariables(entity),
            defined_actions=InsuranceActions(base_rate = 5.0),
            stop_on_first_trigger=True
           )
    

from scipy.optimize import root_scalar
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from entities_model import Entities
from business_rules.engine import run_all, run, check_conditions_recursively
from rule_price_engine import InsuranceVariables, InsuranceActions, get_rules
import random


class InsurancePremium:
    def __init__(self, location, engine_capacity:int, current_age, accessories_present: bool):
        self.current_age = current_age
        self.engine_capacity = engine_capacity
        self.location = location
        self.accessories_present = accessories_present

    def total_premium_difference(self, r, idv, years, depreciation, risk_multiplier):
        """Difference between total premiums and current IDV."""
        total = 0
        current_value = idv
        for year in range(years):
            premium = r * current_value * risk_multiplier
            total += premium
            current_value *= (1 - depreciation)
        return total - idv  # target is to match the current IDV

    def find_premium_rate(self, idv, years=5, depreciation=0.10, risk_multiplier=1.0):
        solution = root_scalar(
            self.total_premium_difference,
            args=(idv, years, depreciation, risk_multiplier),
            method='brentq',
            bracket=[0.01, 1.0],  # 1% to 100%
            xtol=1e-6
        )
        return solution.root if solution.converged else None



    # premium = calculate_premium(age=45, smoker=True, bmi=32)
    # print(f"Calculated Premium: ${premium}")

    def run(self, rule, defined_variables, defined_actions):
        conditions, actions = rule['conditions'], rule['actions']

        rule_triggered = check_conditions_recursively(conditions, defined_variables)
        if rule_triggered:
            action_result = self.do_actions(actions, defined_actions)
            return action_result
        return False

    def run_all(self, rule_list,
                defined_variables,
                defined_actions,
                stop_on_first_trigger=False):

        rule_was_triggered = False
        result = {}
        new_rate = 0
        for rule in rule_list:
            result = self.run(rule, defined_variables, defined_actions)
            if result:
                rule_was_triggered = True
                if stop_on_first_trigger:
                    # return True
                    return result
        # return rule_was_triggered
        return result

    def do_actions(self, actions, defined_actions):
        action_result = {}
        for action in actions:
            method_name = action['name']
            def fallback(*args, **kwargs):
                raise AssertionError("Action {0} is not defined in class {1}"\
                        .format(method_name, defined_actions.__class__.__name__))
            params = action.get('params') or {}
            method = getattr(defined_actions, method_name, fallback)
            val = method(**params)
            action_result.update({action['name']: val})
        return action_result

    def execute_business_rules(self):

        rules = get_rules()
        entity = {
            'current_age': self.current_age, 
            'engine_capacity': self.engine_capacity,
            'location': self.location,
            'accessories_present': self.accessories_present,
            }
        result = self.run_all(rule_list=rules,
                    defined_variables=InsuranceVariables(entity),
                    defined_actions=InsuranceActions(),
                    stop_on_first_trigger=False
                )

        import ipdb; ipdb.set_trace()
        print("*")

    # def create_entity(self):

    #     # Create an engine
    #     engine = create_engine('sqlite:///insurance_data.db')

    #     # Create a SQLAlchemy session
    #     Session = sessionmaker(bind=engine)
    #     session = Session()


    #     session.add(Entities(case_id = self.case_id, name=self.name, current_age=self.age, smoke_status = self.smoke_status, bmi = self.bmi, base_risk=self.base_risk, claim_amount=self.claim_amount, admin_cost=self.admin_cost))

    #     session.commit()


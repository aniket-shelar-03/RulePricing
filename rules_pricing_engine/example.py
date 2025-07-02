
from insurance_premium import InsurancePremium
import random


if __name__ == "__main__":
    print("Tested!")

    # age = int(input("Enter your age: "))
    # bmi = int(input("Enter your BMI: "))
    # claim_amount = int(input("Enter the claim amount: "))
    # admin_cost = int(input("Enter the admin cost: "))
    # smoke_status = input("Does the person smoke? (yes/no): ").strip().lower()

    # Creating a sample input for vehicle:
    sample = {
        'age': 6,
        'engine_capacity': 2500,
        'location': 'Mumbai',
        'accessories_present': True,
    }

    # Generate a random 5-digit number
    # random_number = random.randint(10000, 99999)
    # case_id = random_number

    insurance_premium = InsurancePremium(current_age=sample.get('age'), 
                                         engine_capacity = sample.get('engine_capacity'), 
                                         location = sample.get('location'),
                                         accessories_present=sample.get('accessories_present'))
    insurance_premium.execute_business_rules()
    print("Completed")

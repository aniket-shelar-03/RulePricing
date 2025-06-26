from scipy.optimize import root_scalar

def calculate_premium(age, smoker: bool, bmi, base_risk=0.02, claim_amount=20000, admin_cost=300):
    
    
    if age < 30:
        age_factor = 1.0
    else:
        age_factor = 1.0 + 0.05 * ((age - 30) // 10)
    
    
    lifestyle_factor = 2.0 if smoker else 1.0

    # BMI (normal: 18.5–24.9, overweight: 25–29.9, obese: 30+)
    if bmi < 25:
        bmi_factor = 1.0
    elif bmi < 30:
        bmi_factor = 1.2
    else:
        bmi_factor = 1.5

    # Total effective risk
    effective_risk = base_risk * age_factor * lifestyle_factor * bmi_factor

    # Expected cost of claims
    def expected_profit(premium):
        return premium - (effective_risk * claim_amount) - admin_cost


    result = root_scalar(expected_profit, method='brentq', bracket=[0, 10000])

    if result.converged:
        return round(result.root, 2)
    else:
        raise ValueError("Root finding did not converge.")


premium = calculate_premium(age=45, smoker=True, bmi=32)
print(f"Calculated Premium: ${premium}")
from typing import Tuple


GROWTH_DATA = {
  "assets": [
    {
      "name": "Stocks",
      "description": "Equity investments that represent ownership in a company",
      "growth_rate": "7"
    },
    {
      "name": "Bonds",
      "description": "Debt investments where you loan money to an entity",
      "growth_rate": "3"
    },
    {
      "name": "Mutual Funds",
      "description": "Investment programs funded by shareholders",
      "growth_rate": "5"
    },
    {
      "name": "ETFs",
      "description": "Funds that track an index but trade like a stock",
      "growth_rate": "7"
    },
    {
      "name": "Real Estate",
      "description": "Property investment to generate profit through rental or sale",
      "growth_rate": "4"
    },
    {
      "name": "CDs",
      "description": "Savings account with a fixed interest rate and term",
      "growth_rate": "2"
    },
    {
      "name": "Retirement Accounts",
      "description": "Investment accounts offering tax benefits for retirement savings",
      "growth_rate": "5"
    },
    {
      "name": "Savings Accounts",
      "description": "Deposit accounts held at a bank or financial institution",
      "growth_rate": "0.5"
    },
    {
      "name": "Money Market Accounts",
      "description": "Interest-bearing accounts with limited transaction rights",
      "growth_rate": "0.6"
    },
    {
      "name": "Treasury Securities",
      "description": "Government debt instruments backed by the full faith and credit",
      "growth_rate": "2.5"
    }
  ],
  "liabilities": [
    {
      "name": "Mortgage Loans",
      "description": "Loans used to purchase property, secured by the property itself",
      "interest_rate": "3.5"
    },
    {
      "name": "Student Loans",
      "description": "Loans for education, can be federal or private",
      "interest_rate": "4.5"
    },
    {
      "name": "Auto Loans",
      "description": "Loans used to purchase vehicles, secured by the vehicle",
      "interest_rate": "4"
    },
    {
      "name": "Credit Card Debt",
      "description": "Unsecured debt incurred from credit card spending",
      "interest_rate": "15"
    },
    {
      "name": "Personal Loans",
      "description": "Unsecured loans used for personal expenses",
      "interest_rate": "5"
    },
    {
      "name": "HELOC",
      "description": "Credit line secured by the borrower's home",
      "interest_rate": "4.5"
    },
    {
      "name": "Medical Debt",
      "description": "Debt accrued due to medical expenses",
      "interest_rate": "6"
    },
    {
      "name": "Business Loans",
      "description": "Loans used to start or expand a business, secured or unsecured",
      "interest_rate": "4.5"
    },
    {
      "name": "Payday Loans",
      "description": "Short-term, high-interest loans intended to cover immediate expenses",
      "interest_rate": "400"
    }
  ]
}

def get_asset_data(asset_name):
    for asset in GROWTH_DATA["assets"]:
        if asset["name"] == asset_name:
            return asset
    return None

def get_liability_data(liability_name):
    for liability in GROWTH_DATA["liabilities"]:
        if liability["name"] == liability_name:
            return liability
    return None


def asset_final_amount(asset: str, current_amount: float, days: int) -> Tuple[float, float]:
    """
    Calculates the final amount of an asset after a given number of days, assuming a constant annual growth rate.

    Args:
        asset (str): The name of the asset.
        current_amount (float): The current amount invested in the asset.
        days (int): The number of days to calculate the final amount for.

    Returns:
        A tuple containing the profit/loss on the asset and the final amount after the given number of days.
    """
    final_amount = current_amount
    asset_data = get_asset_data(asset)
    annual_growth_rate = float(asset_data["growth_rate"])
    for _ in range(days):
        final_amount += final_amount * annual_growth_rate / 365
    
    return final_amount - asset, final_amount

def liabilities_final_amount(liability: str, current_principal: float, days: int) -> Tuple[float, float]:
    """
    Calculates the total interest paid and remaining principal for a given liability over a specified number of days.

    Args:
        liability (str): The name of the liability.
        current_principal (float): The current principal balance of the liability.
        days (int): The number of days over which to calculate the interest.

    Returns:
        tuple: A tuple containing the total interest paid (float) and the remaining principal balance (float).
    """
    remaining_principal = current_principal
    liability_data = get_liability_data(liability)
    annual_interest_rate = float(liability_data["interest_rate"])
    total_interest_paid = 0

    for _ in range(days):
        # This simple calculation assumes no extra payments to principal
        annual_interest = remaining_principal * annual_interest_rate / 365
        total_interest_paid += annual_interest
        # Normally you would decrease remaining_principal here if you were calculating amortization with payments
        remaining_principal -= annual_interest 

    return total_interest_paid, remaining_principal
# RetirementCalc
Overall objective: Calculate retirement glide paths to estimate wealth at a given retirement age and provide analytical tools to support retirement decision-making.

## Input Sheet
The calculator accepts a multi-tab Excel spreadsheet with organized inputs. Inputs in blue fonts need to be set prior to executing any code.
* Investments - All assumptions related money that is invested, including expected returns, expected volatility, return decay, and withdrawal expectations
* Expenses - Annual / monthly estimates for different categories of spending. Spending for certain categories is also reset as of retirement. Inflation expectations and their related uncertainty also serve as an input.
* Revenue - Monthly estimates for income and expectations for growth
* Salary_Data - Annual salary data to calculate expected Social Security income
* Other - Miscellaneous parameters that drive key model functionality

## Input Sheet detail - Investments
The calculator is set up to generate projections for a single brokerage account, IRA, 401K, and a residential home. Assumption balance and return expectations can be set to zero if one of these is not valid for the user. Parameters (columns) are defined below:
* BB: Beginning balance of the account as of the beginning of "Date_Start" on the "Other tab"
* Return: Expected monthly return for the account as of "Date_Start"
* Rtn_SD: Standard deviation of monthly returns for the account
* Decay: Expected returns are likely to decrease over a retirement horizon as (1) markets rise in value and (2) a future retiree allocates more money to safe, capital-preserving assets. The decay factor is meant to dampen expected returns the farther out the calculator makes predictions.
* Withdrawal_Dt: Initial date of withdrawal from the specified investment fund
* Withdrawal: Initial amount of withdrawal from the specified investment fund

## Input Sheet Detail - Expenses

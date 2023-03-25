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
* Enter the annual cost of each category in column B, except for 401K investments. This will be calculated based on current salary information provided elsewhere in the calculator
* The monthly cost of each category will automatically populate in column C
* For any categories where you expect spending behavior to substantially change upon retirement, you can enter an updated expectation for an annual spend in column D. If spending behavior is not expected to substantially change, leave column D blank. Note that the amount inputted in this column will be the annual spend the calculator uses for the first year of retirement.
* For any categories where column D is populated, a monthly cost will be automatically calculated in column E. If column D is not populated, column E will be blank.
* In column F, enter your expectation for year-over-year cost inflation within the category. Note that this is calculated elsewhere within the calculator for all investments (IRA, FOK, Brokerage)
* In column G, you can enter a standard deviation for your inflation rate, with more volatile categories having a higher standard deviation. If you would prefer to use a constant inflation rate, set column G to zero for all categories.


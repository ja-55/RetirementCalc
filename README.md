# RetirementCalc
Overall objective: Calculate retirement glide paths to estimate wealth at a given retirement age and provide analytical tools to support retirement decision-making.

## Input Sheet
The calculator accepts a multi-tab Excel spreadsheet with organized inputs. Inputs in blue fonts need to be set prior to executing any code.
* Investments - All assumptions related money that is invested, including expected returns, expected volatility, return decay, and withdrawal expectations
* Expenses - Annual / monthly estimates for different categories of spending. Spending for certain categories is also reset as of retirement. Inflation expectations and their related uncertainty also serve as an input.
* Revenue - Monthly estimates for income and expectations for growth
* Salary_Data - Annual salary data to calculate expected Social Security income
* Other - Miscellaneous parameters that drive key model functionality

## Input Sheet Detail - Investments
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

## Input Sheet Detail - Revenue
* The calculator accepts a monthly pre-tax salary (cell B2).
* Expected income from social security upon retiring is calculated in cell B3 from inputs in other parts of the calculator.
* Additional amounts can be inputted for regular gifts. The calculator assumes the gift amount occurs twice annually.
* All other expected regular income can be inputted in cell B5.
* In column C and D, enter expected year-over-year revenue increases and the standard deviation related to those increases.
* All investment-related lines are placeholders; these should not be changed or removed.

## Input Sheet Detail - Salary_Data
The calculator makes an estimate for expected income from Social Security based on salary history, which is provided by the user on this tab.
* Enter your initial year of regular employment in cell A2. Subsequent years will populate automatically.
* For each historical year, enter your actual, pre-tax salary for the year in column B.
* For each year in the future, input an estimated pre-tax salary for the year in column B (the default setting is for the calculator to grow the prior year by 2%).
* For each historical year, enter the name of the company you worked for in column C.
* In column D, a "working" or "retired" flag will populate automatically.

## Input Sheet Detail - Other
All other calculator parameters are held on this tab, described below:
* Tax_Salary: Tax rate on salary
* Tax_Investment: Tax rate on investment income not held in IRA
* FOK_Contribution: % of salary contributed to 401K
* FOK_Match: % of 401K contribution matched by employer
* Date_Start: Initial date considered by calculator
* Date_End: Last date considered by calculator
* Date_Retire: Date of retirement
* Date_SocSec: Date of social security eligibility
* BB_Sav: Beginning balance in cash savings as of start date
* SS_Excl: Fixed parameter used in calculation of social security income (tax exclusion)
* SS_Flag: Fixed parameter used in calculation of social security income
* Dist_size: The calculator sets up distributions for uncertain variables; all distributions will be set with this population parameter
* Sims: Number of simulations generated by the calculator

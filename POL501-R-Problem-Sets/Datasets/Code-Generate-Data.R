library(haven)
library(dplyr)

# Set Directory of the files of the project
setwd('C:\\Users\\Ignacio\\Dropbox\\PhD SBU\\06_Teaching\\00_POL-501\\Problem Sets\\PS-1\\W117_Nov22\\')

# Load File of Pew's ATP Wave 117
load_savfile <- read_spss("ATP W117.sav")

# Get a list/vector of variable names using the colnames(object) function.
var_names <- colnames(load_savfile)

# Use DPLYR "pipe" (%>%) and "verb" (select) to keep a subset of variables.
df_subset <- load_savfile %>%
  select(QKEY, VOTED_ATPCONG_W117, VTCOUNT_OWN_W117, ATTENDPERSON2_W117,
         F_AGECAT, F_GENDER, F_EDUCCAT)
a
# Use function "str" to get a quick look at the variables
str(df_subset)

' Questionnaire Response Coding:

ASK ALL CITIZENS (XCITIZEN=1):
VOTED_ATPCONG Which of the following statements best describes you?
1 I did not vote in the 2022 congressional elections
2 I planned to vote but wasn’t able to
3 I definitely voted in the 2022 congressional elections

ASK IF VOTED (VOTED_ATPCONG=3):
VTCOUNT_OWN How confident are you that your vote was accurately counted?
1 Very confident
2 Somewhat confident
3 Not too confident
4 Not at all confident

DISPLAY FOR ALL: Thinking more broadly, not just about the last month…
[SHOW ATTENDPERSON2 AND ATTENDONLINE2 ON SAME PAGE; DO NOT RANDOMIZE]
ASK ALL:
ATTENDPERSON2 In general how often do you attend religious services in person at a church, synagogue, mosque or other house of worship?
1 More than once a week
2 Once a week
3 Once or twice a month
4 A few times a year
5 Seldom
6 Never

F_AGECAT
Four-way category based on the panelist age as calculated from their date of birth. If only YOB is available, age is calculated as calendar year July 1 – YOB. If DOB and YOB are both unavailable, age is calculated as calendar year of recruitment survey – self-reported age at the time of recruitment. Age is updated annually during the annual profile survey
1 18-29
2 30-49
3 50-64
4 65+
99 Refused

F_GENDER
Gender.
GENDER Do you describe yourself as a man, a woman or in some other way?
1 A man
2 A woman
3 In some other way
99 Refused

F_EDUCCAT
Three-way category coded from self-reported educational attainment.
1 College graduate+ (EDUC_ACS =11,12,13,14)
2 Some college (EDUC_ACS =8,9,10)
3 H.S. graduate or less (EDUC_ACS =1,2,3,4,5,6,7)
99 Don’t know/Refused (EDUC_ACS =Refused)
'
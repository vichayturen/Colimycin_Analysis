library(mice)
library(readr)

data <- read_csv(
  "splits/WBC.csv",
  col_types = cols(
    患者编号 = col_character(),
    WBC = col_double(), WBC.1 = col_double(),
    WBC.2 = col_double(), WBC.3 = col_double(), 
    WBC.4 = col_double(), WBC.5 = col_double(), 
    WBC.6 = col_double()))
imp_data <- mice(
  data,
  method = "lasso.norm",
  m=5,
  printFlag=TRUE
)

imp_data$method

# Source:  www.openintro.org/stat/supplements.php
# License: CC BY-SA
#          creativecommons.org/licenses/by-sa/3.0/


#_____ Libraries and Data _____#
library(openintro)
library(OIdata)

setwd('C:\\Users\\Ignacio\\Dropbox\\PhD SBU\\06_Teaching\\00_POL-501\\DAP\\Example Student Analysis')

# Load the CSV file into a data frame
piracy <- read.csv("piracy.csv")

# View the first few rows of the data
head(piracy)


#_____ Only Work With Subset _____#
p <- piracy[piracy$stance %in% c("leaning no", "no", "yes") 
            & piracy$party != " I" 
            & !is.na(piracy$money_pro) 
            & !is.na(piracy$money_con), ]
p$stance <- factor(p$stance)
p$party <- factor(p$party)


#_____ Summaries _____#
plot(p$party, p$stance, xlab="", ylab="Stance", col=COL[c(2,1,3)])
mtext("Party", 1, 2.5)


#_____ Party and Stance _____#
chisq.test(table(p$party, p$stance))


#_____ Plots of Money _____#
histPlot(p$money_pro/1000, breaks = 50, xlim = c(0, 500), main="Industries in favor of SOPA/PIPA", col=COL[1], xlab="Lobbying money (in $1000s)", ylab="Frequency")
histPlot(p$money_con/1000, breaks = 50, xlim = c(0, 500), main="Industries against SOPA/PIPA", col=COL[1], xlab="Lobbying money (in $1000s)", ylab="Frequency")
tab <- rbind(c(mean(p$money_pro), mean(p$money_con)),
             c(median(p$money_pro), median(p$money_con)),
             c(sd(p$money_pro), sd(p$money_con)),
             c(IQR(p$money_pro), IQR(p$money_con)),
             c(min(p$money_pro), min(p$money_con)),
             c(max(p$money_pro), max(p$money_con)))
row.names(tab) <- c("Mean", "Median", "St. Dev.", "IQR", "Minimum", "Maximum")
colnames(tab)  <- c("money_pro", "money_con")
tab


#_____ Net Difference _____#
no <- p$stance %in% c("no", "leaning no")
d  <- p$money_pro/1000 - p$money_con/1000
histPlot(d[!no], breaks = 25, main="", border=COL[1], xlab="Net money (in $1000s)", ylab="", xlim=c(-150, 250), hollow=TRUE, lty=1, probability=TRUE)
histPlot(d[no], breaks = 25, main="", border=COL[4], lty=2, hollow=TRUE, add=TRUE, probability=TRUE)
legend("topright", lty=1:2, col=COL[c(1,4)], legend=c("Yes", "No, Leaning No"))
summary(lm(d ~ no))
summary(lm(d ~ p$party))
summary(lm(d ~ p$party + no))


#_____ Simple Tests _____#
t.test(p$money_pro[p$stance == "yes"], p$money_pro[p$stance %in% c("no", "leaning no")])
t.test(p$money_con[p$stance == "yes"], p$money_con[p$stance %in% c("no", "leaning no")])
money_net <- p$money_pro - p$money_con
t.test(money_net[p$stance == "yes"], money_net[p$stance == "no"])

tab <- round(
  rbind(c(mean(p$money_pro[p$stance == "yes"]),
          mean(p$money_pro[no]),
          mean(p$money_con[p$stance == "yes"]),
          mean(p$money_con[no])),
        c(sd(p$money_pro[p$stance == "yes"]),
          sd(p$money_pro[no]),
          sd(p$money_con[p$stance == "yes"]),
          sd(p$money_con[no])),
        c(sum(p$stance == "yes"),
          sum(no),
          sum(p$stance == "yes"),
          sum(no))))
colnames(tab)  <- c("Pro, Yes", "Pro, No", "Con, Yes", "Con, No")
row.names(tab) <- c("Mean", "St Dev", "n")
tab



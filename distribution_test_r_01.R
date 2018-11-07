library(spatstat)

path <- '/Users/michaelshih/Documents/code/personal_project/Ripleys_K_function_test'
outputfolder <- 'output'
outputsubfolder_csv <- 'csv'
filename <- 'P_ThomasPP_20'

inputpath <- file.path(path, outputfolder, outputsubfolder_csv, paste(filename, '.csv', sep = ''))
print(inputpath)


data <- read.csv(inputpath)
head(data)
summary(data)

dx = 20

mypattern <- ppp(data$x, data$y, c(0, dx), c(0, dx))
summary(mypattern)
# png("test.png", width = 10, height= 10, units= "in", res= 300)
# plot(mypattern, xlim = c(0, 20), ylim = c(0, 20))
# dev.off()
resultKest = Kest(mypattern)
plot(resultKest)
r <- resultKest$r
K <- resultKest$border
plot(r, K)
resultKest

resultLest = Lest(mypattern)
plot(resultLest)
r <- resultLest$r
L <- resultLest$border
plot(r, L)

H <- L - r
plot(r, H)
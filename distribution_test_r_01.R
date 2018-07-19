library(spatstat)

path <- '/Users/michaelshih/Documents/code/personal_project/Ripleys_K_function_test'
outputfolder <- 'output'
outputsubfolder_csv <- 'csv'
filename <- 'P_ThomasPP'

inputpath <- file.path(path, outputfolder, outputsubfolder_csv, paste(filename, '.csv', sep = ''))
print(inputpath)


data <- read.csv(inputpath)
head(data)
summary(data)


mypattern <- ppp(data$x, data$y, c(0, 20), c(0, 20))
summary(mypattern)
png("test.png", width = 10, height= 10, units= "in", res= 300)
plot(mypattern, xlim = c(0, 20), ylim = c(0, 20))
dev.off()

result_1 = Kest(mypattern, correction = 'none')
head(result_1$r)
r <- result_1$r
K <- result_1$un
plot(r, K)
plot(r, sqrt(K/pi))
plot(r, sqrt(K/pi) - r)
head(r)

# result_2 = Lest(mypattern, correction = 'border')
# head(result_2)
# r <- result_2$r
# L <- result_2$border
# L_rr <- L - r
# plot(r, L_rr)
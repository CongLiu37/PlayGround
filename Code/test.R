
argv = commandArgs(TRUE)#IDs, blastfile, output

IDs = read.csv(argv[1],header = F)$V1

blast = read.csv(argv[2],header = F, sep = "\t")

write.csv2(subset(blast,blast$V1 %in% IDs),argv[3],sep = "\t",quote = FALSE,col.names = FALSE)


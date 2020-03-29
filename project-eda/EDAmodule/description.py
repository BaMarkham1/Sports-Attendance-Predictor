def description(self, numRows=7):
    print("Exploratory Data analysis of %s begins.." % (self.dataset_filename))
    dataset = self.dataset
    print("First %d rows of the dataset" % (numRows))
    print(dataset.head(n=numRows))
    print(":===================================:")

    print("Detailed information about each column/variable of the dataset")
    print(dataset.info())
    print(":===================================:")

    print("Distribution of the numerical variables in the dataset")
    print(dataset.describe())
    dataset.describe().to_csv("distribution.csv")






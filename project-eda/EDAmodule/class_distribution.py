def class_distribution(self):
    import seaborn as sns
    import matplotlib.pyplot as plt
    import random
    sns.set()

    #plt.figure(random.randint(1,10))
    sns.countplot(x=self.target_column, data = self.dataset).set_title("Dataset = %s"%(self.dataset_filename))
    plt.show()




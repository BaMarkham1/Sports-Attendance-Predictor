def groupby_distribution(self,column1,column2):
    import seaborn as sns
    import matplotlib.pyplot as plt
    import random
    sns.set()

    print(self.dataset.groupby([column1,column2])[column2].count())

    # plt.figure(random.randint(1,10))
    sns.catplot(x=column1,col=column2,kind='count',data=self.dataset)
    plt.show()




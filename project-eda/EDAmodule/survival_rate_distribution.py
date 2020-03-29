def survival_rate_distribution(self,passenger_class_column):
    import seaborn as sns
    import matplotlib.pyplot as plt
    import pandas as pd
    import random
    sns.set()

    #plt.figure(random.randint(1,10))



    sns.catplot(passenger_class_column,self.target_column,kind='point',data=self.dataset)
    plt.show()




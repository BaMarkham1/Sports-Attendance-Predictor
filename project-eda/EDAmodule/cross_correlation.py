def cross_correlation(self, method='pearson'):
    import matplotlib.pyplot as plt
    import seaborn as sns
    corr_result = self.dataset.corr(method)
    print(corr_result)
    corr_result.to_csv("correlation_result.csv")

    #plt.matshow(corr_result)
    sns.heatmap(corr_result)
    plt.show()

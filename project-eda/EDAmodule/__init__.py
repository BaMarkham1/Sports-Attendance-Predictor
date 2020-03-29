class EDA:
    def __init__(self, dataset_filename, target_column):
        self.dataset_filename=dataset_filename
        self.target_column=target_column
        import pandas as pd
        # configure pandas display behavior
        pd.set_option('display.max_rows', 500)
        pd.set_option('display.max_columns', 500)
        pd.set_option('display.width', 1000)
        pd.set_option('precision', 2)

        print("Exploratory Data analysis of %s begins.." % (dataset_filename))

        # First load the dataset into pandas dataframe
        self.dataset = pd.read_csv(dataset_filename)



    #Imported methods
    from .description import description
    from .class_distribution import class_distribution
    from .groupby_distribution import groupby_distribution
    from .survival_rate_distribution import survival_rate_distribution
    from .cross_correlation import cross_correlation



from EDAmodule import *

ed_train = EDA("../csvs/full_dataset.csv","year 1 attendance")
ed_train.description(5)
ed_train.class_distribution()
ed_train.cross_correlation()


#ed_test = EDA("./dataset/test.csv","N/A")
#ed_test.description(5)
#ed_test.class_distribution()  #Due to the fact that test dataset does not have the survived column




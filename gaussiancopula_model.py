import pandas as pd
from sdv.demo import load_tabular_demo
from sdv.tabular import GaussianCopula


def create_gaussian_copula_model():
    # data = load_tabular_demo('student_placements')
    data = pd.read_csv("labeled-data/all-labeled-data.csv")

    model = GaussianCopula()
    model.fit(data)

    model.save("GaussianCopula model/gaussiancopula-model.pkl")


def load_gaussian_copula_model():
    return GaussianCopula.load("GaussianCopula model/gaussiancopula-model.pkl")


# create_gaussian_copula_model()
# model = load_gaussian_copula_model()
#
# new_data = model.sample(num_rows=202)
# print(new_data)
# new_data.to_csv("labeled-data/gaussiancopula-sample-data.csv", index=False)





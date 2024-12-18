from setuptools import find_packages, setup



setup(
    name="mlops",
    version="0.0.1",
    author="meyyappan",
    author_email="",
    install_requires=["pandas",
"scikit-learn",
"numpy",
"seaborn",
"flask",
"mlflow==2.2.2",
"dvc",
"ipykernel",
"xgboost",



"pytest==7.1.3",
"tox",
"black==22.8.0",
"flake8==5.0.4",
"mypy==0.971"],
    packages=find_packages(),
)

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()



REPO_NAME ="Personalized-Book-Recommendation-System"
AUTHOR_USER_NAME ="prit10-ing"
SRC_REPO ="book_ecommender"
LIST_OF_REQUIREMENTS = []



setup(
    name=SRC_REPO,
    version="0.0.1",
    author=AUTHOR_USER_NAME,
    description="A small project for personalized book recommendation system",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/prit10-ing/Personalized-Book-Recommendation-System/tree/main",
    author_email="priteshingle01@gmail.com",
    packages=find_packages(),
    install_requires=LIST_OF_REQUIREMENTS,
    python_requires=">=3.7",
    license="MIT",
)
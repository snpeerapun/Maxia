from setuptools import setup

# Read the requirements from requirements.txt file
with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name='maxia',
    version='0.1',
    author='Max AI',
    author_email='contac@oneable.co.th',
    description='Your project description',
    packages=['maxai'],  # Replace with your actual package name
    install_requires=requirements,
)

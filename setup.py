from setuptools import find_packages, setup
from typing import List

HYPHEN_E_DOT = '-e .'
def get_requirements(path: str) -> List[str] :
    with open(path, 'r') as f:
        requirements = f.readlines()
        requirements = [i.replace('\n', '') for i in requirements]
        
        if HYPHEN_E_DOT in requirements:
            requirements.remove(HYPHEN_E_DOT)
    return requirements

# print(get_requirements('requirements.txt'))
setup (
    name='ml1-krish',
    author='Shashi',
    author_email='shashi@gmail.com',
    packages=find_packages(),
    requires=get_requirements('requirements.txt')   
)
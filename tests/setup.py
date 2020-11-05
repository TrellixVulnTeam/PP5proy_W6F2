from setuptools import setup, find_packages

setup(
    name='TP_DONIS',
    version='2.0',
    extras_require=dict(tests=['unittest']),
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    author='Marina Donis',
    author_email='mdonis@fie.undef.edu.ar',
    description='10.000'
)
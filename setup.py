from setuptools import find_packages, setup

setup (
    name="PyMatsci",
    version="0.0.1",
    author="Yunzhe Wang",
    author_email="ywang393@jhu.edu",
    description="A python library facilitating computaional materials science.",
    #url = "",
    #project_urls = {
    #    "Bug Tracker": "",
    #},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache License 2.0",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "pyMatsci"},
    packages=find_packages(where="pyMatsci"),
    install_requires=[""],
    setup_requires=['pytest-runner'],
    tests_require=['pytest==4.4.1'],
    test_suite='tests',
)
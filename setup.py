import setuptools

with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    name="qe-forest",
    use_scm_version=True,
    author="Zapata Computing, Inc.",
    author_email="info@zapatacomputing.com",
    description="Forest backend for Orquestra.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/zapatacomputing/qe-forest ",
    packages=setuptools.find_packages(where="src/python"),
    package_dir={"": "src/python"},
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    setup_requires=["setuptools_scm~=6.0"],
    install_requires=[
        "z-quantum-core",
        "pyquil>=2.25.0",
    ],
    extras_require={
        "dev": ["pytest"],
    },
)

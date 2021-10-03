from setuptools import setup, find_packages

setup(
    name="rover",
    version="0.0.1",
    include_package_data=True,
    install_requires=["click","requests","pandas"],
    packages=find_packages(), 
    entry_points="""
        [console_scripts]
        rover=rover.cli:cli
    """,
)
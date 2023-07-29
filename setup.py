from setuptools import setup, find_packages

setup(
    name="prop_scraper",
    version="0.1.0",
    description="A scraper for property data in CABA Argentina",
    packages=find_packages(),
    install_requires=[
        "cloudscraper",
        "beautifulsoup4",
        "requests",
        "brotli"
    ],
    python_requires=">=3.6",
)

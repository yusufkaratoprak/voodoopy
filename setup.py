from setuptools import setup, find_packages

setup(
    name="voodoo-gui",
    version="0.1",
    description="A Python library to create UIs like Streamlit but with simple syntax",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="yusuf karatoprak",
    author_email="yusuf.karatoprak@voodoopy.com",
    packages=find_packages(),  # Automatically find packages in the directory
    include_package_data=True,
    install_requires=[
        "Flask",
        "requests",
        "flask_cors"
    ],
    python_requires=">=3.6",
)

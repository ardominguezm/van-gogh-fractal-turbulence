from setuptools import setup, find_packages

setup(
    name="vgfractals",
    version="1.0.0",
    author="Andy R. Domínguez-Monterroza",
    author_email="ardominguezm@gmail.com",
    description="Fractal Turbulence and Aesthetic Complexity in Van Gogh’s Paintings",
    packages=find_packages(),
    install_requires=[
        "numpy",
        "pandas",
        "matplotlib",
        "opencv-python",
        "scipy",
        "tqdm",
    ],
    python_requires=">=3.8",
)

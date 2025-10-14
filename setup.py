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

# pip install -e 
#import vgfractals as vg

#Y = vg.load_luminance("data/starry-night-1889.jpg")
#Hq, tau_q, alpha, f_alpha = vg.hurst_and_spectrum(...)
#vg.plot_spectra(...)


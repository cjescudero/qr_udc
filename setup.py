from setuptools import setup, find_namespace_packages

setup(
    name="qr_udc",
    version="0.1.0",
    packages=find_namespace_packages(include=['qr_udc', 'qr_udc.*']),
    package_dir={"": "src"},
    install_requires=[
        "fastapi",
        "uvicorn",
        "python-multipart",
        "pillow",
        "qrcode"
    ],
    python_requires=">=3.11",
) 
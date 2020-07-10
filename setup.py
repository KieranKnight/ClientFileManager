import setuptools

with open("README.md", "r") as fh:
    l_description = fh.read()


setuptools.setup(
    name='clientFileManager-pkg',
    version='1.0.0',
    author='Kieran Knight',
    author_email='kieransknight@gmail.com',
    description='Application that manages files recieved from a client and integrates them into an internal system',
    long_description=l_description,
    long_description_content_type='text/markdown',
    url='https://github.com/KieranKnight/ClientFileManager',
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent'
    ],
    python_requires='>=3.6'
)
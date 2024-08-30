from setuptools import setup, find_packages

setup(
    name='targetpilot-rag-lab',
    version='0.1.1',
    packages=find_packages(),
    install_requires=[
        'openai',
        'requests',
        'numpy',
        'pyecharts',
        'matplotlib',
        'networkx',
        'communities',
        'pandas',
        'loguru',
        'regex'
    ],
    author='targetpilot',
    author_email='your.email@example.com',
    description='RAG-LAB is an open-source lighter, faster and cheaper RAG toolkit supported by Target Pilot, designed to transform the latest RAG concepts into stable and practical engineering tools. The project currently supports GraphRAG and HybridRAG.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/EcomPilot/rag-lab',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)

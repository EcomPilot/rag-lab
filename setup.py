from setuptools import setup, find_packages

setup(
    name='raglab2',
    version='0.1.10',
    packages=find_packages(),
    license='MIT',
    install_requires=[
        'openai',
        'requests',
        'numpy',
        'pyecharts',
        'matplotlib',
        'networkx',
        'pandas',
        'loguru',
        'regex',
        'tqdm'
    ],
    author='targetpilot',
    author_email='ai-research@targetpilot.ai',
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

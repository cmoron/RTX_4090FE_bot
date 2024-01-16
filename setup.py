from setuptools import setup, find_packages

setup(
    name='RTX4090_FE_tracker',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'discord.py',
        'python-dotenv',
    ],
    entry_points={
        'console_scripts': [
            'rtx_4090fe_bot=bot.main:main'
        ]
    }
)

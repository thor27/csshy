from setuptools import setup


def readme():
    with open('README.md') as f:
        return f.read()


setup(
      name='csshy',
      version='0.2',
      description='Improved ClusterSSH for modern terminals like Terminator and Tilix',
      long_description=readme(),
      classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Environment :: Console',
        'Operating System :: POSIX :: Linux'
      ],
      keywords='funniest joke comedy flying circus',
      url='https://github.com/thor27/csshy',
      author='Thomaz Reis',
      author_email='thor27@gmail.com',
      license='GPLv3',
      packages=['csshy'],
      install_requires=[
          'configobj',
      ],
      entry_points={
            'console_scripts': ['csshy=csshy.csshy:main'],
      },
      include_package_data=True,
      zip_safe=False
)

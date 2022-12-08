from setuptools import setup, find_packages

package_name = 'self_drive'

setup(
    name=package_name,
    version='0.1.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    author='LHJ, LJE',
    author_email='sbdyr025@sch.ac.kr',
    maintainer='LHJ, LJE',
    maintainer_email='sbdyr025@sch.ac.kr',
    keywords=['ROS'],
    classifiers=[
        'Intended Audience :: Developers',
        'License :: MIT License',
        'Programming Language :: Python'
    ],
    description='turtlebot3 self drive controller',
    license='MIT License',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            f'self_drive = {package_name}.self_drive:main',
        ],
    },
)

import argparse
parser = argparse.ArgumentParser(description='Regards to your name.')
parser.add_argument('-n', dest='m_name', type=str, help='your name')
options = parser.parse_args()
print('Hello', options.m_name)

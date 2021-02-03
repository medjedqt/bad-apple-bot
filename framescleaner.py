import os

if __name__ == '__main__':

	folder = 'frames'
	for filename in os.listdir(folder):
		os.remove(f'{folder}/{filename}')
import uuid

def generate(count, filename):
    with open(filename, 'w') as f:
        for i in range(count):
            f.write(str(uuid.uuid4()))
            f.write('\n')

if __name__ == '__main__':
    generate(100000, 'movies')
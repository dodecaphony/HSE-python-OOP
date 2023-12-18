import hse_normalizer.normalizer.normalizer as norm


def main():
    normalizer = norm.Normalizer('17/05/99')
    normalizer.normalize()
    print(normalizer.text)


if __name__ == '__main__':
    main()

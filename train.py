from ai.Agent import train_agent


def main():
    hyperparameters = {
        'alpha': 0.1,
        'gamma': 0.9,
        'epsilon': 0.1,
        'episodes': 1000
    }
    train_agent(hyperparameters)


if __name__ == '__main__':
    main()
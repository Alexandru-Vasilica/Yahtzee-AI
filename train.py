from ai.Agent import train_agent, QTableSerializer


def main():
    hyperparameters = {
        'alpha': 0.1,
        'gamma': 0.9,
        'epsilon_start': 1.0,
        'epsilon_min': 0.01,
        'epsilon_decay': 0.995,
        'episodes': 150000
    }
    train_agent(hyperparameters)


if __name__ == '__main__':
    main()

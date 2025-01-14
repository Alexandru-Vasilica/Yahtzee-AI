from matplotlib import pyplot as plt
from os import path
from state.Action import get_action_from_index

save_path = "agents"


def show_scores(scores, save_path=None):
    plt.figure(figsize=(10, 6))
    plt.plot(scores, label="Score per Episode")
    plt.xlabel("Episode")
    plt.ylabel("Score")
    plt.title("Scores Obtained by Each Episode")
    plt.legend()
    plt.grid()
    if save_path:
        plt.savefig(path.join(save_path, "scores_plot.png"))

    plt.show()


def train_agent(agent, env, num_episodes=1000, batch_size=100):
    best_average_score = 0
    agent.mode = 'train'
    scores = []

    for episode in range(num_episodes):
        state = env.reset()
        total_reward = 0
        done = False

        while not done:
            action_index = agent.choose_action(state)
            action = get_action_from_index(action_index)
            next_state, reward, done, info = env.step(action)
            agent.replay_buffer.add(state.to_features(), action.index, reward, next_state.to_features(), done)
            state = next_state
            total_reward += reward
            agent.train(batch_size)
        scores.append(total_reward)
        if (episode + 1) % 100 == 0:
            print(f"Episode: {episode + 1}, Total Reward: {total_reward}, Epsilon: {agent.epsilon}")
        if (episode + 1) % 1_000 == 0:
            agent.save(path.join(save_path, f"agent_2_{episode + 1}.pth"))
            show_scores(scores, save_path)
            best_score, avg_score = evaluate_agent(agent, env, num_episodes=100)
            print(f"Best Score: {best_score}, Average Score: {avg_score}")
            if avg_score > best_average_score:
                best_average_score = avg_score
                agent.save(path.join(save_path, f"agent_2_best.pth"))


def evaluate_agent(agent, env, num_episodes=100, detailed=False):
    agent.mode = 'eval'
    scores = []
    final_scores = []

    for episode in range(num_episodes):
        state = env.reset()
        total_reward = 0
        done = False

        while not done:
            action_index = agent.choose_action(state)
            action = get_action_from_index(action_index)
            next_state, reward, done, info = env.step(action)
            state = next_state
            total_reward += reward
        scores.append(total_reward)
        final_scores.append(info['score'])
        if detailed:
            print(f"Episode: {episode + 1}, Total Reward: {total_reward}")
    best_score = max(scores)
    total_scores = sum(scores)
    agent.mode = 'train'
    if detailed:
        show_scores(scores)
        print(f"Best final score: {max(final_scores)}")
        print(f"Total final score: {sum(final_scores)}")
    return best_score, total_scores / len(scores)



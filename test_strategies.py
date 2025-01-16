from player.Strategy import AgentStrategy, test_strategy, MinMaxStrategy

# agent_strategy = AgentStrategy('agents/agent_best.pth')
# print('Agent strategy')
# test_strategy(agent_strategy, 1000)
#
# agent_strategy_2 = AgentStrategy('agents/agent_best_2.pth')
# print('Agent 2 strategy')
# test_strategy(agent_strategy_2, 1000)
#
# agent_strategy_10000 = AgentStrategy('agents/agent_2_10000.pth')
# print('Agent 10000 strategy')
# test_strategy(agent_strategy_10000, 1000)

minmax_strategy = MinMaxStrategy(3)
print('MinMax strategy')
test_strategy(minmax_strategy, 20)


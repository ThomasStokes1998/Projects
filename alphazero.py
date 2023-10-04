# General Model For AlphaZero
import time
import math
import random
import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow import keras

# Add a Play AlphaZero Feature

class Node:
    def __init__(self, priorprob: float, val: float):
        self.wins = 0
        self.draws = 0
        self.visits = 0
        # Estimated probability of winning from this position
        self.priorprob = priorprob
        self.expanded = False
        # Estimation for the value of the rest of the decision tree
        self.val = val
        # Stores data about child nodes for creating the training data quicker
        self.childkeys = {}

    def searchScore(self, parent, k: float= 1):
        u = self.priorprob
        m = parent.visits
        n = self.visits
        return u + math.sqrt(m) / (n * k + 1)

    def value(self):
        if self.visits == 0:
            return self.val
        else:
            return (self.wins + 0.5 * self.draws) / self.visits

    def score(self):
        if self.visits == 0:
            return self.priorprob
        else:
            return self.wins / self.visits

class AlphaZero:
    def __init__(self, env, policy) -> None:
        self.env = env
        self.policy = policy
        self.nodes = {}
    
    # Selects the next move to play
    def selectChild(self, state, parent, training: bool=True, policy=None):
        if policy is None:
            policy = self.policy
        maxstate = []
        maxstate0 = []
        maxscore = 0
        maxnode = None
        maxencode = ""
        # Flip the board because we are playing from the opponents perspective
        childscores = policy.predict([state], verbose=0)[0]
        legalmoves = self.env.legalMoves(state)
        for i, action in enumerate(self.env.actions):
            if action not in legalmoves:
                continue
            childstate0 = self.env.move(action, state)
            childstate = self.env.flipState(childstate0)
            # None means the action is illegal
            if childstate is not None:
                if i in parent.childkeys:
                    childencode = parent.childkeys[i]
                else:
                    childencode = self.env.encodeState(childstate)
                    parent.childkeys[i] = childencode
                # The child score is always greater than equal to the priorprob
                if childencode not in self.nodes:
                    # We only care about the value of a node in actual play
                    if training:
                        childval = 0.5
                    else:
                        childval = policy.predict([childstate], verbose=0)[0][-1]
                    self.nodes[childencode] = Node(childscores[i], childval)
                childscore = self.nodes[childencode].searchScore(parent)
                if childscore > maxscore:
                    maxencode = childencode
                    maxstate = childstate
                    maxstate0 = childstate0
                    maxscore = childscore
                    maxnode = self.nodes[childencode]
        return maxstate, maxstate0, maxnode, maxencode

    # Decides what move to play during a game
    def run(self, iterations: int, state, policy=None, info: bool=False):
        if policy is None:
            policy = self.policy
        self.nodes = {}
        # Create the root node
        root_evals = policy.predict([state], verbose=0)[0]
        rootkey = self.env.encodeState(state)
        self.nodes[rootkey] = Node(1, root_evals[-1])
        root = self.nodes[rootkey]
        for _ in range(iterations):
            # Branching bool is to avoid going to the same end node multiples times
            branching = True
            while branching:
                current_node = root
                current_node.visits += 1
                current_state = state
                new_state = state
                search_path = [rootkey]
                state_path = [state]
                # Get the next node to expand
                while current_node.expanded and self.env.reward(new_state) is None:
                    childstate, flippedchildstate, childnode, childencode = self.selectChild(current_state, current_node, False, policy)
                    current_state = childstate
                    current_node = childnode
                    new_state = flippedchildstate
                    search_path.append(childencode)
                    state_path.append(current_state)
                    current_node.visits += 1
                if self.env.reward(new_state) is None:
                    # Expand the new node
                    _, _, _, _ = self.selectChild(current_state, current_node, False, policy)
                    branching = False
                    # Assumes the opponent makes the best move according to our algorithm
                    current_node.val = 1 - max([self.nodes[current_node.childkeys[l]].val for l in current_node.childkeys])
                else:
                    # First time visiting the end state
                    if not current_node.expanded:
                        branching = False
                    # Gives the objective value for a node
                    current_node.val = self.env.reward(new_state)
                current_node.expanded = True
                # Propagate the values back up the tree
                for i in reversed(range(len(search_path)-1)):
                    nodekey = search_path[i]
                    node = self.nodes[nodekey]
                    # Assumes the opponnent makes the best move according to our algorithm
                    node.val = 1 - max([self.nodes[node.childkeys[l]].val for l in node.childkeys])
        # Pick the best move based on the search
        maxval = 0
        maxmove = 0
        if info:
            evals = []
        for l, _ in enumerate(self.env.actions):
            if l not in root.childkeys and info:
                evals.append(0)
            elif l in root.childkeys:
                childkey = root.childkeys[l]
                if info:
                    evals.append(round(self.nodes[childkey].val, 2))
                if self.nodes[childkey].val > maxval:
                    maxmove = l
                    maxval = self.nodes[childkey].val
        if info:
            return maxmove, evals
        return maxmove
    
    # Plays a game between two AI's, returns the score for policy1
    def testGame(self, iterations: int, policy1=None, policy2=None, randomplay=False, rmoves: int = 0, gameinfo: bool=False):
        if policy1 is None:
            policy1 = self.policy
        if policy2 is None and not randomplay:
            policy2 = self.policy
        policies = [policy1, policy2]
        self.env.reset()
        turn_counter = 0
        playing = True
        state = self.env.initstate
        gamehist = []
        while playing:
            state = self.env.flipState(state)
            policy = policies[turn_counter % 2]
            legalmoves = self.env.legalMoves(state)
            # Catch bugs
            if len(legalmoves) == 0:
                print("No legal moves")
                print(f"Game history = {gamehist}")
                self.env.printBoard(state)
                if gameinfo:
                    return 0.5, gamehist
                return 0.5
            # Selects a random move.
            if policy is None or turn_counter // 2 < rmoves:
                bestmove = random.choice(legalmoves)
                newstate = self.env.move(bestmove, state)
                if newstate is None:
                    testedactions = [bestmove]
                    while newstate is None:
                        if len(testedactions) == len(self.env.actions):
                            break
                        bestmove = random.choice(self.env.actions)
                        while bestmove in testedactions:
                            bestmove = random.choice(self.env.actions)
                        newstate = self.env.move(bestmove, state)
                        testedactions.append(bestmove)
            # Uses a neural network to select a move.
            else:
                bestmove = self.run(iterations, state, policy)
                newstate = self.env.move(bestmove, state)
            gamehist.append(bestmove)
            state = newstate
            if state is None:
                # Catch bugs
                if turn_counter < self.env.width * self.env.height:
                    print(f"turns={turn_counter}, gamehist = {gamehist}")
                if gameinfo:
                    return 0.5, gamehist
                return 0.5
            if self.env.reward(state) is not None:
                playing = False
                if turn_counter % 2 == 0:
                    if gameinfo:
                        return self.env.reward(state), gamehist
                    return self.env.reward(state)
                else:
                    if gameinfo:
                        return 1 - self.env.reward(state), gamehist
                    return 1 - self.env.reward(state)
            turn_counter += 1

    # Estimates the ELO based on playing against an opponnent with a known ELO score
    def estimateELO(self, iterations: int, games: int, policy=None, opponnent=None, oppELO: int=0, lam: int=400, 
    rmoves: int=2) -> int:
        results = []
        if opponnent is None:
            rplay = True
        else:
            rplay = False
        for _ in range(games):
            result = self.testGame(iterations, policy, opponnent, rplay, rmoves)
            results.append(result)
        p = np.mean(results)
        if p == 1:
            return round(oppELO + lam * math.log10(2 * games))
        return max(0, round(oppELO + lam * math.log10(max(1/games, p / (1 - p)))))
    
    # Trains the next generation of AlphaZero
    def train(self, games: int, outputname: str = "newpolicy.h5", epochs: int=5, batch_size: int = 256,
    printprogress: bool = False, printfrequency: int = 100, savefrequency: int = 100, savename: str=None,
    loadpath: str=None, testopp = None, testoppelo: int = 0, elothresh: int=50, testgames: int=100, testiterations: int=1,
    trainprop: float = 0.2):
        self.nodes = {}
        # Load in training data
        if loadpath is not None:
            ld = pd.read_csv(loadpath)
            for i, e in enumerate(ld.encodings):
                self.nodes[e] = Node(ld.priorprobs[i], 0.5)
                node = self.nodes[e]
                node.wins = ld.wins[i]
                node.draws = ld.draws[i]
                node.visits = ld.visits[i]
                if ld.expanded[i] == 0:
                    node.expanded = False
                else:
                    node.expanded = True
        # Game Data
        gamewins = 0
        gamedraws = 0
        gamelengths = []
        t0 = time.time()
        parentstate = self.env.initstate
        initencode = self.env.encodeState(parentstate)
        self.nodes[initencode] = Node(0.5, 0.5)
        for g in range(1, games+1):
            #self.env.reset()
            parentstate = self.env.initstate
            parent = self.nodes[initencode]
            movehist = [initencode]
            playing = True
            while playing:
                parent.visits += 1
                if len(parentstate) == 0:
                    print(parentstate)
                    print("Parent Visits:",parent.visits)
                    print(f"Games: {g}")
                    for i, m in enumerate(movehist):
                        print(f"Move {i}:",m)
                childstate, flippedchildstate, childnode, childencode = self.selectChild(parentstate, parent)
                parent.expanded = True
                # Check for end state
                # No more legal moves
                if childnode is None:
                    #print("No more detected legal moves.")
                    #print(self.env.printBoard(parentstate))
                    gamedraws += 1
                    gamelengths.append(len(movehist))
                    for encode in movehist:
                        self.nodes[encode].draws += 1
                    playing = False
                # Check for reward
                else:
                    movehist.append(childencode)
                    childreward = self.env.reward(flippedchildstate)
                    if childreward is not None:
                        #print("Detected a reward")
                        #print(self.env.printBoard(flippedchildstate))
                        if childreward == 0.5:
                            gamedraws += 1
                            gamelengths.append(len(movehist))
                            for encode in movehist:
                                self.nodes[encode].draws += 1
                        else:
                            l = len(movehist)
                            gamelengths.append(l)
                            if l % 2 == 0:
                                gamewins += 1
                            for i, encode in enumerate(movehist):
                                if i % 2 == l % 2:
                                    self.nodes[encode].wins += 1
                        playing = False
                parentstate = childstate
                parent = childnode
            # Save exploration progress
            if g % savefrequency == 0:
                encodings, priorprobs, wins, draws, visits, exp = [], [], [], [], [], []
                for e in self.nodes:
                    node = self.nodes[e]
                    encodings.append(e)
                    priorprobs.append(node.priorprob)
                    wins.append(node.wins)
                    draws.append(node.draws)
                    visits.append(node.visits)
                    if node.expanded:
                        exp.append(1)
                    else:
                        exp.append(0)
                df = pd.DataFrame({"encodings":encodings, "priorprobs":priorprobs, "wins":wins, "draws":draws, 
                "visits":visits, "expanded":exp})
                if savename is None:
                    savename = f"azsave.csv"
                df.to_csv(savename, index=False)

            if printprogress and g % printfrequency == 0:
                dt = time.time() - t0
                print(f"Completed {g} games. Time elapsed for last {printfrequency} games: {round(dt, 3)} seconds.")
                print(f"Wins: {gamewins}, Draws: {gamedraws}, Losses:{g - gamewins - gamedraws}")
                print(f"Game Lengths: LQ={np.percentile(gamelengths, 25)}, Median={np.median(gamelengths)}, UQ={np.percentile(gamelengths, 75)}")
                s = round(dt * (games - g) / printfrequency)
                m = s // 60
                h = m // 60
                print(f"Estimated time remaning: {h}:{m - 60*h}:{s - 60*m}.")
                t0 = time.time()
        # Make the training data from the games
        x_train = []
        y_train = []
        for encode in self.nodes:
            # Only train on a set proportion of training data
            if random.random() > trainprop:
                    continue
            node = self.nodes[encode]
            # Only train on nodes that were played during training.
            if node.visits > 0:
                x_train.append(self.env.decode(encode))
                y_scores = []
                for i, _ in enumerate(self.env.actions):
                    if node.expanded:
                        if i in node.childkeys:
                            childencode = node.childkeys[i]
                            y_scores.append(self.nodes[childencode].score())
                        else:
                            y_scores.append(0)
                    else:
                        y_scores.append(node.score())
                y_scores.append(node.value())
                y_train.append(y_scores)
        self.policy.fit(x_train, y_train, epochs=epochs, batch_size=batch_size)
        # Play a test game to see if the policy has improved sufficently
        print("Playing games against the previous version of AlphaZero to see if there has been sufficent improvement.")
        newelo = self.estimateELO(testiterations, testgames, None, testopp, testoppelo)
        # If there has been a sufficent improvement
        print(f"Old ELO: {testoppelo}, New ELO: {newelo}")
        if newelo > testoppelo + elothresh:
            print("ELO threshold reached")
            self.policy.save(outputname)
        # If this has not happened then more training is needed
        else:
            print("ELO threshold not reached")
            self.train(games, outputname, epochs, batch_size, printprogress, printfrequency, savefrequency, savename,
            savename, testopp, testoppelo, elothresh, testgames, testiterations)
            
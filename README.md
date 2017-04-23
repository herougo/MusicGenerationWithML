## Music Generation With Machine Learning

This is a repository for generating music by combining different machine learning algorithms. The main idea is to have a model for predicting whether a melody is good. You then use a reinforcement learning agent which gets feedback from that model to construct a policy which leads to creating good music. 

All code was written by me except for the RL code in music_generation/reinforcement_learning.py.

### To Do
- [x] Understand the MIDI file format
- [x] Write a MIDI parser
- [x] debug the MIDI parser
- [x] write the music theory code
- [x] organize the data set
- [x] generate random songs as bad songs for the music rating predictor
- [x] implement features for a music rating predictor
- [x] create the data for the music rating model
- [x] train the music rating model
- [x] gather RL code
- [x] write the environment class for the RL agent
- [x] try formulation 1
- [ ] investigate improving performance of the RL agent
- [ ] try formulation 2

### Music Rating Model Results

A random tree model was trained on a data set of 285 points using a train, validation, test split of 0.6, 0.2, 0.2. The resulting validation set and test set accuracies accuracy were 95.7% and 98.2% respectively.


### Possible Reinforcement Learning Formulations:
1. 1 bar of music with 8 eighth notes (agent determines the notes)
2. same as previous example, but 1 new action is added to be able to sustain the previous note.
3. generate a 4 bar phrase using a I IV V I chord progression
4. 2 separate agents to handle rhythm and melody generation (inspired by Maluuba's paper on separation of concerns)
5. 1 agent which decides the next note and duration in the moment

### Next Steps:
1. try Monte Carlo Tree Search
2. have an agent which manages repitition of melodies
3. have an agent which manages harmony structure
### Music Generation With Machine Learning

This is a repository for generating music by combing different machine learning algorithms. The main idea is to have a model for predicting whether a melody is good. You then use a reinforcement learning agent which gets feedback from that model to construct a policy which leads to creating good music. 

All code was written by me except for the code in the "unused folder".

- [x] Understand the MIDI file format
- [x] Write a MIDI parser
- [ ] debug the MIDI parser and organize the data set
- [ ] implement features for a music rating predictor and train the model
- [ ] implement an RL model for choosing a rhythm and train the model
- [ ] implement an RL model for choosing a melody given a rhythm and train the model
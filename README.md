## Music Generation With Machine Learning

This is a repository for generating music by combining different machine learning algorithms. The main idea is to have a model for predicting whether a melody is good. You then use a reinforcement learning agent which gets feedback from that model to construct a policy which leads to creating good music. 

All code was written by me except for the code in the "unused folder".

To Do
- [x] Understand the MIDI file format
- [x] Write a MIDI parser
- [x] debug the MIDI parser
- [x] write the music theory code
- [ ] organize the data set
- [ ] generate random songs as bad songs for the music rating predictor
- [ ] implement features for a music rating predictor
- [ ] train the music rating model
- [ ] gather the RL code
- [ ] try formulation 1
- [ ] try formulation 2


Possible Reinforcement Learning Formulations:
1. 1 bar of music with 8 eighth notes (agent determines the notes)
2. same as previous example, but 1 new action is added to be able to sustain the previous note.
3. 2 separate agents to handle rhythm and melody generation (inspired by Maluuba's paper on separation of concerns)
4. 1 agent which decides the next note and duration in the moment

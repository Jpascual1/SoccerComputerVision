# SoccerComputerVision

My goal is to train yolo models so that I can track players, the ball, the referees, and the lines on a soccer field,  With this I would like to build all sorts of tools that can use this.

# Training

I trained a Yolo26s model on two data sets with Ball, Player, and Referee.  I used google colab to train the model with their free gpu usage, where I uploaded the zips of the data sets I got from roboflow.  I had to modify the tags of the football-players-detection set as it used ball, player, referee, and goalkeeper tags while the other used Ball, Player, Referee.  Since Goalkeepers are just players and to train on both data sets at the same time the tags needed to be the same I used a script to switch the tags.  In total there were 1834 images, I wanted to get a very wide range of views and these two combined gave me a wide range.  The training process was a learning process as it took me about 3 tries to get it down from the model size, epochs, and the resolution to use.  The first try I had used yolo26n with 100 epochs and 1000 resolution, then halfway through my colab connection disconnected and I lost the progress,   second try I completed it but the model wasn't quite what I wanted, and finally the third time I changed it to 60 epochs as I had seen there wasn't much progress past 55 as well as switching to the 26s and raising the resolution to 1280 so the ball would be more clear.

https://universe.roboflow.com/nikhil-chapre-xgndf/detect-players-dgxz0/dataset/7
https://universe.roboflow.com/roboflow-jvuqo/football-players-detection-3zvbc/dataset/20

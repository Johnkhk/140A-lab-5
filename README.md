# README - ECE140A Lab 5

## Introduction

In lab 5, we will use components and concepts from previous labs (with a few
more additional components) to make our JetBots participate in a relay race
autonomously. The lab will be divided into five (six) stages:

0. **Setup**. Getting the lab 5 code on your JetBots.
1. **Pre-processing**. The participants perform calibration.
2. **Discovery**. The participants discover each other.
3. **Consensus**. The participants will decide where each of them should start the
   race.
4. **Race**. Self-explantory.
5. **Post-processing**. The participants aggregate the information obtained during
   the race to generate a "map" of the tracks.

> Note: This lab will have checkpoints/deliverables corresponding to every stage
> that must be demonstrated on the specified lab session dates.


> Note: If the TAs find that the lab is easier or harder than expected then they
> may increase or decrease the complexity of some of the stages (yay modularity!), so keep your
> eyes peeled for their Piazza posts.

## Setup

Perform the following steps for the setup stage.

1. Get the `140A-lab-5` repo (if you're reading this then you already have it).
2. Make sure that you have the MQTT and ML stuff on you JetBot from the previous labs.
3. Copy your repo on to your JetBot.

### Deliverables

1. The lab 5 repo copied to your JetBot.
2. Brief demonstration of your ML behaviors. Even if you couldn't get them to
   work perfectly for lab 2, you have a chance to improve them now.

## Pre-processing

For the subsequent stages, you'll need to know where exactly your JetBot is in
the Relay Race World. The TAs will define a frame of reference for that world.
If you start at (0, 0) (in inches/meters) and you move with a speed of 0.4
(JetBot speed) along the x-axis, where will you be? That's exactly the kind of
questions you're looking to answer in this stage. We will use [linear
interpolation](https://en.wikipedia.org/wiki/Linear_interpolation) to achieve
this. You can write your own linear interpolation function or use the [utility
provided by
scipy](https://docs.scipy.org/doc/scipy/reference/generated/scipy.interpolate.interp1d.html#scipy.interpolate.interp1d).
Here's what you'll need to do for this stage:

1. Decide on a fix duration of time (say 5s).
2. Set the JetBot speed to a fixed value, say 0.25. Run the JetBot forward for
   that duration of time.
> Warning: Don't set the speed too low; that will lead to all kinds of
> calibration problems.

3. Measure how far the JetBot travelled with a measuring tape.
4. Calculate the speed of the JetBot in m/s (or inches/s).
5. Repeat 2-4 for at least 5 different JetBot speeds.
6. Use your measurements, x =  JetBot speeds and y =  real speeds to write
   a linear interpolation function.
> Note: Please don't use polynomial interpolation or any other fancy
> interpolation strategies; we want to keep things simple and easy to evaluate.

We will also need similar interpolation for (in-place) rotation. But to begin,
you can just find out how long you need to rotate for at, say 0.4 (JetBot)
speed to do a 90 degree turn. The TAs will decide later on whether or not you
need to do interpolation for rotation too.

### Deliverables

1. A python function that performs linear interpolation of JetBot speeds
   correctly.
2. A python function that rotates the JetBot by 90 degrees.
   
### Checkpoints
1. You should be able to demonstrate commands like "go to (1, 2) assuming that
   you are at (-1, 3)."

## Discovery

This stage is *very* similar to problem 1 from lab 4. First, the TAs will
arbitrarily pick three teams to participate in a race. These teams must discover
each other using MQTT communication. 

1. Each team publishes information about themselves on the topic
   `lab5/discovery` with the [appropriate message
   format](messages/team_discovery.json).
2. Each team must maintain a dictionary of all the participating teams(including
   self). This dictionary should not contain any duplicates.
3. Each then team subscribes to the topic `lab5/<own_teamname>/in` and should
   publish to `lab5/<teamname>/in` to send messages to team `<teamname>`.

### Deliverables

1. A python function that publishes the team information.
2. Demonstration that you are indeed subscribed to `lab5/<own_teamname>/in`.

## Consensus

In an IoT or a distributed environment, it is essential that different parties
have some mechanism for achieving consensus concerning decisions that affect
them all. It turns out that, in general, this is a very difficult problem to solve.
However, by making some assumptions we can make it significantly more tractable. For
this stage, first we will operate under the assumption that no (malicious)
adversaries exist. Then we will relax that assumption a bit by saying that the
majority of the players are not adversaries.

The main task at hand here is to get from a "pit-stop" position to the nearest
(for each team) starting point.

### Assumption 1: No adversaries

Under this assumption, all that is needed for successful behavior is that a
majority of the players have "correct" behavior. This is how we proceed:

1. The TAs will assign a "pit-stop" position to each team. Each pit-stop has an
   associated number (1, 2 or 3) associated with it. They will also assign a
   team to be the "leader" randomly (more on this later).
2. The teams must subscribe to topics `lab5/consensus/pitstop_coordinates/<i>`, where
   `<i> = 1, 2, 3`. The message you receive is of the [given format](messages/coordinates.json).
   Then they place their JetBots in the appropriate locations.
3. For these pit-stops, each team needs to make its way to the nearest starting
   point. The coordinates of each starting point can be found by subscribing to
   `lab5/consensus/start_coordinates/<i>`, where `<i> = 1, 2, 3`. The message
   format is the [same as above](messages/coordinates.json).
4. Now that each team has access to all the pit-stop and starting coordinates,
   to demonstrate your understanding of the problem, you need to compute the
   distance between each of the pit-stops to each of the starting points.
   Convert this computed information in a serialzed JSON object (by using
   `json.dumps` or similar) and send it as a message to the topic
   `lab5/consensus/understanding`. [See here](messages/understanding.json) for
   the message format.
5. Each team verifies the correctness of every other team's calculation and
   publishes [a message](messages/ok.json) accordingly to `lab5/consensus/understanding/ok`;
6. They leader team must check the `lab5/consensus/understanding/ok` topic and
   see that every team has been verified.
   1. If everything is okay, then the leader sends [a
      message](messages/init.json) to the other teams on `lab5/<teamname>/in`
      and each of them start moving to the start points.
   2. If not, the TAs step in and diagnose the faulty parts.

### Assumption 2: With two adversaries

> Note: This is not a part of the lab currently, but could be included later.

Steps 1-4 are exactly the same as when operating under assumption 1. But now,
there will be two adversarial players (read: the TAs) that are impersonating
some teams. They will publish incorrect distance calculations. 

### Deliverables

1. A python function that calulates the euclidean distance between two points.
2. A python method that uses the above function to calculate the distance
   between the pit-stops and starting points, and publishes this.
3. Demonstration of correct message publishing and subscribing.
4. A python method that verifies the distance calulations against their own calculations.
5. A python method that does the verification (as done by the leader).
   
### Checkpoints

1. A successful run-through of the above scenario.

## Race

Finally! The JetBots are at the three starting points. This proceeds as follows:

1. The leader is subscribed to the topic `lab5/race/go`.
2. As soon as the leader receives [a message](messages/go.json) on that topic,
   it sends [a message](messages/go.json) to the team on start position 1 on
   their personal topic.
3. As soon as that team receives a message from the leader, it starts moving
   using the road following ML behavior.
4. It continues to move until its collision avoidance detects an obstacle (the
   next JetBot).
> Note: there will be no other obstacles on the track, so the first obstacle to
> be detected should be the next JetBot.

5. The first JetBot then stops and sends [a message](messages/go.json) to the
   next team. The second team repeats this.
6. The third team also does the same, except that it sends [a different message](messages/completed.json).
   to its teammates and to the topic `lab5/race/completed`.
7. During the race, each team logs the coordinates of the points they passed
   through. When it receives a ["race-completed"
   message](messages/completed.json), it sends [a message](messages/path.json) with list of points
   that it passed through to the leader.
8. The leader aggregates these path messages into a [single path message](messages/aggregate_path.json) and
   publishes it to `lab5/race/path`.

### Deliverables

1. Good road following behavior. Improved from before if it wasn't robust.
2. Good collision avoidance behavior (especially at detecting other JetBots).

### Checkpoints

1. A successful run-through of the race.

## Post-processing

The teams read (subscribe) the data from `lab5/race/path` and visualize it. 
(To be completed by Mudit)



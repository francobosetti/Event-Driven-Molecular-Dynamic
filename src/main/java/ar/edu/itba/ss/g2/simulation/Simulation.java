package ar.edu.itba.ss.g2.simulation;

import ar.edu.itba.ss.g2.model.Particle;

import java.util.*;

import ar.edu.itba.ss.g2.simulation.events.*;

public class Simulation {

    private final List<Set<Particle>> snapshots;


    public Simulation(Set<Particle> particles) {
        this.snapshots = new ArrayList<>();
        this.snapshots.add(particles);
    }

    public void run(int steps) {
        // begin calculating all posible collitions
        Set<Particle> particles = snapshots.get(0);
        // begin queue ordered by time before crash
        PriorityQueue<Event> collitionEventQueue = new PriorityQueue<>();
        for(Particle p1 : particles) {
            // TODO: square at the moment, should support both configurations ( square and circle )
            // TODO: fixed obstacle collition
            Double time = collidesWithHorizontalWall(p1);
            if(time != null) {
                collitionEventQueue.add(new HorizontalWallEvent(time, p1));
            }
            time = collidesWithVerticalWall(p1);
            if(time != null) {
                collitionEventQueue.add(new VerticalWallEvent(time, p1));
            }
            for (Particle p2 : particles) {
                time = collidesWithParticle(p1, p2);
                if(time != null) {
                    collitionEventQueue.add(new TwoParticleEvent(time, p1, p2));
                }
            }
        }


        // TODO: dequeue, update state, recalculate collitions for dequeued particle, etc

        for(int i = 0; i < steps; i++) {
            Event event = collitionEventQueue.poll();
            if(event == null) {
                break;
            }

            if(event.isInvalid()) {
                continue;
            }
            event.resolveCollision();

            // TODO: i need the involved particle / particles to propperly update the list

        }

    }

    public List<Set<Particle>> getSnapshots() {
        return snapshots;
    }

    private Double timeToLinearWallCollision(double v, double radius, double position) {
        if (v == 0) {
            return null;
        }

        double distance;

        if (v > 0) {
            distance = boxSide - position - radius;
        } else {
            distance = position - radius;
        }

        return distance / Math.abs(v);
    }

    public Double timeToHorizontalWallCollision(Particle p1) {
        return timeToLinearWallCollision(p1.getVy(), p1.getRadius(), p1.getY());
    }

    public Double timeToVerticalWallCollision(Particle p1) {
        return timeToLinearWallCollision(p1.getVx(), p1.getRadius(), p1.getX());
    }

    public Double timeToParticleCollision(Particle p1, Particle p2) {
        Double deltaVelX = p2.getVx() - p1.getVx();
        Double deltaVelY = p2.getVy() - p1.getVy();

        Double deltaPosX = p2.getX() - p1.getX();
        Double deltaPosY = p2.getY() - p1.getY();

        double deltaVelPos = deltaVelX * deltaPosX + deltaVelY * deltaPosY;

        if (deltaVelPos >= 0) {
            return null;
        }

        double deltaVelVel = deltaVelX * deltaVelX + deltaVelY * deltaVelY;
        double deltaPosPos = deltaPosX * deltaPosX + deltaPosY * deltaPosY;

        double radiusSquared =
                (p1.getX() - p2.getX()) * (p1.getX() - p2.getX())
                        + (p1.getY() - p2.getY()) * (p1.getY() - p2.getY());
        double d = deltaVelPos * deltaVelPos - (deltaVelVel * (deltaPosPos - radiusSquared));

        if (d < 0) {
            return null;
        }

        return -(deltaVelPos + Math.sqrt(d)) / (deltaVelVel);
    }
}

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

    public void run() {
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

    }

    public List<Set<Particle>> getSnapshots() {
        return snapshots;
    }

    private static Double collidesWithLinearWall(double v, double radius, double axisPosition, double axisUpperBoundry) {
        if(v == 0) return null;
        if(v < 0) {
            return (radius - axisPosition) / v;
        }
        return (axisUpperBoundry - radius - axisPosition) / v;
    }

    public static Double collidesWithHorizontalWall(Particle p1) {
        // TODO: add upper boundry, should be the vertical dimension of the box
        return collidesWithLinearWall(p1.getVy(), p1.getRadius(), p1.getY(), 0);
    }

    public static Double collidesWithVerticalWall(Particle p1) {
        // TODO: add upper boundry, should be the hotizontal dimension of the box
        return collidesWithLinearWall(p1.getVx(), p1.getRadius(), p1.getX(), 0);
    }

    public static Double collidesWithParticle(Particle p1, Particle p2) {
        Double deltaVelX = p2.getVx() - p1.getVx();
        Double deltaVely = p2.getVy() - p1.getVy();

        Double deltaPosX = p2.getX() - p1.getX();
        Double deltaPosY = p2.getY() - p1.getY();

        double deltaVelPos = deltaVelX * deltaPosX + deltaVely * deltaPosY;

        if (deltaVelPos >= 0) {
            return null;
        }

        double deltaVelVel = deltaVelX * deltaVelX + deltaVely * deltaVely;
        double deltaPosPos = deltaPosX * deltaPosX + deltaPosY * deltaPosY;

        double radiusSquared = (p1.getX() - p2.getX()) * (p1.getX() - p2.getX()) + (p1.getY() - p2.getY()) * (p1.getY() - p2.getY());
        double d = deltaVelPos * deltaVelPos - (deltaVelVel * (deltaPosPos - radiusSquared));

        if (d<0) {
            return null;
        }

        return -(deltaVelPos + Math.sqrt(d))/(deltaVelVel);
    }
}

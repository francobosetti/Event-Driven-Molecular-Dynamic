package ar.edu.itba.ss.g2.simulation;

import ar.edu.itba.ss.g2.model.Particle;
import ar.edu.itba.ss.g2.simulation.events.*;

import java.util.ArrayList;
import java.util.List;
import java.util.PriorityQueue;
import java.util.Set;
import java.util.stream.Collectors;

public class Simulation {

    private final List<Set<Particle>> snapshots;
    private final Set<Particle> particles;
    private final PriorityQueue<Event> collisionEventQueue;

    private final double boxSide;

    public Simulation(Set<Particle> particles, double boxSide) {
        this.particles = particles;
        this.boxSide = boxSide;

        this.snapshots = new ArrayList<>();
        this.collisionEventQueue = new PriorityQueue<>();
    }

    public void run(double maxTime) {

        // Save initial state
        saveSnapshot();

        // Load initial collisions
        for (Particle p1 : particles) {
            addParticleCollisions(p1);
        }

        double currentTime = 0;
        while (currentTime < maxTime) {
            Event event = collisionEventQueue.poll();

            // TODO: maybe unnecesary?
            if (event == null) {
                break;
            }

            if (event.isInvalid()) {
                continue;
            }

            double eventTime = event.getTime();
            double timeDiff = eventTime - currentTime;

            // Advance particles
            for (Particle particle : particles) {
                particle.setX(particle.getX() + particle.getVx() * timeDiff);
                particle.setY(particle.getY() + particle.getVy() * timeDiff);
            }

            event.resolveCollision();

            // Recalculate future collisions
            // TODO: refactor this aberracion absoluta
            if (event instanceof TwoParticleEvent twoParticleEvent) {
                Particle particleA = twoParticleEvent.getParticleA();
                Particle particleB = twoParticleEvent.getParticleB();

                addParticleCollisions(particleA);
                addParticleCollisions(particleB);

            } else if (event instanceof OneParticleEvent oneParticleEvent) {
                Particle particle = oneParticleEvent.getParticle();

                addParticleCollisions(particle);
            }

            // Save snapshot
            saveSnapshot();

            currentTime = eventTime;
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

    // TODO: Add obstacle and circular wall collisions
    public void addParticleCollisions(Particle particle) {

        Double time = timeToHorizontalWallCollision(particle);
        if (time != null) {
            collisionEventQueue.add(new HorizontalWallEvent(time, particle));
        }

        time = timeToVerticalWallCollision(particle);
        if (time != null) {
            collisionEventQueue.add(new VerticalWallEvent(time, particle));
        }

        for (Particle p2 : particles) {
            time = timeToParticleCollision(particle, p2);
            if (time != null) {
                collisionEventQueue.add(new TwoParticleEvent(time, particle, p2));
            }
        }
    }

    private void saveSnapshot() {
        Set<Particle> particlesCopy = particles.stream().map(Particle::new).collect(Collectors.toSet());
        snapshots.add(particlesCopy);
    }
}

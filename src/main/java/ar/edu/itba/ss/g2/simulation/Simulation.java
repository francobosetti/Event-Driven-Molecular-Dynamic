package ar.edu.itba.ss.g2.simulation;

import ar.edu.itba.ss.g2.model.Particle;
import ar.edu.itba.ss.g2.simulation.events.*;

import java.util.HashMap;
import java.util.Map;
import java.util.PriorityQueue;
import java.util.Set;
import java.util.stream.Collectors;

public class Simulation {

    private final Map<Double, Set<Particle>> snapshots;
    private final Set<Particle> particles;
    private final PriorityQueue<Event> collisionEventQueue;

    private final double boxSide;

    public Simulation(Set<Particle> particles, double boxSide) {
        this.particles = particles;
        this.boxSide = boxSide;

        this.snapshots = new HashMap<>();
        this.collisionEventQueue = new PriorityQueue<>();
    }

    public void run(double maxTime) {

        // Save initial state
        saveSnapshot(0);

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
            saveSnapshot(currentTime);

            currentTime += eventTime;
        }
    }

    public Map<Double, Set<Particle>> getSnapshots() {
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

    private Double timeToHorizontalWallCollision(Particle p1) {
        return timeToLinearWallCollision(p1.getVy(), p1.getRadius(), p1.getY());
    }

    private Double timeToVerticalWallCollision(Particle p1) {
        return timeToLinearWallCollision(p1.getVx(), p1.getRadius(), p1.getX());
    }

    private Double timeToParticleCollision(Particle p1, Particle p2) {
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

    private Double timeToCircularWallCollision(Particle p1) {
        if(p1.getVx() == 0 && p1.getVy() == 0) {
            return null;
        }

        // TODO: add propper radius
        double circularWallRadius = 2;
        // TODO: this
        if(p1.getVx() == 0) {
            return null;
        }
        // TODO: this
        if(p1.getVy() == 0) {
            return null;
        }
        double frac = p1.getVy()/p1.getVx();
        double x0 = p1.getX();
        double y0 = p1.getY();
        double radius = p1.getRadius();
        double a = 1 + frac*frac;
        double b = 2*frac*(y0-frac*x0);
        double c = (y0 - x0*frac)*(y0 - x0*frac) - (circularWallRadius - radius)*(circularWallRadius - radius);

        double d = Math.sqrt(b*b - 4*a*c);

        double x = (-b * Math.signum(p1.getVx())*d)/(2*a);

        return (x-x0) / p1.getVx();
    }

    // TODO: Add obstacle and circular wall collisions
    private void addParticleCollisions(Particle particle) {

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

    private void saveSnapshot(double time) {
        Set<Particle> particlesCopy =
                particles.stream().map(Particle::new).collect(Collectors.toSet());
        snapshots.put(time, particlesCopy);
    }
}

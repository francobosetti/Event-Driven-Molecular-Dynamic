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

    private double currentTime;

    private final double obstacleRadius;
    private final double obstacleCenter;
    private final boolean hasObstacle;

    private final double domainSize;
    private final boolean isCircularDomain;

    public Simulation(
            Set<Particle> particles,
            double domainSize,
            boolean isCircularDomain,
            double obstacleRadius) {
        this.particles = particles;
        this.domainSize = domainSize;
        this.isCircularDomain = isCircularDomain;

        this.obstacleRadius = obstacleRadius;
        this.obstacleCenter = isCircularDomain ? 0 : domainSize / 2;
        this.hasObstacle = true;

        this.currentTime = 0;

        this.snapshots = new HashMap<>();
        this.collisionEventQueue = new PriorityQueue<>();
    }

    public Simulation(Set<Particle> particles, double domainSize, boolean isCircularDomain) {
        this.particles = particles;
        this.domainSize = domainSize;
        this.isCircularDomain = isCircularDomain;

        this.hasObstacle = false;
        this.obstacleCenter = isCircularDomain ? 0 : domainSize / 2;
        this.obstacleRadius = 0;

        this.currentTime = 0;

        this.snapshots = new HashMap<>();
        this.collisionEventQueue = new PriorityQueue<>();
    }

    public void run(long maxEvents) {

        // Save initial state
        saveSnapshot(0);

        // Load initial collisions
        for (Particle p1 : particles) {
            addParticleCollisions(p1);
        }

        long eventCount = 0;

        while (eventCount < maxEvents) {
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

            currentTime = eventTime;

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

            eventCount++;
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
            distance = domainSize - position - radius;
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
                (p1.getRadius() + p2.getRadius()) * (p1.getRadius() + p2.getRadius());

        double d = deltaVelPos * deltaVelPos - (deltaVelVel * (deltaPosPos - radiusSquared));

        if (d < 0) {
            return null;
        }

        return -(deltaVelPos + Math.sqrt(d)) / (deltaVelVel);
    }

    private Double timeToObstacleCollision(Particle p1) {
        // TODO: medio feo
        Particle obstacle =
                new Particle(0, obstacleCenter, obstacleCenter, 0.0, 0.0, obstacleRadius, 0.0);

        return timeToParticleCollision(p1, obstacle);
    }

    private Double timeToCircularWallCollision(Particle p1) {
        if (p1.getVx() == 0 && p1.getVy() == 0) {
            return null;
        }

        double dr = (domainSize - p1.getRadius());
        double x0 = p1.getX();
        double y0 = p1.getY();

        double vx = p1.getVx();
        double vy = p1.getVy();

        double a = vx*vx + vy*vy;
        double b = 2*(x0*vx + y0*vy);
        double c = x0*x0 + y0*y0 - dr*dr;
        double d = Math.sqrt(b*b-4*a*c);
        return (-b+d)/(2*a);
    }

    // TODO: Add  circular wall collisions
    private void addParticleCollisions(Particle particle) {

        Double time;
        if (isCircularDomain) {
            time = timeToCircularWallCollision(particle);
            if (time != null) {
                collisionEventQueue.add(new CircularWallEvent(currentTime + time, particle));
            }

        } else {
            time = timeToHorizontalWallCollision(particle);
            if (time != null) {
                collisionEventQueue.add(new HorizontalWallEvent(currentTime + time, particle));
            }

            time = timeToVerticalWallCollision(particle);
            if (time != null) {
                collisionEventQueue.add(new VerticalWallEvent(currentTime + time, particle));
            }
        }

        if (hasObstacle) {
            time = timeToObstacleCollision(particle);
            if (time != null) {
                collisionEventQueue.add(
                        new ObstacleEvent(
                                currentTime + time, particle, obstacleCenter, obstacleCenter));
            }
        }

        for (Particle p2 : particles) {

            if (p2.equals(particle)) {
                continue;
            }

            time = timeToParticleCollision(particle, p2);
            if (time != null) {
                collisionEventQueue.add(new TwoParticleEvent(currentTime + time, particle, p2));
            }
        }
    }

    private void saveSnapshot(double time) {
        Set<Particle> particlesCopy =
                particles.stream().map(Particle::new).collect(Collectors.toSet());
        snapshots.put(time, particlesCopy);
    }
}

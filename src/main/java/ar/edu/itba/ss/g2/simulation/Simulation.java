package ar.edu.itba.ss.g2.simulation;

import ar.edu.itba.ss.g2.model.Particle;
import ar.edu.itba.ss.g2.simulation.events.*;

import java.util.HashMap;
import java.util.LinkedList;
import java.util.List;
import java.util.Map;
import java.util.PriorityQueue;
import java.util.Set;

import java.util.stream.Collectors;

public class Simulation {

    private final Map<Double, Set<Particle>> snapshots;
    private final List<Event> events;

    private final Particle[] particles;
    private final PriorityQueue<Event> collisionEventQueue;


    private double currentTime;

    private final double obstacleCenter;
    private final boolean hasObstacle;
    private final Particle obstacle;

    private final double domainSize;
    private final boolean isCircularDomain;

    public Simulation(
            Set<Particle> particles,
            double domainSize,
            boolean isCircularDomain,
            double obstacleRadius) {

        this.particles = new Particle[particles.size()];

        for (Particle particle : particles) {
            this.particles[particle.getId()] = particle;
        }

        this.domainSize = domainSize;
        this.isCircularDomain = isCircularDomain;

        this.obstacleCenter = isCircularDomain ? 0 : domainSize / 2;
        this.hasObstacle = true;
        this.obstacle = new Particle(0, obstacleCenter, obstacleCenter, 0.0, 0.0, obstacleRadius, 0.0);

        this.currentTime = 0;

        this.snapshots = new HashMap<>();
        this.collisionEventQueue = new PriorityQueue<>();
        this.events = new LinkedList<>();
    }

    public Simulation(Set<Particle> particles, double domainSize, boolean isCircularDomain) {

        this.particles = new Particle[particles.size()];

        for (Particle particle : particles) {
            this.particles[particle.getId()] = particle;
        }

        this.domainSize = domainSize;
        this.isCircularDomain = isCircularDomain;

        this.hasObstacle = false;
        this.obstacle = null;

        this.obstacleCenter = isCircularDomain ? 0 : domainSize / 2;

        this.currentTime = 0;

        this.snapshots = new HashMap<>();
        this.collisionEventQueue = new PriorityQueue<>();
        this.events = new LinkedList<>();
    }

    public void run(double maxTime, int skipEvents) {

        // Save initial state
        saveSnapshot(0);

        // Load initial collisions
        for (Particle p1 : particles) {
            addParticleCollisions(p1);
        }

        int skipCounter = 0;

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

            currentTime = eventTime;

            event.resolveCollision();

            // Recalculate future collisions
            for (Particle p : event.getParticles()) {
                addParticleCollisions(p);
            }

            skipCounter++;
            if (skipCounter == skipEvents) {
                skipCounter = 0;

                // Save snapshot
                saveSnapshot(currentTime);
            }

            events.add(event.copy());
        }
    }

    public Map<Double, Set<Particle>> getSnapshots() {
        return snapshots;
    }

    public List<Event> getEvents() {
        return events;
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
        return timeToParticleCollision(p1, this.obstacle);
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

        double a = vx * vx + vy * vy;
        double b = 2 * (x0 * vx + y0 * vy);
        double c = x0 * x0 + y0 * y0 - dr * dr;
        double d = Math.sqrt(b * b - 4 * a * c);
        return (-b + d) / (2 * a);
    }

    private boolean collitionIsInsideDomain(double time, Particle particle) {
        double fx = particle.getX() + particle.getVx() * time;
        double fy = particle.getY() + particle.getVy() * time;

        
        if(isCircularDomain) {
            return domainSize*domainSize >= (fx*fx + fy*fy); 
        }

        return (fx > 0 && fx < domainSize && fy > 0 && fy < domainSize); 
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
            if (time != null && collitionIsInsideDomain(time, particle)) {
                collisionEventQueue.add(new HorizontalWallEvent(currentTime + time, particle));
            }

            time = timeToVerticalWallCollision(particle);
            if (time != null && collitionIsInsideDomain(time, particle)) {
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
            if (time != null && collitionIsInsideDomain(time, particle)) {
                collisionEventQueue.add(new TwoParticleEvent(currentTime + time, particle, p2));
            }
        }
    }

    private void saveSnapshot(double time) {
        Set<Particle> particlesCopy =
                Set.of(particles).stream().map(Particle::new).collect(Collectors.toSet());
        snapshots.put(time, particlesCopy);
    }
}

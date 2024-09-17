package ar.edu.itba.ss.g2.simulation;

import ar.edu.itba.ss.g2.model.Particle;
import ar.edu.itba.ss.g2.simulation.events.*;

import java.util.HashMap;
import java.util.Map;
import java.util.PriorityQueue;
import java.util.Set;
import java.util.function.BiPredicate;
import java.util.function.Predicate;
import java.util.stream.Collectors;

public class Simulation {

    private final Map<Double, Set<Particle>> snapshots;
    private final Particle[] particles;
    private Particle[] previousParticles;
    private final PriorityQueue<Event> collisionEventQueue;

    private double currentTime;
    private double previousTime;

    private final double obstacleRadius;
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
        this.previousParticles = new Particle[particles.size()];

        for (Particle particle : particles) {
            this.particles[particle.getId()] = particle;
            this.previousParticles[particle.getId()] = new Particle(particle);
        }

        this.domainSize = domainSize;
        this.isCircularDomain = isCircularDomain;

        this.obstacleRadius = obstacleRadius;
        this.obstacleCenter = isCircularDomain ? 0 : domainSize / 2;
        this.hasObstacle = true;
        this.obstacle = new Particle(0, obstacleCenter, obstacleCenter, 0.0, 0.0, obstacleRadius, 0.0);

        this.currentTime = 0;
        this.previousTime = 0;

        this.snapshots = new HashMap<>();
        this.collisionEventQueue = new PriorityQueue<>();
    }

    public Simulation(Set<Particle> particles, double domainSize, boolean isCircularDomain) {

        this.particles = new Particle[particles.size()];
        this.previousParticles = new Particle[particles.size()];

        for (Particle particle : particles) {
            this.particles[particle.getId()] = particle;
            this.previousParticles[particle.getId()] = new Particle(particle);
        }

        this.domainSize = domainSize;
        this.isCircularDomain = isCircularDomain;

        this.hasObstacle = false;
        this.obstacle = null;

        this.obstacleCenter = isCircularDomain ? 0 : domainSize / 2;
        this.obstacleRadius = 0;

        this.currentTime = 0;
        this.previousTime = 0;

        this.snapshots = new HashMap<>();
        this.collisionEventQueue = new PriorityQueue<>();
    }

    public void run(double maxTime, int skipEvents) {

        // Save initial state
        saveSnapshot(0, 0, skipEvents);

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


            previousTime = currentTime;
            // Set previous particles speed and position with current particles
            // This has to be done without creating a new object as garbage collection will suffer
            for (int i = 0; i < particles.length; i++) {
                Particle previousParticle = previousParticles[i];
                Particle currentParticle = particles[i];

                previousParticle.setVx(currentParticle.getVx());
                previousParticle.setVy(currentParticle.getVy());
                previousParticle.setX(currentParticle.getX());
                previousParticle.setY(currentParticle.getY());
            }
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
            double r = domainSize - particle.getRadius();
            return r*r >= (fx*fx + fy*fy); 
        }

        double r = particle.getRadius();
        return (fx > r && fx < domainSize-r && fy > r && fy < domainSize-r); 
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

    private void saveSnapshot(double previousTime, double time, int skipEvents) {
        Set<Particle> particlesCopy =
                Set.of(particles).stream().map(Particle::new).collect(Collectors.toSet());
        snapshots.put(time, particlesCopy);

        if (previousTime != currentTime && skipEvents > 1) {
            Set<Particle> previousParticlesCopy =
                    Set.of(previousParticles).stream().map(Particle::new).collect(Collectors.toSet());
            snapshots.put(previousTime, previousParticlesCopy);
        }
    }
}

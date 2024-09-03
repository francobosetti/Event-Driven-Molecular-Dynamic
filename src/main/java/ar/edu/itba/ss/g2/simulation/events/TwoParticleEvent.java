package ar.edu.itba.ss.g2.simulation.events;

import ar.edu.itba.ss.g2.model.Particle;

public class TwoParticleEvent extends Event {
    private final Particle a;
    private final int collisionCountA;
    private final Particle b;
    private final int collisionCountB;

    public TwoParticleEvent(
            double time, Particle a, Particle b) {
        super(time);
        this.a = a;
        this.collisionCountA = a.getCollisionCount();
        this.b = b;
        this.collisionCountB = b.getCollisionCount();
    }

    // return the first particle
    public Particle getParticleA() {
        return a;
    }

    // return the second particle
    public Particle getParticleB() {
        return b;
    }

    @Override
    public boolean isInvalid() {
        return a.getCollisionCount() != collisionCountA || b.getCollisionCount() != collisionCountB;
    }

    @Override
    public void resolveCollision() {
        // center-to-center distance (sigma) between the two particles
        double sigma =
                Math.sqrt(Math.pow(b.getX() - a.getX(), 2) + Math.pow(b.getY() - a.getY(), 2));

        // relative velocity vector (delta v) between the two particles
        double dvx = b.getVx() - a.getVx();
        double dvy = b.getVy() - a.getVy();

        // relative position vector (delta r) between the two particles
        double dx = b.getX() - a.getX();
        double dy = b.getY() - a.getY();

        // Cross product of the relative position vector and the relative velocity vector
        double dvdr = dvx * dx + dvy * dy;

        // Impulse magnitude
        double j = (2 * a.getMass() * b.getMass() * dvdr) / (sigma * (a.getMass() + b.getMass()));

        // Impulse vector
        double jx = (j * dx) / sigma;
        double jy = (j * dy) / sigma;

        // Update particle velocities (newtons second law)
        double newVax = a.getVx() + jx / a.getMass();
        double newVay = a.getVy() + jy / a.getMass();

        a.setVx(newVax);
        a.setVy(newVay);

        double newVbx = b.getVx() - jx / b.getMass();
        double newVby = b.getVy() - jy / b.getMass();

        b.setVx(newVbx);
        b.setVy(newVby);

        a.incrementCollisionCount();
        b.incrementCollisionCount();
    }
}

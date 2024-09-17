package ar.edu.itba.ss.g2.simulation.events;

import ar.edu.itba.ss.g2.model.Particle;

public class TwoParticleEvent extends Event {
    private final int collisionCountA;
    private final int collisionCountB;

    public TwoParticleEvent(double time, Particle a, Particle b) {
        super(time, new Particle[]{a, b});
        this.collisionCountA = a.getCollisionCount();
        this.collisionCountB = b.getCollisionCount();
    }

    @Override
    public boolean isInvalid() {
        Particle a = getParticles()[0];
        Particle b = getParticles()[1];

        return a.getCollisionCount() != collisionCountA || b.getCollisionCount() != collisionCountB;
    }

    @Override
    public void resolveCollision() {
        Particle a = getParticles()[0];
        Particle b = getParticles()[1];

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

    @Override
    public String toString() {
        Particle a = getParticles()[0];
        Particle b = getParticles()[1];

        return String.format(
                "%.5f P %d %5f %5f %5f %5f %d %5f %5f %5f %5f",
                getTime(), a.getId(), a.getX(), a.getY(), a.getVx(), a.getVy(), b.getId(), b.getX(),
                b.getY(), b.getVx(), b.getVy());
    }

    @Override
    public Event copy() {
        Particle a = getParticles()[0];
        Particle b = getParticles()[1];

        return new TwoParticleEvent(getTime(), new Particle(a), new Particle(b));
    }
}

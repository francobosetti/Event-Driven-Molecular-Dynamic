package ar.edu.itba.ss.g2.simulation.events;

import ar.edu.itba.ss.g2.model.Particle;

public abstract class OneParticleEvent extends Event {
    protected final Particle particle;
    protected final int collisionCount;

    public OneParticleEvent(double time, Particle particle) {
        super(time);
        this.particle = particle;
        this.collisionCount = particle.getCollisionCount();
    }

    public Particle getParticle() {
        return particle;
    }

    @Override
    public boolean isInvalid() {
        return particle.getCollisionCount() != collisionCount;
    }
}

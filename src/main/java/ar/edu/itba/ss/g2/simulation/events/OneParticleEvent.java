package ar.edu.itba.ss.g2.simulation.events;

import ar.edu.itba.ss.g2.model.Particle;

public abstract class OneParticleEvent extends Event {
    protected final int collisionCount;

    public OneParticleEvent(double time, Particle particle) {
        super(time, new Particle[]{particle});
        this.collisionCount = particle.getCollisionCount();
    }

    @Override
    public boolean isInvalid() {
        Particle particle = getParticles()[0];
        return particle.getCollisionCount() != collisionCount;
    }
}

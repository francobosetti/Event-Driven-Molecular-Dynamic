package ar.edu.itba.ss.g2.simulation.events;

import ar.edu.itba.ss.g2.model.Particle;

public abstract class WallEvent extends Event {
    protected final Particle particle;
    protected final int collisionCount;


    public WallEvent(double time, Particle particle) {
        super(time);
        this.particle = particle;
        this.collisionCount = particle.getCollisionCount();
    }

    @Override
    public boolean wasSuperveningEvent() {
        return particle.getCollisionCount() != collisionCount;
    }
}

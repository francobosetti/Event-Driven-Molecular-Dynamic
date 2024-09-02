package ar.edu.itba.ss.g2.model.Events;

import ar.edu.itba.ss.g2.model.Particle;

abstract class WallEvent extends Event {
    private final Particle particle;
    private final int collisionCount;

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

package ar.edu.itba.ss.g2.simulation.events;

import ar.edu.itba.ss.g2.model.Particle;

public class VerticalWallEvent extends OneParticleEvent {
    public VerticalWallEvent(double time, Particle particle) {
        super(time, particle);
    }

    @Override
    public void resolveCollision() {
        double vx = particle.getVx();
        particle.setVx(-vx);

        particle.incrementCollisionCount();
    }
}

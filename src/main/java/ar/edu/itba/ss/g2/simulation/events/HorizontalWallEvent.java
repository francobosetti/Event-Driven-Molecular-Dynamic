package ar.edu.itba.ss.g2.simulation.events;

import ar.edu.itba.ss.g2.model.Particle;

public class HorizontalWallEvent extends OneParticleEvent {
    public HorizontalWallEvent(double time, Particle particle) {
        super(time, particle);
    }

    @Override
    public void resolveCollision() {
        Particle particle = getParticles()[0];
        double vy = particle.getVy();
        particle.setVy(-vy);

        particle.incrementCollisionCount();
    }
}

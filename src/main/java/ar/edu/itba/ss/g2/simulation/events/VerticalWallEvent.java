package ar.edu.itba.ss.g2.simulation.events;

import ar.edu.itba.ss.g2.model.Particle;

public class VerticalWallEvent extends OneParticleEvent {
    public VerticalWallEvent(double time, Particle particle) {
        super(time, particle);
    }

    @Override
    public void resolveCollision() {
        Particle particle = getParticles()[0];
        previousVx = particle.getVx();
        previousVy = particle.getVy();

        double vx = particle.getVx();
        particle.setVx(-vx);

        particle.incrementCollisionCount();
    }

    @Override
    public String toString() {
        Particle particle = getParticles()[0];

        return String.format(
                "%.5f W %d %5f %5f %5f %5f %5f %5f",
                getTime(),
                particle.getId(),
                particle.getX(),
                particle.getY(),
                particle.getVx(),
                particle.getVy(),
                previousVx,
                previousVy
        );
    }

    @Override
    public Event copy() {
        Particle particle = getParticles()[0];
        OneParticleEvent resp =  new CircularWallEvent(getTime(), new Particle(particle));

        resp.previousVx = previousVx;
        resp.previousVy = previousVy;

        return resp;
    }
}

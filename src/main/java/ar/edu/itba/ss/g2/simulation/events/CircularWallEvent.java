package ar.edu.itba.ss.g2.simulation.events;

import ar.edu.itba.ss.g2.model.Particle;

public class CircularWallEvent extends OneParticleEvent {
    public CircularWallEvent(double time, Particle particle) {
        super(time, particle);
    }

    @Override
    public void resolveCollision() {

        // alpha: angle between the normal and the x-axis
        // the position versor is the same as the normal versor
        double x = particle.getX();
        double y = particle.getY();

        double alpha = Math.atan2(y, x);

        // Decompose the velocity vector in normal and tangential components
        double vNormal = particle.getVx() * Math.cos(alpha) + particle.getVy() * Math.sin(alpha);
        double vTangential =
                -particle.getVx() * Math.sin(alpha) + particle.getVy() * Math.cos(alpha);

        // Invert the normal component
        vNormal = -vNormal;

        // Recompose the velocity vector
        double newVx = vNormal * Math.cos(alpha) - vTangential * Math.sin(alpha);
        double newVy = vNormal * Math.sin(alpha) + vTangential * Math.cos(alpha);

        particle.setVx(newVx);
        particle.setVy(newVy);

        particle.incrementCollisionCount();
    }
}

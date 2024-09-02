package ar.edu.itba.ss.g2.simulation.events;

import ar.edu.itba.ss.g2.model.Particle;

public class ObstacleEvent extends OneParticleEvent {

    private final double obstacleX;
    private final double obstacleY;

    public ObstacleEvent(double time, Particle particle, double obstacleX, double obstacleY) {
        super(time, particle);
        this.obstacleX = obstacleX;
        this.obstacleY = obstacleY;
    }

    @Override
    public void resolveCollision() {

        double x = particle.getX();
        double y = particle.getY();

        double dx = x - obstacleX;
        double dy = y - obstacleY;

        // alpha: angle between the normal and the x-axis
        // the versor between the particle and the obstacle center is the same as the normal versor
        double alpha = Math.atan2(dy, dx);

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

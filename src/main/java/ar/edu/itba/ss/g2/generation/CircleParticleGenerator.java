package ar.edu.itba.ss.g2.generation;

import java.util.ArrayList;
import java.util.List;
import java.util.Random;

import ar.edu.itba.ss.g2.model.Particle;

public class CircleParticleGenerator extends ParticleGenerator {

    private final double domainRadius;

    public CircleParticleGenerator(
            double domainRadius,
            int particleCount,
            double particleRadius,
            double particleMass,
            double initialVelocity,
            Random random) {
        super(particleCount, particleRadius, particleMass, initialVelocity, random);
        this.domainRadius = domainRadius;
    }

    @Override
    public List<Particle> generate() {
        List<Particle> particles = new ArrayList<>(particleCount);

        for (int i = 0; i < particleCount; i++) {
            
            // Coords. polares
            double positionAngle = random.nextDouble() * 2 * Math.PI;
            double positionRadius = random.nextDouble() * domainRadius;

            double x = positionRadius * Math.cos(positionAngle);
            double y = positionRadius * Math.sin(positionAngle);

            double velocityAngle = random.nextDouble() * 2 * Math.PI;
            double vx = initialVelocity * Math.cos(velocityAngle);
            double vy = initialVelocity * Math.sin(velocityAngle);

            particles.add(new Particle(x, y, vx, vy, particleMass, particleRadius));

        }

        return particles;
    }
}

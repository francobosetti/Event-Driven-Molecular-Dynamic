package ar.edu.itba.ss.g2.generation;

import ar.edu.itba.ss.g2.model.Particle;

import java.util.ArrayList;
import java.util.List;
import java.util.Random;

public class CircleParticleGenerator extends ParticleGenerator {

    private final double domainRadius;

    public CircleParticleGenerator(
            double domainRadius,
            int particleCount,
            double particleRadius,
            double particleMass,
            double initialVelocity,
            double obstacleRadius,
            Random random) {
        super(particleCount, particleRadius, particleMass, initialVelocity, obstacleRadius, random);
        this.domainRadius = domainRadius;
    }

    @Override
    public List<Particle> generate() {
        List<Particle> particles = new ArrayList<>(particleCount);

        for (int i = 0, tries = 0; i < particleCount; i++, tries++) {

            if (tries > MAX_TRIES) {
                throw new IllegalStateException("Could not generate particles without overlaps");
            }

            // Coords. polares
            double positionAngle = random.nextDouble() * 2 * Math.PI;
            double positionRadius =
                    Math.sqrt(random.nextDouble()) * (domainRadius - 2 * particleRadius - obstacleRadius)
                            + particleRadius
                            + obstacleRadius;

            double x = positionRadius * Math.cos(positionAngle);
            double y = positionRadius * Math.sin(positionAngle);

            double velocityAngle = random.nextDouble() * 2 * Math.PI;
            double vx = initialVelocity * Math.cos(velocityAngle);
            double vy = initialVelocity * Math.sin(velocityAngle);

            Particle particle = new Particle(i, x, y, vx, vy, particleRadius, particleMass);

            if (particles.stream().anyMatch(p -> p.overlaps(particle))) {
                i--;
                continue;
            }

            particles.add(particle);
        }

        return particles;
    }
}

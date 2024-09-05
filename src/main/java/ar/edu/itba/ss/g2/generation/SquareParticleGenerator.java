package ar.edu.itba.ss.g2.generation;

import java.util.ArrayList;
import java.util.List;
import java.util.Random;

import ar.edu.itba.ss.g2.model.Particle;

public class SquareParticleGenerator extends ParticleGenerator {

    private final double domainSide;

    public SquareParticleGenerator(
            double domainSide,
            int particleCount,
            double particleRadius,
            double particleMass,
            double initialVelocity,
            Random random) {
        super(particleCount, particleRadius, particleMass, initialVelocity, random);
        this.domainSide = domainSide;
    }

    @Override
    public List<Particle> generate() {
        List<Particle> particles = new ArrayList<>(particleCount);

        for (int i = 0, tries = 0; i < particleCount; i++, tries++) {

            if (tries > MAX_TRIES) {
                throw new IllegalStateException("Could not generate particles without overlaps");
            }

            double x = random.nextDouble() * (domainSide - 2 * particleRadius) + particleRadius;
            double y = random.nextDouble() * (domainSide - 2 * particleRadius) + particleRadius;
            
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

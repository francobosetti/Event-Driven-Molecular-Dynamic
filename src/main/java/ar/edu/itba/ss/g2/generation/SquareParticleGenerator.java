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

        for (int i = 0; i < particleCount; i++) {
            double x = random.nextDouble() * domainSide;
            double y = random.nextDouble() * domainSide;
            
            double velocityAngle = random.nextDouble() * 2 * Math.PI;

            double vx = initialVelocity * Math.cos(velocityAngle);
            double vy = initialVelocity * Math.sin(velocityAngle);

            particles.add(new Particle(i, x, y, vx, vy, particleRadius, particleMass));
        }

        return particles;
    }
}

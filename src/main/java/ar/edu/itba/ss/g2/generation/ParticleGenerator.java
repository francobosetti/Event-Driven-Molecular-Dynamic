package ar.edu.itba.ss.g2.generation;

import ar.edu.itba.ss.g2.model.Particle;

import java.util.List;
import java.util.Random;

public abstract class ParticleGenerator {

    protected static final long MAX_TRIES = 10_000_000L;

    protected final int particleCount;
    protected final double particleRadius;
    protected final double particleMass;
    protected final double initialVelocity;
    protected final double obstacleRadius;
    protected final Random random;

    protected ParticleGenerator(
            int particleCount,
            double particleRadius,
            double particleMass,
            double initialVelocity,
            double obstacleRadius,
            Random random) {
        this.particleCount = particleCount;
        this.particleRadius = particleRadius;
        this.particleMass = particleMass;
        this.initialVelocity = initialVelocity;
        this.obstacleRadius = obstacleRadius;
        this.random = random;
    }

    public abstract List<Particle> generate();
}

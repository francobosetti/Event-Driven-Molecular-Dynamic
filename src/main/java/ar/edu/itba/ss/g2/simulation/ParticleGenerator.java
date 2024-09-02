package ar.edu.itba.ss.g2.simulation;

import ar.edu.itba.ss.g2.model.Particle;

import java.util.ArrayList;
import java.util.List;
import java.util.Random;

public class ParticleGenerator {

    private final int particleAmount;

    private final Random random;

    public ParticleGenerator(int particleAmount, int seed) {
        this.particleAmount = particleAmount;
        this.random = new Random(seed);
    }

    public List<Particle> generate() {
        List<Particle> particles = new ArrayList<>(particleAmount);

        for (long i = 0; i < particleAmount; i++) {
            particles.add(new Particle());
        }

        return particles;
    }
}

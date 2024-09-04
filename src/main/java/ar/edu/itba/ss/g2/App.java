package ar.edu.itba.ss.g2;

import ar.edu.itba.ss.g2.config.ArgParser;
import ar.edu.itba.ss.g2.config.Configuration;
import ar.edu.itba.ss.g2.generation.ParticleGenerator;
import ar.edu.itba.ss.g2.generation.CircleParticleGenerator;
import ar.edu.itba.ss.g2.generation.SquareParticleGenerator;
import ar.edu.itba.ss.g2.model.Particle;
import ar.edu.itba.ss.g2.simulation.Simulation;

import java.util.HashSet;
import java.util.List;
import java.util.Random;
import java.util.stream.Collectors;

public class App {
    public static void main(String[] args) {

        ArgParser parser = new ArgParser(args);
        Configuration configuration = parser.parse();

        if (configuration == null) {
            parser.printHelp();
            System.exit(1);
        }

        // Generate particles
        int particleCount = configuration.getParticleCount();
        double particleRadius = configuration.getParticleRadius();
        double particleMass = configuration.getParticleMass();
        double initialVelocity = configuration.getInitialVelocity();
        Random random = configuration.getRandom();

        ParticleGenerator generator;

        if (configuration.isDomainCircular()) {
            double domainRadius = configuration.getDomainRadius();
            generator =
                    new CircleParticleGenerator(
                            domainRadius,
                            particleCount,
                            particleRadius,
                            particleMass,
                            initialVelocity,
                            random);
        } else {
            double domainSide = configuration.getDomainSide();
            generator =
                    new SquareParticleGenerator(
                            domainSide,
                            particleCount,
                            particleRadius,
                            particleMass,
                            initialVelocity,
                            random);
        }

        List<Particle> particles = generator.generate();

        for (Particle particle : particles) {
            System.out.println(particle);
        }


        double domainSide = configuration.getDomainSide();
        double maxTime = configuration.getMaxTime();

        Simulation simulation = new Simulation(new HashSet<>(particles), domainSide);
        simulation.run(maxTime);

    }
}

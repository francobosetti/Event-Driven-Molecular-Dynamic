package ar.edu.itba.ss.g2;

import ar.edu.itba.ss.g2.config.ArgParser;
import ar.edu.itba.ss.g2.config.Configuration;
import ar.edu.itba.ss.g2.generation.CircleParticleGenerator;
import ar.edu.itba.ss.g2.generation.ParticleGenerator;
import ar.edu.itba.ss.g2.generation.SquareParticleGenerator;
import ar.edu.itba.ss.g2.model.Output;
import ar.edu.itba.ss.g2.model.Particle;
import ar.edu.itba.ss.g2.simulation.Simulation;
import ar.edu.itba.ss.g2.utils.FileUtil;

import java.io.IOException;
import java.util.HashSet;
import java.util.List;
import java.util.Random;

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

        List<Particle> particles;

        try {
            System.out.println("Generating particles...");
            particles = generator.generate();
        } catch (IllegalStateException e) {
            System.err.println(e.getMessage());
            System.exit(1);
            return;
        }

        double domainSide = configuration.getDomainSide();
        double maxTime = configuration.getMaxTime();

        Simulation simulation = new Simulation(new HashSet<>(particles), domainSide);

        System.out.println("Running simulation...");

        simulation.run(maxTime);

        System.out.println("Simulation finished, writing output...");

        Output output = new Output(simulation.getSnapshots(), configuration);

        try {
            FileUtil.serializeOutput(output, configuration.getOutputDirectory());
        } catch (IOException e) {
            System.err.println("Error writing output file: " + e.getMessage());
            System.exit(1);
        }
    }
}

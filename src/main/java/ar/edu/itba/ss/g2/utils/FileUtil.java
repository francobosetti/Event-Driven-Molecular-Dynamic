package ar.edu.itba.ss.g2.utils;

import ar.edu.itba.ss.g2.config.Configuration;
import ar.edu.itba.ss.g2.model.Output;
import ar.edu.itba.ss.g2.model.Particle;
import ar.edu.itba.ss.g2.simulation.events.Event;

import java.io.BufferedWriter;
import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.util.*;
import java.util.Map.Entry;

public class FileUtil {

    private FileUtil() {
        throw new RuntimeException("Util class");
    }

    public static void serializeOutput(Output output, String directory) throws IOException {

        // Create directory if it doesn't exist
        File dir = new File(directory);
        if (!dir.exists()) {
            dir.mkdirs();
        }

        // Static
        Configuration configuration = output.configuration();
        try (FileWriter writer = new FileWriter(directory + "/static.txt")) {
            int particleCount = configuration.getParticleCount();
            if (configuration.isObstacleFree()) {
                particleCount += 1;
            }
            writer.write(particleCount + "\n");
            writer.write(configuration.getParticleRadius() + "\n");
            writer.write(configuration.getParticleMass() + "\n");
            writer.write(configuration.getInitialVelocity() + "\n");

            if (configuration.isDomainCircular()) {
                writer.write("circular\n");
                writer.write(configuration.getDomainRadius() + "\n");
            } else {
                writer.write("square\n");
                writer.write(configuration.getDomainSide() + "\n");
            }

            if (configuration.isObstacleFree()) {
                writer.write("free\n");
                writer.write(configuration.getObstacleRadius() + "\n");
                writer.write(configuration.getObstacleMass() + "\n");
            } else {
                writer.write("obstacle\n");
                writer.write(configuration.getObstacleRadius() + "\n");
            }
            writer.write(output.snapshots().size() + "\n");
            writer.write(output.events().size() + "\n");
        }

        // dynamic
        Map<Double, Set<Particle>> snapshots = output.snapshots();
        try (BufferedWriter writer = new BufferedWriter(new FileWriter(directory + "/snapshots.txt"), 128 * 1024)) {
            List<Entry<Double, Set<Particle>>> entries = new ArrayList<>(snapshots.entrySet());
            entries.sort(Comparator.comparingDouble(Entry::getKey));

            for (Entry<Double, Set<Particle>> entry : entries) {
                writer.write(entry.getKey() + "\n");

                List<Particle> particles = new ArrayList<>(entry.getValue());
                particles.sort(Comparator.comparingInt(Particle::getId));

                for (Particle particle : particles) {
                    writer.write(
                            String.format(
                                "%.5f %.5f %.5f %.5f\n", 
                                particle.getX(), 
                                particle.getY(), 
                                particle.getVx(),
                                particle.getVy())
                            );
                }
            }
        }

        List<Event> events = output.events();
        try (BufferedWriter writer = new BufferedWriter(new FileWriter(directory + "/events.txt"), 128 * 1024)) {
            for (Event event : events) {
                writer.write(event + "\n");
            }
        }
    }
}

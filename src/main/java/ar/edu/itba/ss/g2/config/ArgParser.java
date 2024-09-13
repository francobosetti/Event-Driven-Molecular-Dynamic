package ar.edu.itba.ss.g2.config;

import org.apache.commons.cli.*;

import java.util.Comparator;
import java.util.List;

public class ArgParser {

    private static final List<Option> OPTIONS =
            List.of(
                    new Option("h", "help", false, "Print this message"),
                    new Option("out", "output", true, "Output directory"),

                    // Simulation domain
                    new Option("d", "domain", true, "Domain type square|circular"),
                    new Option("sz", "size", true, "Domain side(square) or radius(circular)"),

                    // Particles
                    new Option("N", "particles", true, "Number of particles"),
                    new Option("r", "radius", true, "Particle radius"),
                    new Option("m", "mass", true, "Particle mass"),
                    new Option("v", "velocity", true, "Initial velocity"),
                    new Option("s", "seed", true, "Random seed"),

                    // Obstacle
                    new Option("obs", "obstacle", true, "Obstacle type free|fixed"),
                    new Option("or", "obstacle-radius", true, "Obstacle radius"),
                    new Option("om", "obstacle-mass", true, "Obstacle mass"),

                    // Simulation
                    new Option("e", "events", true, "Maximum events"));

    private final String[] args;
    private final Options options;

    public ArgParser(String[] args) {
        this.args = args;

        Options options = new Options();
        OPTIONS.forEach(options::addOption);
        this.options = options;
    }

    public Configuration parse() {

        CommandLineParser parser = new DefaultParser();

        CommandLine cmd;

        try {
            cmd = parser.parse(options, args);
        } catch (ParseException e) {
            System.err.println("Error parsing arguments: " + e.getMessage());
            return null;
        }

        if (cmd.hasOption("h")) {
            return null;
        }

        Configuration.Builder builder = new Configuration.Builder();

        // Output directory
        if (cmd.hasOption("out")) {
            builder.outputDirectory(cmd.getOptionValue("out"));
        } else {
            System.err.println("Output directory is required");
            return null;
        }

        // Max simulation time
        if (cmd.hasOption("e")) {

            long maxEvents;

            try {
                maxEvents = Long.parseLong(cmd.getOptionValue("e"));
            } catch (NumberFormatException e) {
                System.err.println("Invalid max events: " + cmd.getOptionValue("e"));
                return null;
            }

            if (maxEvents <= 0) {
                System.err.println("Max events must be greater than 0");
                return null;
            }

            builder.maxEvents(maxEvents);

        } else {
            System.err.println("Max events is required");
            return null;
        }

        // Simulation Domain
        if (cmd.hasOption("d") && cmd.hasOption("sz")) {

            String domainType = cmd.getOptionValue("d");

            if (!domainType.equals("square") && !domainType.equals("circular")) {
                System.err.println("Invalid domain type: " + domainType);
                return null;
            }

            boolean isCircular = domainType.equals("circular");

            double size;

            try {
                size = Double.parseDouble(cmd.getOptionValue("sz"));
            } catch (NumberFormatException e) {
                System.err.println("Invalid domain size: " + cmd.getOptionValue("sz"));
                return null;
            }

            if (size <= 0) {
                System.err.println("Domain size must be greater than 0");
                return null;
            }

            if (isCircular) {
                builder.circularDomain(size);
            } else {
                builder.squareDomain(size);
            }

        } else {
            System.err.println("Domain type and size are required");
            return null;
        }

        // Particles
        if (cmd.hasOption("N") && cmd.hasOption("r") && cmd.hasOption("m") && cmd.hasOption("v")) {

            int N;

            try {
                N = Integer.parseInt(cmd.getOptionValue("N"));
            } catch (NumberFormatException e) {
                System.err.println("Invalid number of particles: " + cmd.getOptionValue("N"));
                return null;
            }

            if (N <= 0) {
                System.err.println("Number of particles must be greater than 0");
                return null;
            }

            builder.particleCount(N);

            double r;

            try {
                r = Double.parseDouble(cmd.getOptionValue("r"));
            } catch (NumberFormatException e) {
                System.err.println("Invalid particle radius: " + cmd.getOptionValue("r"));
                return null;
            }

            if (r <= 0) {
                System.err.println("Particle radius must be greater than 0");
                return null;
            }

            builder.particleRadius(r);

            double m;

            try {
                m = Double.parseDouble(cmd.getOptionValue("m"));
            } catch (NumberFormatException e) {
                System.err.println("Invalid particle mass: " + cmd.getOptionValue("m"));
                return null;
            }

            if (m <= 0) {
                System.err.println("Particle mass must be greater than 0");
                return null;
            }

            builder.particleMass(m);

            double v;

            try {
                v = Double.parseDouble(cmd.getOptionValue("v"));
            } catch (NumberFormatException e) {
                System.err.println("Invalid initial velocity: " + cmd.getOptionValue("v"));
                return null;
            }

            if (v < 0) {
                System.err.println("Initial velocity must be greater or equal to 0");
                return null;
            }

            builder.initialVelocity(v);

            if (cmd.hasOption("s")) {
                long seed;

                try {
                    seed = Long.parseLong(cmd.getOptionValue("s"));
                } catch (NumberFormatException e) {
                    System.err.println("Invalid seed: " + cmd.getOptionValue("s"));
                    return null;
                }

                builder.seed(seed);
            }

        } else {
            System.err.println("Particle parameters are required: N, r, m, v");
            return null;
        }

        // Obstacle
        if (cmd.hasOption("obs") && cmd.hasOption("or")) {

            String obstacleType = cmd.getOptionValue("obs");

            if (!obstacleType.equals("free") && !obstacleType.equals("fixed")) {
                System.err.println("Invalid obstacle type: " + obstacleType);
                return null;
            }

            boolean isObstacleFree = obstacleType.equals("free");

            double or;

            try {
                or = Double.parseDouble(cmd.getOptionValue("or"));
            } catch (NumberFormatException e) {
                System.err.println("Invalid obstacle radius: " + cmd.getOptionValue("or"));
                return null;
            }

            if (or <= 0) {
                System.err.println("Obstacle radius must be greater than 0");
                return null;
            }

            if (isObstacleFree) {

                if (!cmd.hasOption("om")) {
                    System.err.println("Obstacle mass is required");
                    return null;
                }

                double om;

                try {
                    om = Double.parseDouble(cmd.getOptionValue("om"));
                } catch (NumberFormatException e) {
                    System.err.println("Invalid obstacle mass: " + cmd.getOptionValue("om"));
                    return null;
                }

                if (om <= 0) {
                    System.err.println("Obstacle mass must be greater than 0");
                    return null;
                }

                builder.freeObstacle(om, or);
            } else {
                builder.obstacle(or);
            }
        } else {
            System.err.println("Obstacle parameters are required: obs, or, om");
            return null;
        }

        return builder.build();
    }

    public void printHelp() {

        HelpFormatter formatter = new HelpFormatter();
        formatter.setOptionComparator(Comparator.comparingInt(OPTIONS::indexOf));

        formatter.setLeftPadding(4);
        formatter.setWidth(120);

        String commandLineSyntax =
                "java -jar event-driven-molecular-dynamics-1.0-SNAPSHOT-jar-with-dependencies.jar"
                        + " [options]";

        formatter.printHelp(commandLineSyntax, options);
    }
}

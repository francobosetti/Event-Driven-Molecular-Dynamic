package ar.edu.itba.ss.g2.config;

import java.util.Random;

public class Configuration {

    // For simulation domain
    private final double domainSide;
    private final double domainRadius;
    private final boolean isDomainCircular;

    // For particles
    private final int particleCount;
    private final double particleRadius;
    private final double particleMass;
    private final double initialVelocity;
    private final Random random;

    // For Obstacle
    private final double obstacleMass;
    private final double obstacleRadius;
    private final boolean isObstacleFree;

    private final double maxTime;

    private final String outputDirectory;

    private Configuration(Builder builder) {
        this.domainSide = builder.domainSide;
        this.domainRadius = builder.domainRadius;
        this.isDomainCircular = builder.isDomainCircular;

        this.particleCount = builder.particleCount;
        this.particleRadius = builder.particleRadius;
        this.particleMass = builder.particleMass;
        this.initialVelocity = builder.initialVelocity;

        this.random = builder.seed != null ? new Random(builder.seed) : new Random();

        this.obstacleMass = builder.obstacleMass;
        this.obstacleRadius = builder.obstacleRadius;
        this.isObstacleFree = builder.isObstacleFree;

        this.maxTime = builder.maxTime;

        this.outputDirectory = builder.outputDirectory;
    }

    public double getDomainSide() {

        if (isDomainCircular) {
            throw new IllegalStateException("Domain is circular, use getDomainRadius instead");
        }

        return domainSide;
    }

    public double getDomainRadius() {

        if (!isDomainCircular) {
            throw new IllegalStateException("Domain is not circular, use getDomainSide instead");
        }

        return domainRadius;
    }

    public boolean isDomainCircular() {
        return isDomainCircular;
    }

    public int getParticleCount() {
        return particleCount;
    }

    public double getParticleRadius() {
        return particleRadius;
    }

    public double getParticleMass() {
        return particleMass;
    }

    public double getInitialVelocity() {
        return initialVelocity;
    }

    public Random getRandom() {
        return random;
    }

    public double getObstacleMass() {

        if (!isObstacleFree) {
            throw new IllegalStateException("Obstacle is not free, therefore it has no mass");
        }

        return obstacleMass;
    }

    public double getObstacleRadius() {
        return obstacleRadius;
    }

    public boolean isObstacleFree() {
        return isObstacleFree;
    }

    public double getMaxTime() {
        return maxTime;
    }

    public String getOutputDirectory() {
        return outputDirectory;
    }

    @Override
    public String toString() {
        return "Configuration{"
                + "domainSide="
                + domainSide
                + ", domainRadius="
                + domainRadius
                + ", isDomainCircular="
                + isDomainCircular
                + ", particleCount="
                + particleCount
                + ", particleRadius="
                + particleRadius
                + ", particleMass="
                + particleMass
                + ", initialVelocity="
                + initialVelocity
                + ", seed="
                + random
                + ", obstacleMass="
                + obstacleMass
                + ", obstacleRadius="
                + obstacleRadius
                + ", isObstacleFree="
                + isObstacleFree
                + ", maxTime="
                + maxTime
                + ", outputDirectory='"
                + outputDirectory
                + '\''
                + '}';
    }

    public static class Builder {

        // For simulation domain
        private double domainSide;
        private double domainRadius;
        private boolean isDomainCircular;

        // For particles
        private int particleCount;
        private double particleRadius;
        private double particleMass;
        private double initialVelocity;
        private Long seed;

        // For Obstacle
        private double obstacleMass;
        private double obstacleRadius;
        private boolean isObstacleFree;

        private double maxTime;

        private String outputDirectory;

        public Builder() {}

        public Builder circularDomain(double domainRadius) {
            this.domainRadius = domainRadius;
            this.isDomainCircular = true;
            return this;
        }

        public Builder squareDomain(double domainSide) {
            this.domainSide = domainSide;
            this.isDomainCircular = false;
            return this;
        }

        public Builder particleCount(int particleCount) {
            this.particleCount = particleCount;
            return this;
        }

        public Builder particleRadius(double particleRadius) {
            this.particleRadius = particleRadius;
            return this;
        }

        public Builder particleMass(double particleMass) {
            this.particleMass = particleMass;
            return this;
        }

        public Builder initialVelocity(double initialVelocity) {
            this.initialVelocity = initialVelocity;
            return this;
        }

        public Builder seed(long seed) {
            this.seed = seed;
            return this;
        }

        public Builder freeObstacle(double obstacleMass, double obstacleRadius) {
            this.obstacleMass = obstacleMass;
            this.isObstacleFree = true;
            return this;
        }

        public Builder obstacle(double obstacleRadius) {
            this.obstacleRadius = obstacleRadius;
            this.isObstacleFree = false;
            return this;
        }

        public Builder maxTime(double maxTime) {
            this.maxTime = maxTime;
            return this;
        }

        public Builder outputDirectory(String outputDirectory) {
            this.outputDirectory = outputDirectory;
            return this;
        }

        public Configuration build() {
            return new Configuration(this);
        }
    }
}

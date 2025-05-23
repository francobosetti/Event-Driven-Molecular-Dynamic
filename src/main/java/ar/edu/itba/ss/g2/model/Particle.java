package ar.edu.itba.ss.g2.model;

public class Particle {
    private int id;

    private Double x;
    private Double y;

    private Double vx;
    private Double vy;

    private final Double radius;
    private final Double mass;

    private int collisionCount;

    public Particle(int id, Double x, Double y, Double vx, Double vy, Double radius, Double mass) {
        this.id = id;
        this.x = x;
        this.y = y;
        this.vx = vx;
        this.vy = vy;
        this.radius = radius;
        this.mass = mass;
        this.collisionCount = 0;
    }

    public Particle(Particle particle) {
        this.id = particle.id;
        this.x = particle.x;
        this.y = particle.y;
        this.vx = particle.vx;
        this.vy = particle.vy;
        this.radius = particle.radius;
        this.mass = particle.mass;
        this.collisionCount = particle.collisionCount;
    }

    public int getId() {
        return id;
    }

    public Double getX() {
        return x;
    }

    public Double getY() {
        return y;
    }

    public Double getVx() {
        return vx;
    }

    public Double getVy() {
        return vy;
    }

    public Double getMass() {
        return mass;
    }

    public Double getRadius() {
        return radius;
    }

    public void setX(Double x) {
        this.x = x;
    }

    public void setY(Double y) {
        this.y = y;
    }

    public void setVx(Double vx) {
        this.vx = vx;
    }

    public void setVy(Double vy) {
        this.vy = vy;
    }

    // return the total number of collisions involving this particle.
    public int getCollisionCount() {
        return collisionCount;
    }

    public void incrementCollisionCount() {
        collisionCount++;
    }

    public boolean overlaps(Particle other) {
        double otherX = other.getX();
        double otherY = other.getY();

        double distance = Math.sqrt(Math.pow(x - otherX, 2) + Math.pow(y - otherY, 2));

        return distance < radius + other.getRadius();
    }

    @Override
    public String toString() {
        return "Particle{"
                + "id="
                + id
                + ", x="
                + x
                + ", y="
                + y
                + ", vx="
                + vx
                + ", vy="
                + vy
                + ", mass="
                + mass
                + ", radius="
                + radius
                + ", collisionCount="
                + collisionCount
                + '}';
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (!(o instanceof Particle particle)) return false;
        return this.id == particle.id;
    }

    @Override
    public int hashCode() {
        return Integer.hashCode(id);
    }
}

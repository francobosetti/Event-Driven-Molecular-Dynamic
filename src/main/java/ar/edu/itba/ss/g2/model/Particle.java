package ar.edu.itba.ss.g2.model;

public class Particle {
    private int id;

    private Double x;
    private Double y;

    private Double vx;
    private Double vy;

    private final Double mass;
    private final Double radius;

    private int collisionCount;

    public Particle(int id, Double x, Double y, Double vx, Double vy, Double mass, Double radius) {
        this.x = x;
        this.y = y;
        this.vx = vx;
        this.vy = vy;
        this.mass = mass;
        this.radius = radius;
        this.collisionCount = 0;
    }

    // return the duration of time until the invoking particle collides with a vertical wall,
    // assuming it follows a straight-line trajectory. If the particle never collides with a vertical wall, return NULL
    public Double collidesX(double L) {
        throw new UnsupportedOperationException("Not implemented yet");
    }

    // return the duration of time until the invoking particle collides with a horizontal wall,
    // assuming it follows a straight-line trajectory. If the particle never collides with a horizontal wall, return NULL
    public Double collidesY(double L) {
        throw new UnsupportedOperationException("Not implemented yet");
    }

    // return the duration of time until the invoking particle collides with particle
    // b, assuming both follow straight-line trajectories. If the two particles never collide, return NULL
    public Double collides(Particle b) {
        throw new UnsupportedOperationException("Not implemented yet");
    }

    // update the invoking particle to simulate it bouncing off a vertical wall
    public void bounceX() {
        vx = -vx;
    }

    // update the invoking particle to simulate it bouncing off a horizontal wall
    public void bounceY() {
        vy = -vy;
    }

    // update both particles to simulate them bouncing off each other.
    public void bounce(Particle b) {
        throw new UnsupportedOperationException("Not implemented yet");
    }

    // return the total number of collisions involving this particle.
    public int getCollisionCount() {
        return collisionCount;
    }

    @Override
    public String toString() {
        return "Particle{" +
                "id=" + id +
                "x=" + x +
                ", y=" + y +
                ", vx=" + vx +
                ", vy=" + vy +
                ", mass=" + mass +
                ", radius=" + radius +
                ", collisionCount=" + collisionCount +
                '}';
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

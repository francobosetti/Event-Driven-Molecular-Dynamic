package ar.edu.itba.ss.g2.model;

public class Event implements Comparable<Event> {
    private final double t;
    private final Particle a;
    private final int collisionCountA;
    private final Particle b;
    private final int collisionCountB;

    public Event(double t, Particle a, Particle b) {
        this.t = t;
        this.a = a;
        this.b = b;
        this.collisionCountA = a.getCollisionCount();
        this.collisionCountB = b.getCollisionCount();
    }

    // return the time associated with the event.
    public double getTime() {
        return t;
    }

    // return the first particle, possibly null.
    public Particle getParticle1() {
        return a;
    }

    // return the second particle, possibly null.
    public Particle getParticle2() {
        return b;
    }

    // compare the time associated with this event and x. Return a positive number (greater),
    // negative number (less), or zero (equal) accordingly.
    @Override
    public int compareTo(Event x) {
        if (this.t < x.t) {
            return -1;
        }
        if (this.t > x.t) {
            return 1;
        }
        return 0;
    }

    public boolean wasSuperveningEvent() {
        return a.getCollisionCount() != collisionCountA || b.getCollisionCount() != collisionCountB;
    }
}

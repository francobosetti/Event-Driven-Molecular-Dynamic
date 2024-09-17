package ar.edu.itba.ss.g2.simulation.events;

import ar.edu.itba.ss.g2.model.Particle;

public abstract class Event implements Comparable<Event> {
    private final double t;
    private final Particle[] particles;

    public Event(double t, Particle[] particles) {
        this.t = t;
        this.particles = particles;
    }

    // return the time associated with the event.
    public double getTime() {
        return t;
    }

    // return the particles associated with the event.
    public Particle[] getParticles() {
        return particles;
    }

    // compare the time associated with this event and x. Return a positive number (greater),
    // negative number (less), or zero (equal) accordingly.
    @Override
    public int compareTo(Event x) {
        return Double.compare(this.t, x.t);
    }

    public abstract boolean isInvalid();


    public abstract void resolveCollision();
}

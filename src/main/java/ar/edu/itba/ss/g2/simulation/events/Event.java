package ar.edu.itba.ss.g2.simulation.events;

public abstract class Event implements Comparable<Event> {
    private final double t;

    public Event(double t) {
        this.t = t;
    }

    // return the time associated with the event.
    public double getTime() {
        return t;
    }

    // compare the time associated with this event and x. Return a positive number (greater),
    // negative number (less), or zero (equal) accordingly.
    @Override
    public int compareTo(Event x) {
        return Double.compare(this.t, x.t);
    }

    abstract boolean wasSuperveningEvent();


    abstract void resolveCollision();
}

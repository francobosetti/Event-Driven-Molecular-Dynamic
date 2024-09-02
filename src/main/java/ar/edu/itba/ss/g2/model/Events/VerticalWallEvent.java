package ar.edu.itba.ss.g2.model.Events;

import ar.edu.itba.ss.g2.model.Particle;

public class VerticalWallEvent extends Event{
    private final Particle particle;

    public VerticalWallEvent(double time, Particle particle) {
        super(time);
        this.particle = particle;
    }
}

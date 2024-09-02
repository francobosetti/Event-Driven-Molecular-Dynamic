package ar.edu.itba.ss.g2.model.Events;

import ar.edu.itba.ss.g2.model.Particle;

public class HorizontalWallEvent extends Event{
    private Particle particle;

    public HorizontalWallEvent(double time, Particle particle) {
        super(time);
        this.particle = particle;
    }
}

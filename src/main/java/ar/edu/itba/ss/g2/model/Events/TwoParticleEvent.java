package ar.edu.itba.ss.g2.model.Events;

import ar.edu.itba.ss.g2.model.Particle;

public class TwoParticleEvent extends Event{
    private final Particle a;
    private final int collisionCountA;
    private final Particle b;
    private final int collisionCountB;

    public TwoParticleEvent(double time, Particle a, int collisionCountA, Particle b, int collisionCountB) {
        super(time);
        this.a = a;
        this.collisionCountA = collisionCountA;
        this.b = b;
        this.collisionCountB = collisionCountB;
    }

    // return the first particle
    public Particle getParticle1() {
        return a;
    }

    // return the second particle
    public Particle getParticle2() {
        return b;
    }

    @Override
    public boolean wasSuperveningEvent() {
        return a.getCollisionCount() != collisionCountA || b.getCollisionCount() != collisionCountB;
    }
}

package ar.edu.itba.ss.g2.simulation;

import ar.edu.itba.ss.g2.generation.ParticleGenerator;
import ar.edu.itba.ss.g2.model.Particle;

import java.util.ArrayList;
import java.util.List;
import java.util.Set;

public class Simulation {

    private final List<Set<Particle>> snapshots;


    public Simulation(Set<Particle> particles) {
        this.snapshots = new ArrayList<>();
        this.snapshots.add(particles);
    }

    public void run() {
        // calculate all possible collitions
        //
    }

    public List<Set<Particle>> getSnapshots() {
        return snapshots;
    }
}

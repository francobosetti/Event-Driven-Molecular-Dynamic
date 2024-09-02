package ar.edu.itba.ss.g2.simulation;

import ar.edu.itba.ss.g2.model.Particle;

import java.util.ArrayList;
import java.util.List;
import java.util.Set;

public class Simulation {

    private final List<Set<Particle>> snapshots;


    public Simulation() {
        this.snapshots = new ArrayList<>();
    }

    public void run() {
    }

    public List<Set<Particle>> getSnapshots() {
        return snapshots;
    }
}

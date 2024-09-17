package ar.edu.itba.ss.g2.model;

import ar.edu.itba.ss.g2.config.Configuration;
import ar.edu.itba.ss.g2.simulation.events.Event;

import java.util.List;
import java.util.Map;
import java.util.Set;

public record Output(
        Map<Double, Set<Particle>> snapshots, List<Event> events, Configuration configuration) {}

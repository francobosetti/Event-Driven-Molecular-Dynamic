package ar.edu.itba.ss.g2.model;

import java.util.Map;
import java.util.Set;

import ar.edu.itba.ss.g2.config.Configuration;

public record Output(Map<Double, Set<Particle>> snapshots, Configuration configuration) {}

package ar.edu.itba.ss.g2.model.Events;

public class RedrawEvent extends Event {
    public RedrawEvent(double time) {
        super(time);
    }

    @Override
    boolean wasSuperveningEvent() {
        throw new UnsupportedOperationException("Not implemented yet");
    }
}

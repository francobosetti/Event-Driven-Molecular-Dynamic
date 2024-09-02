package ar.edu.itba.ss.g2.config;

public class Configuration {


    private Configuration(Builder builder) {
    }


    @Override
    public String toString() {
        return "Configuration{" +
                '}';
    }

    public static class Builder {

        public Builder() {}


        public Configuration build() {
            return new Configuration(this);
        }
    }
}

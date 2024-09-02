package ar.edu.itba.ss.g2.config;

import org.apache.commons.cli.*;

import java.util.Comparator;
import java.util.List;

public class ArgParser {

    private static final List<Option> OPTIONS =
            List.of();

    private final String[] args;
    private final Options options;

    public ArgParser(String[] args) {
        this.args = args;

        Options options = new Options();
        OPTIONS.forEach(options::addOption);
        this.options = options;
    }

    public Configuration parse() {

        CommandLineParser parser = new DefaultParser();

        CommandLine cmd;

        try {
            cmd = parser.parse(options, args);
        } catch (ParseException e) {
            System.err.println("Error parsing arguments: " + e.getMessage());
            return null;
        }

        if (cmd.hasOption("h")) {
            return null;
        }

        Configuration.Builder builder = new Configuration.Builder();




        return builder.build();
    }

    public void printHelp() {

        HelpFormatter formatter = new HelpFormatter();
        formatter.setOptionComparator(Comparator.comparingInt(OPTIONS::indexOf));

        formatter.setLeftPadding(4);
        formatter.setWidth(120);

        String commandLineSyntax =
                "java -jar event-driven-molecular-dynamics-1.0-SNAPSHOT-jar-with-dependencies.jar [options]";

        formatter.printHelp(commandLineSyntax, options);
    }
}

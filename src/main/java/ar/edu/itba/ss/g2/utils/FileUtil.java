package ar.edu.itba.ss.g2.utils;

import ar.edu.itba.ss.g2.model.Output;
import ar.edu.itba.ss.g2.model.Particle;

import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.util.*;

public class FileUtil {

    private FileUtil() {
        throw new RuntimeException("Util class");
    }

    public static void serializeOutput(Output output, String directory)
            throws IOException {

        // Create directory if it doesn't exist
        File dir = new File(directory);
        if (!dir.exists()) {
            dir.mkdirs();
        }

        // Dynamic
        try (FileWriter writer = new FileWriter(directory + "/dynamic.txt")) {
        }

        // Static
        try (FileWriter writer = new FileWriter(directory + "/static.txt")) {
        }
    }
}

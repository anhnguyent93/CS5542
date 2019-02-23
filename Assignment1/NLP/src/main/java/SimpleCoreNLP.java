
import edu.stanford.nlp.coref.CorefCoreAnnotations;
import edu.stanford.nlp.coref.data.CorefChain;
import edu.stanford.nlp.ling.CoreAnnotations;
import edu.stanford.nlp.ling.CoreLabel;
import edu.stanford.nlp.pipeline.Annotation;
import edu.stanford.nlp.pipeline.StanfordCoreNLP;
import edu.stanford.nlp.simple.*;
import edu.stanford.nlp.trees.Tree;
import edu.stanford.nlp.trees.TreeCoreAnnotations;
import edu.stanford.nlp.util.CoreMap;
import javafx.util.Pair;
import org.apache.commons.lang3.StringUtils;

import javax.swing.*;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.io.PrintWriter;
import java.io.UnsupportedEncodingException;
import java.lang.reflect.Array;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.*;


public class SimpleCoreNLP {
    public static void main(String[] args) {
        // creates a StanfordCoreNLP object, with POS tagging, lemmatization, NER, parsing, and coreference resolution
        Properties props = new Properties();
        props.setProperty("annotators", "tokenize, ssplit, pos, lemma, ner, parse, dcoref");
        StanfordCoreNLP pipeline = new StanfordCoreNLP(props);

        Map<String, ArrayList<Integer>> mapCaption = new HashMap<>();

        // Create a document. No computation is done yet.
        List<String> lines = Collections.emptyList();
        try
        {
            lines = Files.readAllLines(Paths.get("data\\SBU\\SBU_captioned_photo_dataset_captions.txt"), StandardCharsets.UTF_8);
        }
        catch (IOException e)
        {
            e.printStackTrace();
        }

        for (int i = 0; i < 1000; i++) {
            // create an empty Annotation just with the given text
            Annotation document = new Annotation(lines.get(i));

            // run all Annotators on this text
            pipeline.annotate(document);

            // these are all the sentences in a caption
            List<CoreMap> sentences = document.get(CoreAnnotations.SentencesAnnotation.class);

            for (CoreMap sentence : sentences) {
               for (CoreLabel token : sentence.get(CoreAnnotations.TokensAnnotation.class)) {

                    String lemma = token.get(CoreAnnotations.LemmaAnnotation.class);

                    if (mapCaption.containsKey(lemma)) {
                        if (!mapCaption.get(lemma).contains(i)) {
                            mapCaption.get(lemma).add(i);
                        }
                        continue;
                    }

                    String pos = token.get(CoreAnnotations.PartOfSpeechAnnotation.class);

                    if (pos.contains("NN")) {
                        ArrayList<Integer> list = new ArrayList<Integer>();
                        list.add(i);
                        mapCaption.put(lemma, list);
                    }
                }
            }
        }


        PrintWriter writer = null;
        try {
            writer = new PrintWriter("output.txt", "UTF-8");
        } catch (FileNotFoundException e) {
            e.printStackTrace();
        } catch (UnsupportedEncodingException e) {
            e.printStackTrace();
        }

        for (String key : mapCaption.keySet()) {
            String s = "";
            for (Integer in : mapCaption.get(key)){
                s += in + " ";
            }
            writer.println(key + " " + mapCaption.get(key).size() + " " + s);
        }
        writer.close();

    }
}
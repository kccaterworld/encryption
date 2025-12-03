import java.util.*;
import java.io.*;
import java.lang.System;
@SuppressWarnings("unused")

public class Caesar {
    private String chars = "!?.,'_-;:\"()[]{}<>@#$%^&*~`+=/\\|\n\r\t";

    public static void main(String[] args) {
        long startTime = System.nanoTime();
        String plaintext = "Hello, World!";
        compileWords(plaintext.length());
        System.out.printf("%s milliseconds\n", (System.nanoTime() - startTime) / 1000000);
        String ciphertext = caesarCipher(plaintext, 3, true);
        System.out.printf("Ciphertext: %s\n", ciphertext);
        System.out.printf("%s milliseconds\n", (System.nanoTime() - startTime) / 1000000);
    }

    public static ArrayList<String> compileWords() {
        try{
            ArrayList<String> list = new ArrayList<String>();
            File wordsFile = new File("Caesar/WordLists/allWords.txt");
            Scanner input = new Scanner(wordsFile);
            while (input.hasNextLine()){
                list.add(input.nextLine());
            }
            input.close();
            return list;
        }
        catch(IOException e){
            e.printStackTrace();
            return null;
        }
    }
    public static ArrayList<String> compileWords(int lenText) {
        try{
            ArrayList<String> list = new ArrayList<String>();
            File wordsFile = new File("Caesar/WordLists/allWords.txt");
            Scanner input = new Scanner(wordsFile);
            while (input.hasNextLine()){
                String next = input.nextLine();
                if (next.length() == lenText)
                    list.add(next);
            }
            input.close();
            return list;
        }
        catch(IOException e){
            e.printStackTrace();
            return null;
        }
    }

    public static String caesarCipher(String text, int shift, boolean encrypt) {
        String[] alpha = { "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z" };
        if (encrypt){
            String encoded = "";
            for (int i = 0; i < text.length(); i++) {
                String glyph = text.substring(i, i + 1);
                if (!Arrays.asList(alpha).contains(glyph.toLowerCase())) {
                    encoded += glyph;
                    continue;
                }
                if (glyph.equals(" ")) {
                    encoded += " ";
                    continue;
                }
                if (glyph.equals(glyph.toLowerCase())) {
                    encoded += alpha[(Arrays.asList(alpha).indexOf(glyph) + shift) % 26];
                    continue;
                }
                if (glyph.equals(glyph.toUpperCase())) {
                    encoded += alpha[(Arrays.asList(alpha).indexOf(glyph.toLowerCase()) + shift) % 26].toUpperCase();
                    continue;
                }
            }
            return encoded;
        }
        if (!encrypt){
            return caesarCipher(text, -shift, true);
        }
        return null;
    }
}

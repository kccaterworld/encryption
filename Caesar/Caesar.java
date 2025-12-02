import java.util.*;
import java.io.*;
import java.lang.System;

public class Caesar {
    private String chars = "!?.,'_-;:\"()[]{}<>@#$%^&*~`+=/\\|\n\r\t";

    public void main(String[] args) {
        long startTime = System.nanoTime();
        String plaintext = "Hello, World!";
        compileWords(plaintext.length());
        String ciphertext = caesarCipher(plaintext, 3, true);
        System.out.println(System.nanoTime() - startTime);
    }

    public ArrayList<String> compileWords() {
        try{
            ArrayList<String> list = new ArrayList<String>();
            File wordsFile = new File("WordLists/allWords.txt");
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
    public ArrayList<String> compileWords(int lenText) {
        try{
            ArrayList<String> list = new ArrayList<String>();
            File wordsFile = new File("WordLists/allWords.txt");
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
        ArrayList<String> alphabet = new ArrayList<String>();
        return "";
    }
}
